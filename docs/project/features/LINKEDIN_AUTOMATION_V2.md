# LinkedIn Post Generation & Automation - V2

**Brief description**: Generate LinkedIn posts using AI (OpenAI GPT-4) from subjects in Google Sheets, save generated posts, and optionally publish them to LinkedIn.

## Requirements

### Functional Requirements

#### Phase 1: Post Generation Only
- [ ] Read subject from Sheet2, Row 2, Column A
- [ ] Generate post using OpenAI GPT-4 API with prompt template
- [ ] Save generated post to Sheet2, Row 2, Column B
- [ ] Set Column C "post generated" to "yes" after generation
- [ ] Allow regeneration (overwrite Column B if already filled)
- [ ] Display generated post for review
- [ ] Test and validate post quality

#### Phase 2: LinkedIn Integration & Archiving
- [ ] Read generated post from Sheet2, Row 2, Column B
- [ ] Validate Column C = "yes" before posting
- [ ] Post to LinkedIn using V1 automation code
- [ ] Archive row (A + B + C) to Archive sheet after successful publication

### Non-Functional Requirements
- [ ] Secure API key storage (environment variables)
- [ ] Error handling and recovery
- [ ] Clear logging output
- [ ] Two-phase approach (Phase 1 must be validated before Phase 2)
- [ ] User control over when to move to Phase 2

## User Stories

### Phase 1
- As a user, I want to generate LinkedIn posts from subjects in Google Sheets
- So that I can create content automatically using AI
- I want to review generated posts before they are published
- So that I can ensure quality and control what gets posted

### Phase 2
- As a user, I want to publish generated posts to LinkedIn automatically
- So that I can automate my social media presence
- I want posts to be archived after publication
- So that I can track what has been posted

## Technical Specifications

### Google Sheets Structure

**Sheet2**:
- Row 1: Header - "sujet" (A), "post" (B), "post generated" (C)
- Row 2: First data row (always processed)
- Column A: Subject/topic for post generation
- Column B: Generated post content (filled by V2)
- Column C: Status flag ("yes" when post is generated)

**Archive Sheet**:
- Same structure as Sheet2
- Already exists
- Used to archive rows after LinkedIn publication
- Archive includes: Column A + Column B + Column C

### Backend

#### New/Modified Modules

**Phase 1**:
- **`backend/services/openai_service.py`** - OpenAI GPT-4 API integration
  - Initialize OpenAI client with GPT-4
  - Generate posts from prompts
  - Handle API errors and retries
  
- **`backend/services/prompt_service.py`** - Prompt template management
  - Load prompt template from file
  - Inject subject into template placeholder
  - Handle template parsing

- **`backend/services/post_generation_service.py`** - Post generation orchestration
  - Combine prompt service + OpenAI service
  - Generate post from subject
  - Return generated post text

- **`backend/services/google_sheets_v2.py`** - Extended Google Sheets service
  - Read subject from Sheet2, Row 2, Column A
  - Write generated post to Sheet2, Row 2, Column B
  - Set Column C to "yes" after generation
  - Handle regeneration (overwrite)

**Phase 2**:
- **`backend/services/google_sheets_v2.py`** - Extended for Phase 2
  - Read post from Column B (validate Column C = "yes")
  - Archive row (A + B + C) to Archive sheet
  
- **`backend/main_v2_phase1.py`** - Phase 1 main application
  - Generate post only (no LinkedIn)
  
- **`backend/main_v2_phase2.py`** - Phase 2 main application
  - Read generated post
  - Post to LinkedIn (reuse V1 code)
  - Archive after publication

#### Dependencies
- `openai>=1.0.0` - OpenAI API client
- `gspread>=5.12.0` - Google Sheets API (existing)
- `google-auth>=2.23.0` - Google authentication (existing)
- `playwright>=1.40.0` - Browser automation (existing, Phase 2)
- `python-dotenv>=1.0.0` - Environment variables (existing)

#### Configuration Files
- `.env` - OpenAI API key: `OPENAI_API_KEY`
- `backend/prompts/post_generation_template.txt` - Prompt template (user will provide)

## Testing Requirements

### Phase 1 Tests
- [ ] Unit tests for OpenAI service
- [ ] Unit tests for prompt service
- [ ] Unit tests for post generation service
- [ ] Integration test: Generate post and save to Google Sheets
- [ ] Test script to preview generated posts
- [ ] Test regeneration (overwrite Column B)

### Phase 2 Tests
- [ ] Integration test: Read generated post and validate Column C
- [ ] Integration test: Post to LinkedIn
- [ ] Integration test: Archive after publication
- [ ] End-to-end test: Full workflow

