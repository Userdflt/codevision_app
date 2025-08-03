"""
FastAPI dependencies for authentication and authorization.
"""

from typing import Dict, Any
import structlog
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from agent_project.config import settings


logger = structlog.get_logger()
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Validate JWT token and extract user information.
    
    Args:
        credentials: HTTP Bearer token from request header
        
    Returns:
        User information dictionary
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Extract token
        token = credentials.credentials
        
        # Decode JWT token
        # Note: In production, you should validate against Supabase public key
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        
        # Extract user ID
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # TODO: Add additional token validation (expiration, audience, etc.)
        # TODO: Validate against Supabase JWT format
        
        logger.debug("User authenticated", user_id=user_id)
        
        return {
            "sub": user_id,
            "email": payload.get("email"),
            "role": payload.get("role", "user"),
            "aud": payload.get("aud"),
            "exp": payload.get("exp")
        }
        
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
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User information if user is admin
        
    Raises:
        HTTPException: If user is not admin
    """
    user_role = current_user.get("role", "user")
    
    if user_role != "admin":
        logger.warning(
            "Admin access denied",
            user_id=current_user.get("sub"),
            role=user_role
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    logger.info("Admin user authenticated", user_id=current_user.get("sub"))
    return current_user


async def validate_supabase_jwt(token: str) -> Dict[str, Any]:
    """
    Validate Supabase JWT token using Supabase public key.
    
    This is a placeholder implementation. In production, you should:
    1. Fetch Supabase's public key from their JWKS endpoint
    2. Validate the token signature
    3. Check token expiration and audience
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
    """
    try:
        # TODO: Implement proper Supabase JWT validation
        # For now, use basic JWT decoding
        
        # In production, you would:
        # 1. Get public key: GET https://{supabase_url}/auth/v1/.well-known/jwks.json
        # 2. Validate signature with the public key
        # 3. Check aud, iss, exp claims
        
        payload = jwt.decode(
            token,
            options={"verify_signature": False},  # Disable for development
            algorithms=["HS256", "RS256"]
        )
        
        # Validate required claims
        required_claims = ["sub", "aud", "exp", "iss"]
        for claim in required_claims:
            if claim not in payload:
                raise JWTError(f"Missing required claim: {claim}")
        
        # Check if token is from Supabase
        if not payload.get("iss", "").startswith("https://"):
            raise JWTError("Invalid issuer")
        
        return payload
        
    except JWTError as e:
        logger.warning("Supabase JWT validation failed", error=str(e))
        raise
    except Exception as e:
        logger.error("JWT validation error", error=str(e))
        raise JWTError(f"Token validation failed: {str(e)}")