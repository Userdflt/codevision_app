"""
FastAPI dependencies for authentication and authorization.
"""

from typing import Dict, Any, Optional
import structlog
import time
import json
from functools import lru_cache
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import httpx

from agent_project.config import settings


logger = structlog.get_logger()
security = HTTPBearer()

# Cache for Supabase public keys
_supabase_jwks_cache = {}
_jwks_cache_expiry = 0


@lru_cache(maxsize=1)
def get_supabase_jwks_url() -> str:
    """Get Supabase JWKS URL."""
    return f"{settings.supabase_url}/auth/v1/.well-known/jwks.json"


async def get_supabase_public_keys() -> Dict[str, Any]:
    """
    Fetch and cache Supabase public keys for JWT validation.
    Handles both ECC (P-256) and RSA keys.
    """
    global _supabase_jwks_cache, _jwks_cache_expiry
    
    # Check cache (refresh every hour)
    current_time = time.time()
    if _supabase_jwks_cache and current_time < _jwks_cache_expiry:
        return _supabase_jwks_cache
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(get_supabase_jwks_url(), timeout=10.0)
            response.raise_for_status()
            jwks_data = response.json()
            
            # Cache for 1 hour
            _supabase_jwks_cache = jwks_data
            _jwks_cache_expiry = current_time + 3600
            
            logger.debug(
                "Fetched Supabase JWKS", 
                keys_count=len(jwks_data.get("keys", [])),
                key_types=[key.get("kty") for key in jwks_data.get("keys", [])]
            )
            return jwks_data
            
    except Exception as e:
        logger.error("Failed to fetch Supabase JWKS", error=str(e))
        # Return cached data if available, otherwise raise
        if _supabase_jwks_cache:
            logger.warning("Using cached JWKS due to fetch error")
            return _supabase_jwks_cache
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to validate tokens at this time"
        )


def build_ec_key(jwk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build an EC (Elliptic Curve) key from JWK for ECC P-256 keys.
    """
    if jwk.get("kty") != "EC" or jwk.get("crv") != "P-256":
        raise JWTError("Unsupported EC key type")
    
    return {
        "kty": "EC",
        "crv": "P-256",
        "x": jwk["x"],
        "y": jwk["y"],
        "use": jwk.get("use"),
        "kid": jwk.get("kid")
    }


def build_rsa_key(jwk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build an RSA key from JWK for legacy RSA keys.
    """
    if jwk.get("kty") != "RSA":
        raise JWTError("Unsupported RSA key type")
    
    return {
        "kty": "RSA",
        "kid": jwk.get("kid"),
        "use": jwk.get("use"),
        "n": jwk["n"],
        "e": jwk["e"]
    }


async def validate_supabase_jwt(token: str) -> Dict[str, Any]:
    """
    Validate Supabase JWT token using Supabase public keys.
    Supports both new ECC (P-256) and legacy RSA keys.
    """
    try:
        # Get the token header to find the correct key
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        alg = unverified_header.get("alg")
        
        if not kid:
            raise JWTError("Token missing key ID")
        
        logger.debug("Validating JWT", kid=kid, algorithm=alg)
        
        # Get public keys
        jwks = await get_supabase_public_keys()
        
        # Find the correct key
        signing_key = None
        key_algorithm = None
        
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                key_type = key.get("kty")
                
                if key_type == "EC":
                    # New ECC P-256 keys
                    signing_key = build_ec_key(key)
                    key_algorithm = "ES256"
                elif key_type == "RSA":
                    # Legacy RSA keys
                    signing_key = build_rsa_key(key)
                    key_algorithm = "RS256"
                else:
                    logger.warning("Unsupported key type", key_type=key_type, kid=kid)
                    continue
                
                break
        
        if not signing_key:
            raise JWTError(f"Unable to find appropriate key for kid: {kid}")
        
        if not key_algorithm:
            raise JWTError("Unable to determine key algorithm")
        
        logger.debug("Using key", key_type=signing_key.get("kty"), algorithm=key_algorithm)
        
        # Validate the token
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=[key_algorithm],
            audience="authenticated",
            issuer=f"{settings.supabase_url}/auth/v1"
        )
        
        # Additional validation
        required_claims = ["sub", "aud", "exp", "iss"]
        for claim in required_claims:
            if claim not in payload:
                raise JWTError(f"Missing required claim: {claim}")
        
        # Check if token is expired (jose should handle this, but double-check)
        current_time = time.time()
        if payload.get("exp", 0) < current_time:
            raise JWTError("Token has expired")
        
        logger.debug("Supabase JWT validated successfully", user_id=payload.get("sub"))
        return payload
        
    except JWTError as e:
        logger.warning("Supabase JWT validation failed", error=str(e))
        raise
    except Exception as e:
        logger.error("JWT validation error", error=str(e))
        raise JWTError(f"Token validation failed: {str(e)}")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Validate JWT token and extract user information.
    Tries Supabase JWT validation first, with fallback for development.
    """
    try:
        token = credentials.credentials
        
        # Try Supabase JWT validation first
        try:
            payload = await validate_supabase_jwt(token)
            
            # Extract user information from Supabase JWT
            return {
                "sub": payload.get("sub"),
                "email": payload.get("email"),
                "role": payload.get("role", "authenticated"),
                "aud": payload.get("aud"),
                "exp": payload.get("exp"),
                "user_metadata": payload.get("user_metadata", {}),
                "app_metadata": payload.get("app_metadata", {}),
                "session_id": payload.get("session_id"),
                "iss": payload.get("iss")
            }
            
        except JWTError as e:
            # Fallback to basic JWT validation for development/testing
            if settings.app_env == "development":
                logger.warning("Falling back to basic JWT validation", error=str(e))
                
                payload = jwt.decode(
                    token,
                    settings.jwt_secret_key,
                    algorithms=[settings.jwt_algorithm]
                )
                
                user_id = payload.get("sub")
                if user_id is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token: missing user ID",
                        headers={"WWW-Authenticate": "Bearer"}
                    )
                
                return {
                    "sub": user_id,
                    "email": payload.get("email"),
                    "role": payload.get("role", "user"),
                    "aud": payload.get("aud"),
                    "exp": payload.get("exp")
                }
            else:
                # In production, don't fallback
                raise
        
    except JWTError as e:
        logger.warning("JWT validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        logger.error("Authentication error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_admin_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Require admin role for accessing admin endpoints.
    Checks both role claim and app_metadata for admin permissions.
    """
    user_role = current_user.get("role", "authenticated")
    app_metadata = current_user.get("app_metadata", {})
    
    # Check if user has admin role in various locations
    is_admin = (
        user_role == "admin" or 
        app_metadata.get("role") == "admin" or
        "admin" in app_metadata.get("roles", []) or
        app_metadata.get("claims", {}).get("admin") is True
    )
    
    if not is_admin:
        logger.warning(
            "Admin access denied",
            user_id=current_user.get("sub"),
            role=user_role,
            app_metadata=app_metadata
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    logger.info("Admin user authenticated", user_id=current_user.get("sub"))
    return current_user


# Optional: Helper for checking if user is authenticated
async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    )
) -> Optional[Dict[str, Any]]:
    """
    Optional authentication - returns user if token is provided and valid, None otherwise.
    Useful for endpoints that work with or without authentication.
    """
    if not credentials:
        return None
    
    try:
        # Temporarily set credentials for get_current_user
        return await get_current_user(credentials)
    except HTTPException:
        # If token is invalid, return None instead of raising error
        return None