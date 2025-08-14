"""
LLM client for interfacing with various language model providers.
"""

from typing import Optional, Dict, AsyncGenerator
import structlog
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from agent_project.config import settings


logger = structlog.get_logger()


class LLMClient:
    """
    Unified client for multiple LLM providers.
    
    Supports OpenAI and Anthropic with automatic provider selection
    based on configuration.
    """
    
    def __init__(self):
        self.default_provider = settings.default_llm_provider
        self.default_model = settings.default_model
        
        # Initialize clients based on available API keys
        self.openai_client = None
        self.anthropic_client = None
        
        if settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        
        if settings.anthropic_api_key:
            self.anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        
        logger.info(
            "Initialized LLM client",
            default_provider=self.default_provider,
            default_model=self.default_model,
            openai_available=bool(self.openai_client),
            anthropic_available=bool(self.anthropic_client)
        )
    
    async def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """
        Generate text using the specified or default LLM provider.
        
        Args:
            prompt: User prompt or question
            system_message: Optional system message
            provider: LLM provider ('openai' or 'anthropic')
            model: Specific model to use
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text response
        """
        provider = provider or self.default_provider
        model = model or self.default_model
        
        try:
            logger.debug(
                "Generating LLM response",
                provider=provider,
                model=model,
                prompt_length=len(prompt),
                temperature=temperature
            )
            
            if provider == "openai" and self.openai_client:
                return await self._generate_openai(
                    prompt=prompt,
                    system_message=system_message,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
            
            elif provider == "anthropic" and self.anthropic_client:
                return await self._generate_anthropic(
                    prompt=prompt,
                    system_message=system_message,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
            
            else:
                raise ValueError(f"Provider '{provider}' not available or not configured")
                
        except Exception as e:
            logger.error("LLM generation failed", provider=provider, error=str(e))
            raise
    
    async def _generate_openai(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """Generate response using OpenAI API."""
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    async def _generate_anthropic(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        model: str = "claude-3-sonnet-20240229",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """Generate response using Anthropic API."""
        # Anthropic handles system messages differently
        full_prompt = prompt
        if system_message:
            full_prompt = f"{system_message}\n\nUser: {prompt}\n\nAssistant:"
        
        response = await self.anthropic_client.completions.create(
            model=model,
            prompt=full_prompt,
            temperature=temperature,
            max_tokens_to_sample=max_tokens,
            **kwargs
        )
        
        return response.completion
    
    async def stream_generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Stream text generation for real-time responses.
        
        Args:
            prompt: User prompt
            system_message: Optional system message
            provider: LLM provider
            model: Specific model
            **kwargs: Additional parameters
            
        Yields:
            Text chunks as they are generated
        """
        provider = provider or self.default_provider
        model = model or self.default_model
        
        try:
            if provider == "openai" and self.openai_client:
                async for chunk in self._stream_openai(
                    prompt=prompt,
                    system_message=system_message,
                    model=model,
                    **kwargs
                ):
                    yield chunk
            
            elif provider == "anthropic" and self.anthropic_client:
                # Anthropic streaming implementation
                response = await self.generate(
                    prompt=prompt,
                    system_message=system_message,
                    provider=provider,
                    model=model,
                    **kwargs
                )
                yield response
            
            else:
                raise ValueError(f"Provider '{provider}' not available")
                
        except Exception as e:
            logger.error("LLM streaming failed", provider=provider, error=str(e))
            yield f"Error: {str(e)}"
    
    async def _stream_openai(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        model: str = "gpt-4-turbo-preview",
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream OpenAI response."""
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        stream = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            **kwargs
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def get_available_providers(self) -> Dict[str, bool]:
        """Get list of available LLM providers."""
        return {
            "openai": bool(self.openai_client),
            "anthropic": bool(self.anthropic_client)
        }