## Acceptance Criteria

### Phase 1
- [ ] System reads subject from Sheet2, Row 2, Column A
- [ ] System generates post using OpenAI GPT-4
- [ ] Generated post is saved to Sheet2, Row 2, Column B
- [ ] Column C is set to "yes" after generation
- [ ] System allows regeneration (overwrites Column B)
- [ ] Generated posts are of acceptable quality
- [ ] User can review posts before Phase 2

### Phase 2
- [ ] System validates Column C = "yes" before posting
- [ ] System posts generated content to LinkedIn successfully
- [ ] System archives row (A + B + C) after successful publication
- [ ] Full workflow works end-to-end

## Implementation Plan

### ⚠️ CRITICAL WORKFLOW RULES

**Before checking [x] in any step:**
1. Code must be created ✅
2. Test script (`.py` file) must be created ✅
3. Test script must be executed and show successful results ✅
4. User must confirm the step is complete ✅

**NEVER check [x] just after creating code - ALWAYS wait for test validation!**

**Two-Phase Approach**:
- Phase 1 must be completed and validated before starting Phase 2
- User must explicitly approve moving to Phase 2

---

## Phase 1: Post Generation Only

### Step 1: OpenAI API Integration
**Description**: Set up OpenAI GPT-4 API client

**Tasks**:
- [x] Add `openai` to `requirements.txt`
- [x] Create `backend/services/openai_service.py`
- [x] Implement GPT-4 client initialization
- [x] Add API key to `.env` template
- [x] Test API connection
- [x] Handle API errors and rate limits

**Dependencies**: None

**Deliverables**:
- `backend/services/openai_service.py`
- Updated `requirements.txt`
- Updated `.env` template

**Estimated Time**: 2-3 hours

---

### Step 2: Prompt Template Management
**Description**: Create system to read and process prompt template

**Tasks**:
- [x] Create `backend/prompts/` directory
- [x] Create `post_generation_template.txt` file (user provides content)
- [x] Implement prompt template reader
- [x] Implement placeholder replacement logic (inject subject)
- [x] Test template reading and replacement

**Dependencies**: None

**Deliverables**:
- `backend/prompts/post_generation_template.txt`
- `backend/services/prompt_service.py`

**Estimated Time**: 1-2 hours

---

### Step 3: Post Generation Service
**Description**: Create service to generate posts using OpenAI

**Tasks**:
- [x] Create `backend/services/post_generation_service.py`
- [x] Integrate prompt service + OpenAI service
- [x] Implement post generation from subject
- [x] Handle response parsing
- [x] Add error handling and retries
- [x] Test post generation with sample subjects

**Dependencies**: 
- Step 1 must be completed (OpenAI Integration)
- Step 2 must be completed (Prompt Template)

**Deliverables**:
- `backend/services/post_generation_service.py`
- Post generation functionality

**Estimated Time**: 2-3 hours

---

### Step 4: Google Sheets V2 Integration
**Description**: Extend Google Sheets service for V2 (read subject, write post, set status)

**Tasks**:
- [x] Extend `GoogleSheetsService` to access Sheet2
- [x] Implement method to read Row 2, Column A (sujet)
- [x] Implement method to write Row 2, Column B (post)
- [x] Implement method to set Row 2, Column C to "yes"
- [x] Handle regeneration (overwrite Column B)
- [x] Test reading and writing to Sheet2

**Dependencies**: Step 2 from V1 (Google Sheets Integration)

**Deliverables**:
- Extended `GoogleSheetsService` class
- Sheet2 reading/writing functionality

**Estimated Time**: 2-3 hours

---

### Step 5: Phase 1 Main Application
**Description**: Create main application for Phase 1 (generation only)

**Tasks**:
- [x] Create `backend/main_v2_phase1.py` entry point
- [x] Integrate Sheet2 reading (Row 2, Column A)
- [x] Integrate post generation
- [x] Integrate Sheet2 writing (Row 2, Column B)
- [x] Set Column C to "yes"
- [x] Add comprehensive logging
- [x] Display generated post for review
- [x] Handle errors gracefully
- [x] Test full Phase 1 flow

**Dependencies**: 
- All previous Phase 1 steps must be completed

**Deliverables**:
- `backend/main_v2_phase1.py`
- Complete Phase 1 integration

**Estimated Time**: 3-4 hours

---

### Step 6: Phase 1 Testing & Validation
**Description**: Test Phase 1 and validate post quality

**Tasks**:
- [ ] Create test script for Phase 1
- [ ] Test with multiple subjects
- [ ] Validate post quality
- [ ] Test regeneration functionality
- [ ] User reviews and validates posts
- [ ] Document any issues or improvements needed

