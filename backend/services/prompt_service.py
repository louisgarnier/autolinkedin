"""
Prompt template management for LinkedIn Automation V2b.

This module handles reading and processing prompt templates.
"""

import logging
from pathlib import Path
from typing import Optional
import re

logger = logging.getLogger(__name__)


class PromptService:
    """Service for managing prompt templates."""
    
    def __init__(self, template_path: Optional[str] = None):
        """
        Initialize prompt service.
        
        Args:
            template_path: Path to prompt template file. If None, uses default location.
        """
        if template_path is None:
            # Default location: backend/prompts/post_generation_template.txt
            base_dir = Path(__file__).parent.parent
            template_path = base_dir / "prompts" / "post_generation_template.txt"
        
        self.template_path = Path(template_path)
        
        if not self.template_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {self.template_path}")
        
        logger.info(f"Prompt template path: {self.template_path}")
    
    def load_template(self) -> str:
        """
        Load prompt template from file.
        
        Returns:
            Template content as string
            
        Raises:
            FileNotFoundError: If template file doesn't exist
            IOError: If file cannot be read
        """
        try:
            logger.info(f"Loading prompt template from: {self.template_path}")
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            
            logger.info(f"✅ Template loaded ({len(template)} characters)")
            return template
            
        except FileNotFoundError:
            logger.error(f"❌ Template file not found: {self.template_path}")
            raise
        except Exception as e:
            logger.error(f"❌ Error loading template: {e}")
            raise
    
    def inject_subject(self, template: str, subject: str) -> str:
        """
        Inject subject into template by replacing content between <UserInput> tags.
        Only replaces the <UserInput> in the <Input> section, NOT in <Examples>.
        
        Args:
            template: Template content
            subject: Subject to inject
            
        Returns:
            Template with subject injected
        """
        try:
            logger.info(f"Injecting subject into template...")
            logger.debug(f"Subject: {subject[:50]}...")
            
            # Find the <Input> section (first occurrence, before <Examples>)
            input_start = template.find("<Input>")
            if input_start == -1:
                raise ValueError("Could not find <Input> section in template")
            
            # Find the closing </Input> tag
            input_end_tag = template.find("</Input>", input_start)
            if input_end_tag == -1:
                raise ValueError("Could not find </Input> tag in template")
            
            # Extract the Input section
            input_section = template[input_start:input_end_tag + len("</Input>")]
            
            # Find <UserInput> within the Input section only
            userinput_start = input_section.find("<UserInput>")
            if userinput_start == -1:
                raise ValueError("Could not find <UserInput> tag within <Input> section")
            
            userinput_end = input_section.find("</UserInput>", userinput_start)
            if userinput_end == -1:
                raise ValueError("Could not find </UserInput> tag within <Input> section")
            
            # Replace content between <UserInput> tags
            # Keep: everything before <UserInput>, the tag itself, new subject, closing tag, everything after
            new_input_section = (
                input_section[:userinput_start + len("<UserInput>")] +
                subject +
                input_section[userinput_end:]
            )
            
            # Reconstruct the full template
            prompt = template[:input_start] + new_input_section + template[input_end_tag + len("</Input>"):]
            
            logger.info(f"✅ Subject injected successfully")
            logger.debug(f"Prompt length: {len(prompt)} characters")
            
            return prompt
            
        except Exception as e:
            logger.error(f"❌ Error injecting subject: {e}")
            raise
    
    def get_prompt_with_subject(self, subject: str) -> str:
        """
        Load template and inject subject in one call.
        
        Args:
            subject: Subject to inject into template
            
        Returns:
            Complete prompt with subject injected
        """
        template = self.load_template()
        return self.inject_subject(template, subject)


def create_prompt_service(template_path: Optional[str] = None) -> PromptService:
    """
    Factory function to create PromptService.
    
    Args:
        template_path: Optional path to template file
        
    Returns:
        PromptService instance
    """
    return PromptService(template_path=template_path)

