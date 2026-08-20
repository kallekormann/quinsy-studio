# Skill: Game Development

> Game engine setup, 2D/3D mechanics, asset pipelines, and gamedev-specific architecture.

## Metadata

```
skill_id: GM-004
name: Game Development
team: 05-growth-marketing-content
lead_role: Game Systems Architect
support_roles: [Frontend Architect, Backend Architect]
phases: [2, 3, 4, 5]
activation_triggers:
  - Ticket contains "game", "Godot", "Unity", "Unreal", "Phaser", "platformer"
  - Project archetype is `game`
  - Phase 2: engine and scene architecture defined
  - Phase 4: gameplay implementation
```

---

## Behavior rules

### 1. Engine-first architecture

- Choose engine from PRD (Godot, Unity, Unreal, Phaser, three.js, pygame)
- Do not apply SaaS setup tickets (DB schema, OAuth) unless the PRD explicitly requires online services
- Scene graph, input handling, and asset loading are P0 for game projects

### 2. Game-specific quality gates

- Playable build in dev environment before marking tickets done
- Frame budget and input responsiveness documented in ADR
- Anti-slop applies to game UI copy and store descriptions, not engine boilerplate

### 3. Archetype routing

When archetype is `game`, prefer gamedev skills over generic frontend/backend setup.

---

## External skill support

> Load `./studio update-skills` first, then use the gamedev router:

- **`gamedev/router/SKILL.md`** — routes to engine-specific skills (Godot, Unity, Unreal, Phaser, PixiJS, three.js, Bevy, pygame, LÖVE, Roblox)
- Engine-specific skills under **`gamedev/`** — selected automatically by the router based on ticket text

Flow: read router SKILL → follow engine recommendation → apply engine-specific checklist → document engine choice in ADR.

## References

- `.quinsy-studio/process/project-archetypes.md` — `game` archetype
- `.quinsy-studio/teams/skill-registry.md` — GM-004 trigger words
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — UI/marketing slop gates
