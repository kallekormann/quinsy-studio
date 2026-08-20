# Skill: Operating Model

> Team structure, agile processes, ceremonies, OKRs, metrics

## Metadata

```
skill_id: PM-003
name: Operating Model
team: 06-product-management-operating-model
lead_role: Operating Lead
support_roles: [Product Manager, Agile Coach]
phases: [0, 1, 7]
activation_triggers:
  - Ticket contains "operating model", "team structure", "process"
  - Phase 0: team structure is defined
  - Phase 1: processes are established
  - Phase 7: retro and optimization
```

---

## Behavior rules

### 1. Team structure

```markdown
Standard (SaaS project):
  - Product Manager (1)
  - Frontend Engineer (1-2)
  - Backend Engineer (1-2)
  - QA Specialist (0.5-1)
  - DevOps/Platform (0.5)

Scaling:
  - Squad model at >8 people
  - Cross-functional teams
  - Feature teams instead of component teams
```

### 2. Agile processes

```markdown
Sprint length: 2 weeks

Ceremonies:
  - Sprint planning (Monday, 1h)
  - Daily standup (daily, 15 min)
  - Sprint review (Friday, 1h)
  - Sprint retro (Friday, 30 min)
  - Backlog grooming (Wednesday, 1h)

Definition of done:
  - Code written
  - Tests green
  - Code review passed
  - QA passed
  - Docs current
```

### 3. OKRs

```markdown
Structure:
  Objective: what do we want to achieve?
  Key results: how do we measure success?

Example:
  O: "Improve user retention"
  KR1: "Increase 30-day retention from 40% to 60%"
  KR2: "Get onboarding completion rate to 80%"
  KR3: "Increase NPS from 30 to 50"

Frequency: quarterly
Review: monthly
```

### 4. Metrics

```markdown
North Star metric:
  - The ONE metric that measures value

Supporting metrics:
  - Acquisition: signups, traffic
  - Activation: onboarding completion
  - Retention: continued usage
  - Revenue: MRR, ARPU
  - Referral: NPS, shares
```

### 5. Knowledge transfer

```markdown
Documentation:
  - Decision log (decisions + rationales)
  - Sprint summary (what was learned?)
  - Onboarding docs for new team members
  - Architecture decision records (ADRs)
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Dogmatic scrum without adaptation
- No retros
- OKRs that are never reviewed
- No knowledge transfer
- Silos between teams
```

### ✅ Instead

```markdown
- Agile adapted to team size
- Regular retros with action items
- Review OKRs monthly
- Docs as an obligation (not optional)
- Cross-team collaboration
```

---

## References

- `.quinsy-studio/process/iterative-delivery.md` — sprint/grooming
- `.quinsy-studio/process/learning-loop.md` — learning loop
