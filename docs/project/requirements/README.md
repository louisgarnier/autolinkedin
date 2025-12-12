# Requirements Documentation

This directory contains the requirements analysis workflow from initial input to implementation-ready functionalities.

## Quick Start

1. **Add your requirements** → `RAW_REQUIREMENTS.md`
2. **Analyze together** → `ANALYZED_REQUIREMENTS.md` (with AI assistance)
3. **Create functionalities** → `../features/[NAME].md` (one file per functionality)
4. **Break into steps** → Each functionality file contains detailed implementation steps
5. **Implement** → Follow the steps in each functionality file

## Files Overview

| File | Purpose | When to Use |
|------|---------|-------------|
| `RAW_REQUIREMENTS.md` | Initial requirements capture | Start here - add requirements in any format |
| `ANALYZED_REQUIREMENTS.md` | Rephrased, structured requirements | After raw requirements are added - analyze together |
| `TEMPLATE.md` | Feature/functionality template | When creating new functionality files |
| `REQUIREMENTS_WORKFLOW.md` | Complete workflow guide | Reference for the entire process |

## Workflow

```
┌─────────────────────────┐
│ RAW_REQUIREMENTS.md     │ ← You add requirements here
│ (Initial input)         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ ANALYZED_REQUIREMENTS.md │ ← We analyze & rephrase together
│ (Structured & clarified) │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ ../features/[NAME].md   │ ← One file per functionality
│ (With implementation     │
│  steps broken down)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Code Implementation      │ ← Follow the steps
└─────────────────────────┘
```

## Detailed Workflow

See [REQUIREMENTS_WORKFLOW.md](./REQUIREMENTS_WORKFLOW.md) for the complete step-by-step guide.

## Key Principles

1. **Start Simple** - Add requirements in any format to `RAW_REQUIREMENTS.md`
2. **Analyze Together** - We'll clarify, rephrase, and structure requirements
3. **Break Down** - Each functionality gets its own file with clear steps
4. **Make Actionable** - Steps should be completable in 1-2 days
5. **Track Progress** - Use checkboxes in functionality files

## Example

**Raw Requirement**:
```
- Users should be able to login
```

**After Analysis**:
```
Priority 1: User Authentication
- Users must authenticate using email/password
- System validates credentials and returns JWT token
- Passwords must be hashed using bcrypt
```

**Functionality File** (`../features/USER_AUTHENTICATION.md`):
- Step 1: Database Schema (users table)
- Step 2: Authentication API (login endpoint)
- Step 3: Frontend Login Form
- Step 4: Testing

---

**Related Documents**:
- [Requirements Workflow](./REQUIREMENTS_WORKFLOW.md) - Detailed workflow guide
- [Feature Template](./TEMPLATE.md) - Template for functionality files
- [Features Directory](../features/README.md) - Where functionality files live
- [Best Practices](../../workflow/BEST_PRACTICES.md) - Before implementing

