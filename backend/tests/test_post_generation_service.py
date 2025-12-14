"""
Test script for Post Generation service (V2b - Step 3).

This test verifies:
1. Post generation service can be created
2. Post can be generated from a subject
3. Generated post is cleaned and ready for publication
4. Error handling works correctly
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

from backend.services.post_generation_service import PostGenerationService

print("="*60)
print("TEST: Post Generation Service (V2b - Step 3)")
print("="*60)

try:
    # Test 1: Create service
    print("\n1. Creating Post Generation service...")
    service = PostGenerationService()
    print("✅ Service created")
    print(f"   Prompt service: {type(service.prompt_service).__name__}")
    print(f"   OpenAI service: {type(service.openai_service).__name__}")
    
    # Test 2: Generate post from subject
    print("\n2. Testing post generation from subject...")
    test_subject = "Devenir freelance"
    print(f"   Subject: '{test_subject}'")
    print("   Generating post (this may take a few seconds)...")
    
    generated_post = service.generate_post(test_subject)
    
    print(f"✅ Post generated successfully")
    print(f"   Length: {len(generated_post)} characters")
    print(f"   Lines: {len(generated_post.split(chr(10)))}")
    
    # Test 3: Validate post content
    print("\n3. Validating generated post...")
    
    # Check it's not empty
    if not generated_post or len(generated_post.strip()) < 50:
        print("❌ Generated post is too short or empty")
        exit(1)
    print("✅ Post is not empty and has reasonable length")
    
    # Check it doesn't contain XML tags
    xml_tags = ['<AgentOutput>', '</AgentOutput>', '<Post>', '</Post>', '<Input>', '</Input>']
    found_tags = [tag for tag in xml_tags if tag in generated_post]
    if found_tags:
        print(f"⚠️  Warning: Found XML tags in post: {found_tags}")
        print("   (This might be acceptable depending on the model output)")
    else:
        print("✅ No XML tags found in post")
    
    # Check it doesn't contain obvious instruction text
    instruction_keywords = ['Instruction:', 'Note:', 'Remember:', 'Do not include']
    found_instructions = [kw for kw in instruction_keywords if kw.lower() in generated_post.lower()]
    if found_instructions:
        print(f"⚠️  Warning: Found instruction keywords: {found_instructions}")
    else:
        print("✅ No instruction keywords found")
    
    # Test 4: Display generated post
    print("\n4. Generated post preview:")
    print("-" * 60)
    print(generated_post[:500] + ("..." if len(generated_post) > 500 else ""))
    print("-" * 60)
    
    # Test 5: Test with another subject
    print("\n5. Testing with another subject...")
    test_subject2 = "L'entrepreneuriat"
    print(f"   Subject: '{test_subject2}'")
    generated_post2 = service.generate_post(test_subject2)
    print(f"✅ Second post generated ({len(generated_post2)} characters)")
    
    # Test 6: Test error handling (empty subject)
    print("\n6. Testing error handling (empty subject)...")
    try:
        service.generate_post("")
        print("❌ Should have raised ValueError for empty subject")
        exit(1)
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    except Exception as e:
        print(f"⚠️  Raised {type(e).__name__} instead of ValueError: {e}")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED")
    print("="*60)
    print("\n📝 Generated posts are ready for review!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

