"""
Test script for OpenAI service (V2b - Step 1).

This test verifies:
1. OpenAI service can be created
2. API connection works
3. Post generation works with GPT-4
"""

import sys
from pathlib import Path
import logging
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

logging.basicConfig(level=logging.INFO)

from backend.services.openai_service import OpenAIService, create_openai_service

print("="*60)
print("TEST: OpenAI Service (V2b - Step 1)")
print("="*60)

try:
    # Test 1: Create service
    print("\n1. Creating OpenAI service...")
    service = create_openai_service()
    print("✅ Service created")
    print(f"   Model: {service.model}")
    
    # Test 2: Test connection
    print("\n2. Testing API connection...")
    if service.test_connection():
        print("✅ Connection successful")
    else:
        print("❌ Connection failed")
        exit(1)
    
    # Test 3: Generate a simple post
    print("\n3. Testing post generation...")
    test_prompt = "Generate a short LinkedIn post (50 words max) about: 'Devenir freelance'"
    generated = service.generate_post(test_prompt, max_tokens=200)
    print(f"✅ Post generated successfully")
    print(f"\nGenerated post ({len(generated)} characters):")
    print("-" * 60)
    print(generated)
    print("-" * 60)
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

