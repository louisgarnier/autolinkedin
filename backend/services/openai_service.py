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
        # Use GPT-4 (can be changed to gpt-4-turbo or gpt-4o if available)
        # Note: gpt-4-turbo-preview may not be available, using stable gpt-4
        self.model = "gpt-4"  # Stable and reliable
        logger.info(f"OpenAI service initialized with {self.model}")
    
    def generate_post(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7) -> str:
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
            
            # Use system message to guide the model with strict formatting rules
            system_message = """You are an elite LinkedIn copywriter specialized in French content. Generate original, unique posts in FRENCH based on the subject provided. Do NOT copy the examples - they are only for style reference.

LANGUAGE: You MUST write in FRENCH. All posts must be in French language.

CRITICAL FORMATTING RULES - MUST FOLLOW STRICTLY:
- ULTRA-SHORT SENTENCES: MAXIMUM 10-12 WORDS PER SENTENCE (not 15-20, but 10-12 MAX). One idea per sentence. If you have two ideas, make two sentences.
- NO COMPLEX SENTENCES: No "and", "but", "because", "who", "that" that lengthen sentences. No relative clauses. Make separate sentences instead.
- ULTRA-SHORT PARAGRAPHS: MAXIMUM 2 LINES PER PARAGRAPH (not 3, but 2 MAX). Line break after every 1-2 sentences. NO text blocks.
- SIMPLE WORDS: Use common, everyday words. Avoid complex or technical terms.
- ACTIVE VOICE: Always use active voice ("I did" not "It was done by me").
- NO FILLER WORDS: Remove unnecessary words. Be direct and concise. No "indeed", "furthermore", "after years of experience" - go straight to the point.
- BE DIVISIVE: The post must create debate, provoke thought, take a clear stance. Don't be consensual. Dare to make strong statements that may divide opinions. Being divisive generates engagement and discussions.

CRITICAL ACCURACY RULE - ABSOLUTE PRIORITY:
- FACTUAL ACCURACY: All factual, technical, legal, fiscal information MUST be TRUE and ACCURATE. Being divisive does NOT mean saying false things. You can take a strong stance, but ONLY with verified facts. If you're unsure about technical/legal/fiscal information, use cautious formulations ("maybe", "often", "generally") or avoid the claim. NEVER invent or oversimplify complex information.

The prompt contains detailed formatting instructions - follow them STRICTLY."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,  # 0.7 for better instruction following and accuracy
                top_p=0.95,  # Nucleus sampling - helps with coherence (ChatGPT default)
                frequency_penalty=0.1,  # Reduces repetition (ChatGPT uses similar)
                presence_penalty=0.1,  # Encourages topic diversity
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

