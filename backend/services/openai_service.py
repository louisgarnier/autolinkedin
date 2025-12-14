"""
OpenAI API service for LinkedIn Automation V2.

This module handles OpenAI GPT-4 API calls for post generation.
"""

import os
import logging
from typing import Optional
from openai import OpenAI

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI service.
        
        Args:
            api_key: OpenAI API key. If None, will be loaded from environment.
        """
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"  # Using GPT-4 for better quality
        logger.info("OpenAI service initialized with GPT-4")
    
    def generate_post(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.9) -> str:
        """
        Generate a LinkedIn post using OpenAI GPT-4.
        
        Args:
            prompt: The full prompt with subject injected
            max_tokens: Maximum tokens for response (default: 2000)
            temperature: Temperature for creativity (default: 0.9)
            
        Returns:
            Generated post text
            
        Raises:
            Exception: If API call fails
        """
        try:
            logger.info("Calling OpenAI GPT-4 API to generate post...")
            logger.debug(f"Model: {self.model}")
            logger.debug(f"Max tokens: {max_tokens}")
            logger.debug(f"Temperature: {temperature}")
            
            # Use system message to guide the model
            system_message = "You are an elite LinkedIn copywriter. Generate original, unique posts based on the subject provided. Do NOT copy the examples - they are only for style reference."
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            generated_text = response.choices[0].message.content.strip()
            logger.info(f"✅ Post generated successfully ({len(generated_text)} characters)")
            logger.debug(f"Generated text preview: {generated_text[:100]}...")
            
            return generated_text
            
        except Exception as e:
            logger.error(f"❌ Error generating post with OpenAI: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test OpenAI API connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            logger.info("Testing OpenAI GPT-4 API connection...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": "Say 'Hello' if you can read this."}
                ],
                max_tokens=10,
            )
            
            result = response.choices[0].message.content.strip()
            logger.info(f"✅ OpenAI API connection successful. Response: {result}")
            return True
            
        except Exception as e:
            logger.error(f"❌ OpenAI API connection failed: {e}")
            return False


def create_openai_service() -> OpenAIService:
    """
    Factory function to create OpenAIService from environment variables.
    
    Returns:
        OpenAIService instance
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    return OpenAIService(api_key=api_key)