**Dependencies**: Step 5 must be completed

**Deliverables**:
- Test suite for Phase 1
- Validated post quality
- User approval to proceed to Phase 2

**Estimated Time**: 2-3 hours

---

## Phase 2: LinkedIn Integration & Archiving

**⚠️ PREREQUISITE**: Phase 1 must be completed and validated. User must explicitly approve moving to Phase 2.

---

### Step 7: Google Sheets V2 - Phase 2 Extensions
**Description**: Extend Google Sheets service for Phase 2 (read post, validate status, archive)

**Tasks**:
- [ ] Implement method to read Row 2, Column B (post)
- [ ] Implement method to validate Column C = "yes"
- [ ] Implement method to archive row (A + B + C) to Archive sheet
- [ ] Test archiving functionality

**Dependencies**: 
- Phase 1 must be completed
- Step 4 from Phase 1

**Deliverables**:
- Extended `GoogleSheetsService` for Phase 2
- Archive functionality

**Estimated Time**: 2-3 hours

---

### Step 8: Phase 2 Main Application
**Description**: Create main application for Phase 2 (LinkedIn posting + archiving)

**Tasks**:
- [ ] Create `backend/main_v2_phase2.py` entry point
- [ ] Read generated post from Sheet2, Row 2, Column B
- [ ] Validate Column C = "yes"
- [ ] Integrate V1 LinkedIn automation
- [ ] Post generated content to LinkedIn
- [ ] Archive row (A + B + C) after successful publication
- [ ] Add comprehensive logging
- [ ] Handle errors gracefully
- [ ] Test full Phase 2 flow

**Dependencies**: 
- Step 7 must be completed
- V1 LinkedIn automation must be available

**Deliverables**:
- `backend/main_v2_phase2.py`
- Complete Phase 2 integration

**Estimated Time**: 4-5 hours

---

### Step 9: Phase 2 Testing & Documentation
**Description**: Test Phase 2 and document complete workflow

**Tasks**:
- [ ] Create test script for Phase 2
- [ ] Test full workflow: Generate → Post → Archive
- [ ] Validate archiving works correctly
- [ ] Update documentation
- [ ] Create user guide

**Dependencies**: Step 8 must be completed

**Deliverables**:
- Test suite for Phase 2
- Updated documentation
- Complete V2 workflow validated

**Estimated Time**: 2-3 hours

---

## Implementation Steps Overview

### Phase 1: Post Generation Only
- [x] **Step 1**: OpenAI API Integration (2-3 hours) - ✅ COMPLETED
- [x] **Step 2**: Prompt Template Management (1-2 hours) - ✅ COMPLETED
- [x] **Step 3**: Post Generation Service (2-3 hours) - ✅ COMPLETED
- [x] **Step 4**: Google Sheets V2 Integration (2-3 hours) - ✅ COMPLETED
- [x] **Step 5**: Phase 1 Main Application (3-4 hours) - ✅ COMPLETED
- [ ] **Step 6**: Phase 1 Testing & Validation (2-3 hours)

**Phase 1 Total Estimated Time**: 12-18 hours

### Phase 2: LinkedIn Integration & Archiving
- [ ] **Step 7**: Google Sheets V2 - Phase 2 Extensions (2-3 hours)
- [ ] **Step 8**: Phase 2 Main Application (4-5 hours)
- [ ] **Step 9**: Phase 2 Testing & Documentation (2-3 hours)

**Phase 2 Total Estimated Time**: 8-11 hours

**Total Estimated Time**: 20-29 hours

---

## Notes

### Google Sheets Structure V2

**Sheet2 (Main)**:
- Row 1: Headers - "sujet", "post", "post generated"
- Column A: sujet
- Column B: post (generated)
- Column C: post generated ("yes" when generated)
- Always process Row 2

**Archive Sheet**:
- Same structure as Sheet2
- Row 1: Headers - "sujet", "post", "post generated"
- Archive includes: Column A + Column B + Column C
- Already exists

### Prompt Template Format

The prompt template should contain a placeholder for the subject:
- **Location**: `backend/prompts/post_generation_template.txt`
- **Placeholder**: Subject from Column A (Row 2) will be injected
- **Format**: Same as previous V2 attempt (user confirmed)
- **Status**: User will provide the prompt template content

### OpenAI Configuration

- **Model**: `gpt-4` (for better quality)
- **API Key**: `OPENAI_API_KEY` in `.env`
- **Parameters**: Temperature and max_tokens to be tested

---

**Status**: Ready for implementation - Phase 1
