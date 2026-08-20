# Skill: User Research

> Problem interviews, solution interviews, surveys, usability tests, analytics

## Metadata

```
skill_id: PM-001
name: User Research
team: 06-product-management-operating-model
lead_role: Product Manager
support_roles: [UI/Interaction Designer, Growth Manager]
phases: [0, 1, 3, 5, 7]
activation_triggers:
  - Ticket contains "research", "interview", "survey", "usability"
  - Phase 0: problem is validated
  - Phase 1: solution is validated
  - Phase 5: usability is tested
  - Phase 7: optimization based on feedback
```

---

## Behavior rules

### 1. Problem interviews

```markdown
Goal: understand the problem, not sell the solution

Structure (15-30 min):
  1. Context: "Tell me about..."
  2. Problem: "What is frustrating about it?"
  3. Current solution: "How do you solve it today?"
  4. Value: "What would you pay for that?"
  5. Closing: "Is there anything else?"

Rules:
  - 80% listening, 20% questions
  - Don't propose a solution
  - Ask follow-up questions
  - Note emotions and quotes
```

### 2. Solution interviews

```markdown
Goal: test the solution, not sell features

Structure:
  1. Show the concept (don't explain anything)
  2. "What do you understand?"
  3. "How would you use it?"
  4. "What is missing?"
  5. "Would you pay for it?"

Rules:
  - Show a prototype (don't tell)
  - Be patient (let users think)
  - Confusion = design problem
```

### 3. Surveys

```markdown
When: quantitative feedback from many users

Structure:
  - Max. 10 questions
  - Mix of multiple choice + open
  - Likert scale (1-5 or 1-7)
  - Demographics at the end

Rules:
  - No suggestive questions
  - No double questions
  - Test with 3 people beforehand
  - Incentive for participation
```

### 4. Usability tests

```markdown
Structure (30-45 min):
  1. Context: "Imagine..."
  2. Task: "Please find..."
  3. Think aloud: "What are you thinking?"
  4. Follow-up: "Why did you...?"

Rules:
  - 5 users = 80% of the problems
  - No assistance
  - Record: where does the user fail?
  - Severity rating: critical / medium / low
```

### 5. Analytics

```markdown
Tools: Plausible / PostHog / Google Analytics

Metrics:
  - Pageviews, unique visitors
  - Bounce rate
  - Time on page
  - Conversion rate
  - User flows (where do users go?)
  - Drop-off points (where do users leave?)

For decisions:
  - Quantitative data (analytics) +
  - Qualitative data (interviews) =
  - Informed decision
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Interpreting feature requests as user needs
- Only quantitative data (no interviews)
- Leading questions ("Do you agree that...")
- Testing with only 1-2 users
- Revealing the solution in interviews
```

### ✅ Instead

```markdown
- "Five whys" for deeper understanding
- Mix of qualitative and quantitative
- Ask open questions
- Min. 5 users for usability tests
- Understand the problem, don't sell the solution
```

---

## References

- `.quinsy-studio/process/lifecycle.md` — phases
- `.quinsy-studio/knowledge-base/design_playbook.md` — UX heuristics
