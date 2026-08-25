# Workflow Definition Playbook

> **Skills:** UX-001 (Research), UX-002 (Interaction), UX-003 (IA for cross-surface flows)  
> **When:** Before Team 10 writes component-level design specs for multi-step or multi-surface features.

## Purpose

Define **end-to-end workflows** before atoms, molecules, or layout specs. Prevents polished UI on broken journeys.

---

## Deliverable: workflow map

Path: `projects/<project>/docs/design-specs/<TICKET-ID>-workflow.md`  
Or section **§2b Workflow map** inside the main design spec for small flows.

### Template

```markdown
## Workflow: <name>

**Actor:** <role>  
**Trigger:** <what starts this>  
**Success:** <done state>

| Step | User action | System response | Surface |
|------|-------------|-----------------|---------|
| 1 | Opens board | Canvas loads | Board |
| 2 | Clicks Share | Share dialog: canvas link tab | Share |
| 3 | Opens Presentation builder | Builder + client share panel | Builder |

### Edge cases
- No share link yet → create with defaults on canvas; full guest settings in builder
- Expired link → …

### Out of scope
- …
```

---

## When required

| Situation | Workflow map |
|-----------|----------------|
| New feature spans 2+ surfaces | **Required** |
| `ui-composition` touching dialog + another route | **Required** |
| `workflow-explainer` | **Required** (storyboard extends this) |
| Single-button color tweak | Skip |
| `ia-feature-placement` ticket | **Required** (placement is the workflow outcome) |

---

## Order of operations (Team 10)

```
1. Workflow map (this playbook)
2. Context & placement (contextual-ia-playbook.md)
3. Atomic inventory + visual spec (design-spec-template.md)
4. Human approve-design
5. Team 01 implement
```

---

## Review checklist

- [ ] Every step names the **surface** (not just component)
- [ ] No step assumes a capability lives on the wrong surface
- [ ] Entry and exit points are explicit
- [ ] Guest vs collaborator vs owner paths are separated where permissions differ
- [ ] Remediation tickets re-run workflow map — do not only resize dialogs

---

## Related

- [contextual-ia-playbook.md](contextual-ia-playbook.md)
- [design-spec-template.md](design-spec-template.md)
