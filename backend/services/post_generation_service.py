"""
Post generation service for LinkedIn Automation V2b.

This module orchestrates post generation by combining prompt service and OpenAI service.
"""

import logging
from typing import Optional
import time

from backend.services.prompt_service import PromptService
from backend.services.openai_service import OpenAIService

logger = logging.getLogger(__name__)


class PostGenerationService:
    """Service for generating LinkedIn posts from subjects."""
    
    def __init__(
        self,
        prompt_service: Optional[PromptService] = None,
        openai_service: Optional[OpenAIService] = None,
        max_retries: int = 3,
        retry_delay: float = 2.0
    ):
        """
        Initialize post generation service.
        
        Args:
            prompt_service: PromptService instance. If None, creates a new one.
            openai_service: OpenAIService instance. If None, creates a new one.
            max_retries: Maximum number of retries on failure
            retry_delay: Delay between retries (seconds)
        """
        self.prompt_service = prompt_service or PromptService()
        self.openai_service = openai_service or OpenAIService()
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        logger.info("Post generation service initialized")
    
    def generate_post(self, subject: str, max_tokens: int = 1000) -> str:
        """
        Generate a LinkedIn post from a subject.
        
        Args:
            subject: Subject/topic for the post
            max_tokens: Maximum tokens for OpenAI response
            
        Returns:
            Generated post text (cleaned and ready to publish)
            
        Raises:
            ValueError: If subject is empty
            Exception: If generation fails after retries
        """
        if not subject or not subject.strip():
            raise ValueError("Subject cannot be empty")
        
        logger.info(f"Generating post for subject: {subject[:50]}...")
        
        # Retry logic
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                # Step 1: Load template and inject subject
                logger.debug(f"Attempt {attempt}/{self.max_retries}: Loading template and injecting subject...")
                prompt = self.prompt_service.get_prompt_with_subject(subject)
                
                # Step 2: Generate post using OpenAI
                logger.debug(f"Attempt {attempt}/{self.max_retries}: Calling OpenAI API...")
                generated_text = self.openai_service.generate_post(prompt, max_tokens=max_tokens)
                
                # Step 3: Clean and parse response
                logger.debug(f"Attempt {attempt}/{self.max_retries}: Cleaning response...")
                cleaned_post = self._clean_post(generated_text)
                
                logger.info(f"✅ Post generated successfully ({len(cleaned_post)} characters)")
                logger.debug(f"Generated post preview: {cleaned_post[:100]}...")
                
                return cleaned_post
                
            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt}/{self.max_retries} failed: {e}")
                
                if attempt < self.max_retries:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"❌ All {self.max_retries} attempts failed")
                    raise
        
        # Should never reach here, but just in case
        if last_error:
            raise last_error
        raise Exception("Post generation failed for unknown reason")
    
    def _clean_post(self, text: str) -> str:
        """
        Clean and parse the generated post text.
        
        Removes:
        - XML tags (if any)
        - Extra whitespace
        - Instructions or explanations
        - Leading/trailing metadata
        
        Args:
            text: Raw generated text from OpenAI
            
        Returns:
            Cleaned post text ready for publication
        """
        cleaned = text.strip()
        
        # Remove common XML tags that might appear
        xml_tags = ['<AgentOutput>', '</AgentOutput>', '<Post>', '</Post>', '<Output>', '</Output>']
        for tag in xml_tags:
            cleaned = cleaned.replace(tag, '')
        
        # Remove any remaining XML-like structures (basic cleanup)
        # This is a simple approach - more sophisticated parsing could be added if needed
        if cleaned.startswith('<') and '>' in cleaned:
            # Try to remove opening tag
            first_close = cleaned.find('>')
            if first_close != -1:
                cleaned = cleaned[first_close + 1:].strip()
        
        if cleaned.endswith('</') and '<' in cleaned:
            # Try to remove closing tag
            last_open = cleaned.rfind('<')
            if last_open != -1:
                cleaned = cleaned[:last_open].strip()
        
        # Normalize whitespace (multiple newlines to double newline max)
        lines = cleaned.split('\n')
        normalized_lines = []
        prev_empty = False
        for line in lines:
            is_empty = not line.strip()
            if is_empty and prev_empty:
                continue  # Skip consecutive empty lines
            normalized_lines.append(line)
            prev_empty = is_empty
        
        cleaned = '\n'.join(normalized_lines)
        
        # Final strip
        cleaned = cleaned.strip()
        
        logger.debug(f"Cleaned post: {len(cleaned)} characters (was {len(text)} characters)")
        
        return cleaned


def create_post_generation_service(
    prompt_service: Optional[PromptService] = None,
    openai_service: Optional[OpenAIService] = None
) -> PostGenerationService:
    """
    Factory function to create PostGenerationService.
    
    Args:
        prompt_service: Optional PromptService instance
        openai_service: Optional OpenAIService instance
        
    Returns:
        PostGenerationService instance
    """
    return PostGenerationService(
        prompt_service=prompt_service,
        openai_service=openai_service
    )

