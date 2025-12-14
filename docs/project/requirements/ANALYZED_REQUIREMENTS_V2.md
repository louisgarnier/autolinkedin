# Analyzed Requirements V2

This document contains the analyzed, structured, and clarified requirements for V2 of the LinkedIn Automation project.

**Source**: `RAW_REQUIREMENTS_V2.md`

---

## Overview

**Goal**: Generate LinkedIn posts using AI (OpenAI GPT-4) based on subjects from Google Sheets, save generated posts to the same sheet, and optionally publish them to LinkedIn.

**Key Difference from V1**: 
- V1: Reads pre-written posts from Google Sheets and posts them
- V2: Generates posts using AI from subjects, saves them, then posts them

---

## Google Sheets Structure

### Sheet2 (Main Sheet)
- **Row 1**: Header row - "sujet" (Column A), "post" (Column B), "post generated" (Column C)
- **Row 2**: First data row (always the one to process)
- **Column A**: "sujet" - Subject/topic for the post
- **Column B**: "post" - Generated post content (filled by V2)
- **Column C**: "post generated" - Status flag set to "yes" after post generation

**Logic**:
- Always process Row 2 (first data row after header)
- Once a row is processed and archived, Row 2 automatically becomes the next subject
- If Column B is already filled, regenerate the post (overwrite)
- After generation, set Column C to "yes"

### Archive Sheet
- **Structure**: Same as Sheet2 (sujet, post, post generated)
- **Status**: Already exists
- **Usage**: Archive rows after successful LinkedIn publication (Phase 2)
- **Archive includes**: Column A + Column B + Column C

---

## Implementation Phases

### Phase 1: Post Generation Only

**Objective**: Generate posts using AI and save them to Google Sheets. NO LinkedIn posting.

**Functional Requirements**:

1. **Read Subject from Google Sheets**
   - Connect to Sheet2
   - Read Row 2, Column A (sujet)
   - Validate that subject exists

2. **Generate Post with OpenAI**
   - Load prompt template from `backend/prompts/post_generation_template.txt`
   - Inject subject from Column A into prompt template
   - Call OpenAI GPT-4 API to generate post
   - Handle API errors and retries

3. **Save Generated Post**
   - Save generated post to Sheet2, Row 2, Column B
   - Set Column C to "yes" to mark post as generated
   - If Column B already has content, overwrite it (regenerate)

4. **Validation & Testing**
   - Display generated post for review
   - Allow regeneration if quality is not acceptable
   - Test with multiple subjects

**Technical Requirements**:
- OpenAI API integration (GPT-4)
- Prompt template management
- Google Sheets integration (read Column A, write Column B)
- Error handling and logging

**Deliverables**:
- Working post generation service
- Posts saved in Google Sheets Column B
- Test script to validate generation

**Exit Criteria**:
- ✅ Posts are generated correctly from subjects
- ✅ Posts are saved in Google Sheets Column B
- ✅ User validates post quality is acceptable
- ✅ Can regenerate posts if needed

---

### Phase 2: LinkedIn Integration & Archiving

**Objective**: Connect to V1 LinkedIn automation, post generated content, and archive after publication.

**Prerequisites**:
- ✅ Phase 1 must be completed and validated
- ✅ Post generation quality must be acceptable
- ✅ User explicitly approves moving to Phase 2

**Functional Requirements**:

1. **Read Generated Post**
   - Read generated post from Sheet2, Row 2, Column B
   - Validate that Column C = "yes" (post is generated)
   - Only proceed if Column C = "yes"

2. **Post to LinkedIn**
   - Use V1 LinkedIn automation code
   - Post the generated content from Column B
   - Handle LinkedIn errors and retries

3. **Archive After Publication**
   - After successful LinkedIn publication
   - Copy entire row (Column A + Column B + Column C) to Archive sheet
   - Archive sheet already exists - append the row

**Technical Requirements**:
- Integration with V1 LinkedIn automation
- Google Sheets archiving functionality
- Error handling for LinkedIn posting
- Validation that post was published successfully

**Deliverables**:
- Full integration with V1 LinkedIn automation
- Automatic archiving after publication
- Complete workflow: Generate → Post → Archive

**Exit Criteria**:
- ✅ Posts are published to LinkedIn successfully
- ✅ Rows are archived correctly after publication
- ✅ Full workflow works end-to-end
- ✅ User validates complete process

---

## Technical Specifications

### OpenAI API
- **Model**: `gpt-4` (for better quality)
- **API Key**: Stored in `.env` as `OPENAI_API_KEY`
- **Temperature**: TBD (to be tested)
- **Max Tokens**: TBD (to be tested)

### Prompt Template
- **Location**: `backend/prompts/post_generation_template.txt`
- **Format**: Same as previous V2 attempt
- **Placeholder**: Subject from Column A (Row 2) will be injected into prompt
- **Note**: User will provide/confirm the prompt template

### Google Sheets
- **Service Account**: Same as V1
- **Sheet ID**: Same as V1
- **Sheet Name**: Sheet2
- **Archive Sheet**: Already exists, same structure

### Code Structure
- Reuse V1 code where possible (Google Sheets service, LinkedIn automation)
- Extend services for V2 functionality
- Follow best practices and testing workflow

---

## Non-Functional Requirements

### Quality
- Generated posts must be of acceptable quality before Phase 2
- Posts should follow the style and format specified in prompt template
- User must validate post quality before LinkedIn integration

### Workflow
- **Phase 1 first**: Complete and validate post generation before LinkedIn integration
- **User control**: User must explicitly approve moving to Phase 2
- **Testing**: Each phase must be tested and validated before moving to next

### Error Handling
- Handle OpenAI API errors gracefully
- Handle Google Sheets errors gracefully
- Handle LinkedIn posting errors gracefully (Phase 2)
- Log all operations for debugging

### Security
- API keys stored in `.env` file (not in code)
- Credentials not committed to Git

---

## Constraints

1. **Two-Phase Approach**: Must complete Phase 1 before Phase 2
2. **Row Selection**: Always Row 2 (no complex row selection logic)
3. **Regeneration**: If Column B is filled, regenerate (overwrite)
4. **Archive Timing**: Archive only after successful LinkedIn publication (Phase 2)

---

## Open Questions / To Be Decided

1. **OpenAI Parameters**: 
   - Temperature value? (to be tested)
   - Max tokens? (to be tested)

2. **Prompt Template**: 
   - User will provide/confirm the exact prompt template
   - May need adjustments based on GPT-4 behavior

3. **Error Recovery**:
   - What happens if OpenAI API fails?
   - What happens if Google Sheets write fails?
   - Retry logic?

---

## Next Steps

1. ✅ Requirements captured and analyzed
2. ⏳ Create feature specification document (`LINKEDIN_AUTOMATION_V2.md`)
3. ⏳ User provides/confirms prompt template
4. ⏳ Start Phase 1 implementation

---

**Status**: Requirements analyzed and ready for feature specification

