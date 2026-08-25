# Amendment brief — Agency positioning & client presentation track

> **Project:** acme-app  
> **Amendment ID:** (assigned on intake → `AM-001`)  
> **Author:** Product owner  
> **Date:** 2026-08-01  
> **Status:** example — copy to `intake/amendments/<project>/amendment_01.md`  
>
> **Then:** `./studio amend <project> intake/amendments/<project>/amendment_01.md`  
> **Do not fill milestones here** — the studio derives phases after analysis.

---

## 1. Executive summary

Shift from solo creator tool to **agency workflow**: teams share boards internally, ship **client-facing presentation links** with guest access controls, and export brand kits. Billing/limits can wait until agency surfaces are stable.

## 2. Why now

| Trigger | Detail |
|---------|--------|
| Primary driver | Pilot agencies need client presentation without full editor access |
| Evidence | 3 agency interviews; share dialog overloaded |
| Urgency | Before next milestone (billing) |

## 3. Vision & concept

### 3.1 North-star statement

Agencies curate boards in private; clients experience a **guided narrative** with controlled guest access — configured where they author presentations, not in generic share chrome.

### 3.2 Key scenarios

1. Designer builds presentation sections in **presentation builder** → copies client link with password/expiry there  
2. Designer shares **canvas read-only link** with collaborator via Share dialog  
3. Client opens presentation URL → scrolls narrative, leaves feedback  

### 3.3 Product principles

- Separate **collaboration** (Share) from **client delivery** (presentation builder)  
- Guest access settings live in presentation context  

## 4. Scope boundaries

### 4.1 In scope

- Presentation builder client-share panel (link, access level, password, expiry)  
- Share dialog slimmed to canvas link + email invite  
- Team seats (read later in analysis)  

### 4.2 Out of scope

- Billing / usage limits (defer to later milestone)  
- Figma plugin  

## 5. Success picture

- Agencies ship client links without support tickets about "where is presentation URL"  
- Share dialog task completion time drops (fewer fields)  

## 6. Constraints & dependencies

- Same share token under hood for canvas vs `?mode=presentation` until split is justified  
- Design HITL for all UI surfaces  

## 7. Open questions

- Should guest access changes in builder invalidate canvas link stats display?  
- Team editor share policy — stay on Share dialog?  

## 8. Team selection (check all that apply)

- [x] 01 Frontend Experience  
- [x] 02 Backend Systems  
- [x] 04 Product Strategy  
- [x] 10 Product Design & Experience  

## 9. Skill selection (check all that apply)

- [x] UX-003 — contextual IA / feature placement  
- [x] UX-002 — interaction workflows  
- [x] FE-001, FE-002 — implementation  
- [x] BE-001 — share APIs  

## 10. References

- Competitive: Figma presentation mode, Milanote share  

---

## Studio output (after submit — do not fill)

Agent produces `projects/<project>/docs/amendments/AM-001-*/` per [amendment-intake.md](../process/amendment-intake.md).
