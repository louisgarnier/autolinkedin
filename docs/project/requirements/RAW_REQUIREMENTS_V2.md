# Raw Requirements V2

This document captures the initial, unprocessed requirements for V2 of the LinkedIn Automation project.

## How to Use

1. **Add your requirements below** - Write them as you think of them, in any format
2. **Don't worry about structure** - We'll analyze and rephrase them together
3. **Include context** - Add any relevant background information, constraints, or priorities

---

## Initial Requirements V2

### LinkedIn Post Generation and Automation - V2

**Goal**: Generate LinkedIn posts using AI (OpenAI) based on subjects from Google Sheets, save generated posts, and optionally publish them.

**Data Source - Google Sheets Structure**:
- **Sheet**: Sheet2
- Column A: "sujet" (subject/topic for the post)
- Column B: "post" (generated post content - will be filled by V2)
- Row 1: Header row (sujet, post)
- **Archive Sheet**: Already exists, same structure (sujet, post)

**Process Flow**:

1. **Read Subject from Google Sheets**
   - Always read Row 2 (first data row after header)
   - Extract "sujet" from Column A
   - Logic: Row 1 = header, Row 2 = first subject to process
   - Once a row is processed and archived, Row 2 becomes the next subject automatically

2. **Generate Post with AI**
   - Use the subject from Column A (Row 2)
   - Generate post using OpenAI API with prompt template
   - Save the generated post in Column B of the same row (Row 2)
   - **If Column B is already filled**: Regenerate the post (overwrite existing)
   - set column c "post generated" to "yes"

3. **Archive After Publication** (Phase 2 - after LinkedIn integration)
   - After posting to LinkedIn, move the entire row (Column A + Column B) to Archive sheet
   - Archive sheet already exists with same structure (sujet, post)
   - Archive happens only after successful LinkedIn publication

4. **Row Selection Logic**
   - Always process Row 2 (first data row)
   - After archiving, Row 2 automatically becomes the next subject
   - No need to check multiple rows - always Row 2

**Implementation Phases**:

## Phase 1: Post Generation Only

**Goal**: Generate posts and save them to Google Sheets. NO LinkedIn posting.

**Steps**:
1. Read subject from Sheet2, Row 2, Column A
2. Generate post using OpenAI API with prompt template
3. Save generated post to Sheet2, Row 2, Column B, ROW 2, column C to "yes"
4. Test and validate post quality
5. Allow regeneration if needed (overwrite Column B)

**Deliverables**:
- Working post generation
- Posts saved in Google Sheets Column B
- Validation that posts are of good quality

**Exit Criteria**: 
- Posts are generated correctly
- Posts are saved in Google Sheets
- User validates post quality is acceptable

---

## Phase 2: LinkedIn Integration

**Goal**: Connect to V1 LinkedIn automation and archive after publication.

**Prerequisites**: 
- Phase 1 must be completed and validated
- Post generation quality must be acceptable

**Steps**:
1. Read generated post from Sheet2, Row 2, Column B, column C needs to be equal to "yes"
2. Use V1 LinkedIn automation code to post to LinkedIn
3. After successful publication, archive the row (Column A + Column B + column C) to Archive sheet
4. Archive sheet already exists - just copy the row

**Deliverables**:
- Full integration with V1 LinkedIn automation
- Automatic archiving after publication
- Complete workflow: Generate → Post → Archive

**Exit Criteria**:
- Posts are published to LinkedIn successfully
- Rows are archived correctly after publication
- Full workflow works end-to-end

**Technical Details**:

### Prompt Template
- **Location**: `backend/prompts/post_generation_template.txt`
- **Format**: Same as previous V2 attempt (user confirmed)
- **Placeholder**: Subject from Column A (Row 2) will be injected into prompt

### OpenAI API
- **Model**: `gpt-4` (for better quality, will be tested)
- **API Key**: Stored in `.env` as `OPENAI_API_KEY`

### Google Sheets
- **Service Account**: Same as V1
- **Sheet ID**: Same as V1
- **Sheet Name**: Sheet2
- **Archive Sheet**: Already exists, same structure

---

## Clarifications (Answered)

1. ✅ **Google Sheet**: Sheet2
2. ✅ **Prompt location**: `backend/prompts/post_generation_template.txt`
3. ✅ **Row selection**: Always Row 2 (first data row after header)
4. ✅ **Column B filled**: Regenerate (overwrite existing)
5. ✅ **Archive sheet**: Already exists, same structure. Archive happens in Phase 2 after LinkedIn publication
6. ✅ **OpenAI model**: gpt-4 (for better quality, will be tested)

---

## Notes & Context

- **Critical**: Follow best practices - test each step before moving to next
- **Critical**: Validate post generation quality before LinkedIn integration
- **Workflow**: Generate → Review → Validate → Then integrate LinkedIn
- This is a fresh start from previous V2 attempt
- Focus on quality and control over what gets published

---

**Next Step**: Once requirements are clarified, we'll analyze and rephrase them in `ANALYZED_REQUIREMENTS_V2.md`

