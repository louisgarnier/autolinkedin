"""
Test script for Prompt service (V2b - Step 2).

This test verifies:
1. Prompt service can be created
2. Template can be loaded from file
3. Subject can be injected into template
4. Only Input section is modified, not Examples
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

from backend.services.prompt_service import PromptService

print("="*60)
print("TEST: Prompt Service (V2b - Step 2)")
print("="*60)

try:
    # Test 1: Create service
    print("\n1. Creating Prompt service...")
    service = PromptService()
    print("✅ Service created")
    print(f"   Template path: {service.template_path}")
    
    # Test 2: Load template
    print("\n2. Loading template...")
    template = service.load_template()
    print(f"✅ Template loaded ({len(template)} characters)")
    
    # Test 3: Check placeholder exists
    print("\n3. Checking placeholder in <Input> section...")
    if "<Input>" in template and "<UserInput>" in template:
        print("✅ Found <Input> and <UserInput> tags in template")
    else:
        print("❌ Placeholder not found")
        exit(1)
    
    # Test 4: Check examples are present
    print("\n4. Checking examples section...")
    if "<Examples>" in template:
        print("✅ Examples section found")
        # Count UserInput in Examples
        examples_section = template.split("<Examples>")[1].split("</Examples>")[0] if "</Examples>" in template else ""
        example_count = examples_section.count("<UserInput>")
        print(f"   Found {example_count} <UserInput> tags in Examples section")
    else:
        print("⚠️  No Examples section found")
    
    # Test 5: Inject subject
    print("\n5. Testing subject injection...")
    test_subject = "Test sujet pour vérifier l'injection"
    prompt = service.inject_subject(template, test_subject)
    
    # Verify subject is in Input section
    input_start = prompt.find("<Input>")
    input_end = prompt.find("</Input>", input_start)
    if input_start != -1 and input_end != -1:
        input_section = prompt[input_start:input_end]
        print(f"   Input section preview: {input_section[:200]}...")
        print(f"   Looking for: '{test_subject}'")
        
        # Check if subject is between <UserInput> tags in Input section
        userinput_start = input_section.find("<UserInput>")
        userinput_end = input_section.find("</UserInput>", userinput_start)
        if userinput_start != -1 and userinput_end != -1:
            userinput_content = input_section[userinput_start + len("<UserInput>"):userinput_end]
            print(f"   DEBUG: Content between <UserInput> tags: '{userinput_content}'")
            if test_subject == userinput_content.strip():
                print(f"✅ Subject injected successfully in <Input> section")
            else:
                print(f"❌ Subject mismatch. Expected: '{test_subject}', Got: '{userinput_content.strip()}'")
                exit(1)
        else:
            print("❌ Could not find <UserInput> tags in Input section")
            exit(1)
    else:
        print("❌ Could not find <Input> section in prompt")
        exit(1)
    
    # Verify examples are NOT modified
    if "<Examples>" in template:
        original_examples = template.split("<Examples>")[1].split("</Examples>")[0] if "</Examples>" in template else ""
        new_examples = prompt.split("<Examples>")[1].split("</Examples>")[0] if "</Examples>" in prompt else ""
        if original_examples == new_examples:
            print("✅ Examples section not modified (correct)")
        else:
            print("❌ Examples section was modified (incorrect)")
            exit(1)
    
    # Test 6: Get prompt with subject (one call)
    print("\n6. Testing get_prompt_with_subject...")
    test_subject2 = "Devenir freelance"
    prompt2 = service.get_prompt_with_subject(test_subject2)
    
    # Verify subject is in Input section
    input_start2 = prompt2.find("<Input>")
    input_end2 = prompt2.find("</Input>", input_start2)
    if input_start2 != -1 and input_end2 != -1:
        input_section2 = prompt2[input_start2:input_end2]
        userinput_start2 = input_section2.find("<UserInput>")
        userinput_end2 = input_section2.find("</UserInput>", userinput_start2)
        if userinput_start2 != -1 and userinput_end2 != -1:
            userinput_content2 = input_section2[userinput_start2 + len("<UserInput>"):userinput_end2]
            if test_subject2 == userinput_content2.strip():
                print("✅ get_prompt_with_subject works correctly")
            else:
                print(f"❌ get_prompt_with_subject failed. Expected: '{test_subject2}', Got: '{userinput_content2.strip()}'")
                exit(1)
        else:
            print("❌ Could not find <UserInput> tags in Input section")
            exit(1)
    else:
        print("❌ Could not find <Input> section in prompt")
        exit(1)
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

