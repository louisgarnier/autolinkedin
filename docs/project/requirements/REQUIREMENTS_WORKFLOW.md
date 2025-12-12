# Requirements Analysis Workflow

This guide explains how to go from raw requirements to implemented functionalities.

## Workflow Overview

```
Raw Requirements → Analysis → Functionalities → Implementation Steps → Code
```

## Step-by-Step Process

### Step 1: Capture Raw Requirements

**File**: `RAW_REQUIREMENTS.md`

- Add requirements in any format
- Don't worry about structure or clarity
- Include context, constraints, and priorities
- Can be updated iteratively

**Example**:
```markdown
- Users should be able to login
- Need to store user data somewhere
- Should be secure
```

### Step 2: Analyze & Rephrase Requirements

**File**: `ANALYZED_REQUIREMENTS.md`

**With AI assistance**, we will:
1. **Clarify** - Remove ambiguity, add specifics
   - ❌ "Users should be able to login"
   - ✅ "Users must authenticate using email/password. System must validate credentials against database and return JWT token."

2. **Categorize** - Group related requirements
   - Authentication requirements
   - Data storage requirements
   - Security requirements

3. **Prioritize** - Identify must-haves vs. nice-to-haves
   - Priority 1: Core authentication
   - Priority 2: Password reset
   - Priority 3: Social login

4. **Identify Functionalities** - Break into logical features
   - User Authentication
   - User Management
   - Security & Authorization

### Step 3: Create Functionality Files

**Directory**: `../features/`

For each identified functionality:
1. Create a new file: `[FUNCTIONALITY_NAME].md`
2. Use the template from `TEMPLATE.md` as a starting point
3. Link back to analyzed requirements

**Example**: `features/USER_AUTHENTICATION.md`

### Step 4: Break Down into Steps

Within each functionality file, create an **Implementation Plan** section with:

1. **High-level steps** - Major phases
2. **Detailed tasks** - Specific actions
3. **Dependencies** - What needs to be done first
4. **Acceptance criteria** - How to verify completion

**Example Structure**:
```markdown
## Implementation Plan

### Step 1: Database Schema
- Tasks:
  - [ ] Create users table
  - [ ] Add email, password_hash columns
  - [ ] Create migration script
- Dependencies: None
- Acceptance: Users table exists with correct schema

### Step 2: Authentication API
- Tasks:
  - [ ] Create POST /api/auth/login endpoint
  - [ ] Implement password verification
  - [ ] Generate JWT tokens
- Dependencies: Step 1
- Acceptance: Can authenticate and receive token
```

### Step 5: Implementation

Once steps are defined:
1. Review with user
2. Get approval per `BEST_PRACTICES.md`
3. Implement code
4. Create tests
5. Verify against acceptance criteria

## Best Practices

### Requirements Analysis
- ✅ Ask clarifying questions
- ✅ Identify edge cases
- ✅ Consider non-functional requirements
- ✅ Document assumptions
- ❌ Don't assume - clarify

### Functionality Breakdown
- ✅ Keep functionalities focused (single responsibility)
- ✅ Make steps actionable
- ✅ Identify dependencies clearly
- ✅ Include acceptance criteria
- ❌ Don't create overly large functionalities

### Step Definition
- ✅ Steps should be completable in 1-2 days
- ✅ Each step should have clear deliverables
- ✅ Include testing in steps
- ✅ Document dependencies
- ❌ Don't create vague or too-large steps

## Quick Reference

| Stage | File/Directory | Purpose |
|-------|---------------|---------|
| Input | `RAW_REQUIREMENTS.md` | Initial requirements capture |
| Analysis | `ANALYZED_REQUIREMENTS.md` | Rephrased, structured requirements |
| Breakdown | `../features/[NAME].md` | Individual functionality with steps |
| Implementation | Code files | Actual code implementation |

## Example Workflow

1. **User adds to RAW_REQUIREMENTS.md**:
   ```
   - Need user login
   - Store passwords securely
   ```

2. **AI analyzes and creates ANALYZED_REQUIREMENTS.md**:
   - Identifies "User Authentication" functionality
   - Breaks into: login, registration, password security

3. **AI creates features/USER_AUTHENTICATION.md**:
   - Defines steps: database schema → API endpoints → frontend → tests

4. **User reviews and approves**

5. **Implementation begins following steps**

---

**Related Documents**:
- [Best Practices](../../workflow/BEST_PRACTICES.md)
- [Feature Template](./TEMPLATE.md)
- [Features Directory](../features/README.md)

