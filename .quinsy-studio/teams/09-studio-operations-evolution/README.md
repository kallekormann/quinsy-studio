# Team 09 — Studio Operations & Evolution (Self-Learning Core)

> Responsible for the maintenance and evolution of the studio itself — independent of running client projects. This is the heart of the dual-loop learning system.

## Director-level roles

| Role | Level | Responsibilities |
|------|-------|------------------|
| **Studio Automation Engineer** | Director | maintenance of the Python scripts and tools in the studio HQ |
| **Process Guard** | Director | monitoring sprint discipline and optimizing studio flows independently of the project business |
| **Agile Coach** | Director | optimizing studio processes, retrospectives, team performance |
| **Documentation Writer** | Lead | strictly maintaining the separation between studio playbooks and project documentation |

---

## Skills

| ID | Skill | Lead role | File |
|----|-------|-----------|------|
| SO-001 | Studio Tooling Maintenance | Studio Automation Engineer | `skills/studio-tooling-maintenance.md` |
| SO-002 | Process Optimization | Process Guard | `skills/process-optimization.md` |
| SO-003 | Dual-Loop Learning | Process Guard + Agile Coach | `skills/dual-loop-learning.md` |
| SO-004 | Documentation Governance | Documentation Writer | `skills/documentation-governance.md` |

---

## Responsibilities

### Studio HQ maintenance
- Maintain the Python tools in `.quinsy-studio/studio-tools/`
- Update the playbooks in `.quinsy-studio/knowledge-base/`
- Improve the templates in `.quinsy-studio/studio-templates/`
- Keep the skill registry current

### Dual-loop learning

```
LOCAL LOOP (project world)            GLOBAL LOOP (studio world)
────────────────────────             ──────────────────────────
• Project-specific bugs               • Universal playbooks
• Niche insights                      • Python tooling updates
• Workarounds                         • Anti-slop rule updates
• Storage: projects/[name]/           • Storage: .quinsy-studio/
  docs/studio-learnings-local.md       knowledge-base/

⚠️ Does NOT affect other             ✅ Applies to ALL future
   projects                              projects
```

### Process optimization
- Monitor sprint discipline
- Optimize studio flows independently of the project business
- Detect and fix anti-patterns in the studio process
- Collect and analyze metrics

### Documentation governance
- Strict separation between studio playbooks and project documentation
- Maintain the CHANGELOG
- Keep READMEs current
- Ensure knowledge transfer

---

## Phase participation

| Phase | Lead roles | Support roles |
|-------|------------|---------------|
| Phase 0 | — | Documentation Writer |
| Phase 1 | — | Documentation Writer |
| Phase 2 | — | Process Guard (process check) |
| Phase 3 | Process Guard | Studio Automation Engineer |
| Phase 4 | — | Studio Automation Engineer (tooling) |
| Phase 5 | Process Guard | Documentation Writer |
| Phase 6 | **Process Guard, Agile Coach** | Documentation Writer, Studio Automation Engineer |
| Phase 7 | Studio Automation Engineer | Process Guard |

---

## Studio evolution command

```bash
# Put the studio into an autonomous maintenance sprint
./studio evolve

# Only refactors its own tools, no client project
# Improved playbooks, updated skills
# Optimized Python scripts
```

---

## References

- `.quinsy-studio/process/learning-loop.md` — dual-loop learning
- `.quinsy-studio/process/lifecycle.md` — phases
- `.quinsy-studio/studio-tools/` — python automation
- `.quinsy-studio/knowledge-base/` — playbooks
