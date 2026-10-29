# 90-Day Plan – ServiceNow WSD Consultant (Truist via Compucom)

Oct 28, 2026 · @RAI

By day 90 the client has a working WSD proof of concept on its own floor plans and a go/no-go recommendation, with gaps, integrations, migration path and level of effort, for moving Truist off IBM TRIRIGA. The 90 days line up with the contract, which runs through Feb 28, 2027.

## Roadmap

&#91;embedded content: 90-day roadmap · 3 phases, 3 gates\]

Each phase ends in a gate the sponsor signs off; the POC build in days 31–60 is where most of the effort goes.

## Days 1–30: Discover

Goal: know exactly what the current platform does, who depends on it, and whether the CAD data is usable in WSD.

**Stakeholders and governance**

- Meet the sponsor, corporate real estate (CRE) lead, space planners, facilities ops, IT platform owner and the current-platform admin.
- Agree on decision criteria for the evaluation: must-haves, nice-to-haves, cost, timeline.
- Set a weekly status cadence and a single RAID log (risks, assumptions, issues, decisions).

**Current-state inventory**

- Demo TRIRIGA end to end: reservations (desks, rooms, parking), neighborhoods, occupancy reporting, stack plans, restacking, move management.
- Export a feature list, user counts by role, booking volumes, and every integration (HRIS, badge/sensor, calendar, CAFM/IWMS, SSO).
- Document each process as Business outcome → Process → Requirement, the start of the operating model used through day 90.

**Data and floor plans**

- Collect DWG/DXF files for 1–2 pilot buildings and audit them: layers, polylines for rooms, text or blocks for space IDs, units, one file per floor.
- Pull the location and space hierarchy (campus → building → floor → space) and compare it to the CMDB/`cmn_location` data.
- Flag CAD cleanup work early; it is the most common schedule risk.

**Platform readiness**

- Confirm WSD licensing, plugins installed (Workplace Core, Workplace Central, Reservation Management, Space Management, Indoor Mapping) and the release/app versions.
- Stand up or claim a sub-production instance for the POC.

**Day-30 gate:** signed-off requirements list, CAD audit result, and an agreed POC scope with 3–5 demo scenarios.

## Days 31–60: Build the POC

Goal: a working WSD demo on the client's own buildings, configured out of the box first and customized only where a requirement forces it.

**Foundation (weeks 5–6)**

- Load the location hierarchy and spaces in bulk from spreadsheet; set space types, capacity, reservable vs. assigned.
- Import pilot floors through Indoor Mapping / Map Studio: configure Place Types first, map CAD layers to spaces, add points of interest and wayfinding, then sync to WSD.
- Keep a PNG floor-plan fallback ready if a CAD file cannot be cleaned in time.

**Scenarios (weeks 7–8)**

1. Employee books a desk, room and parking from the Employee Center / mobile app, with check-in and auto-release.
2. Space planner manages neighborhoods and assigns users from the floor map.
3. Planner builds a what-if scenario and restacks a department on the stack plan, then turns it into a move project.
4. Workplace manager views occupancy and utilization dashboards (bookings, no-shows, peak days).
5. Optional: one integration stub (calendar, badge or sensor feed) to prove the data path.

**Working practices**

- Weekly demo to the business; capture feedback as stories with acceptance criteria.
- Track every configuration in update sets; log each customization with its reason and upgrade impact.

**Day-60 gate:** stakeholders run the scenarios themselves and score each requirement as Met OOB, Met with configuration, Needs customization, or Gap.

## Days 61–90: Assess and recommend

Goal: a decision-ready recommendation the sponsor can take to leadership.

**Fit-gap and architecture (weeks 9–10)**

- Finish the fit-gap matrix: each requirement → WSD capability → OOB/config/custom/gap → proposed solution.
- Draw the target architecture: WSD apps, CMDB/location data, HRIS for people, SSO, calendar, sensors/badges, and any IWMS or lease system that stays.
- Define a CAD/floor-plan operating model: who updates drawings, layer standards, how changes reach WSD.

**Migration and effort (week 11)**

- Migration approach: data to move (locations, spaces, assignments, neighborhoods, future bookings), cutover order by building, parallel-run period.
- Choose the floor-plan route per building: CAD now, or PNG first and CAD later.
- Level-of-effort estimate by workstream with assumptions, dependencies and a phased rollout (pilot building → region → global).

**Recommendation (week 12–13)**

- Executive readout: POC demo, fit-gap summary, risks, cost and timeline, and a clear go / go-with-conditions / no-go.
- Hand over: POC update sets, configuration workbook, CAD standards, backlog of stories for phase 1.

**Day-90 gate:** sponsor decision and an approved phase-1 scope.

## POC scope: current capability → WSD

Every capability named in the role maps to an existing WSD app, so the POC tests fit rather than building from scratch.

| Current capability | WSD app / feature | What the POC proves |
| --- | --- | --- |
| Desk, room, parking reservations | Workplace Reservation Management | Booking, check-in, auto-release, mobile |
| Floor plans from AutoCAD | Workplace Indoor Mapping (Map Studio) | DWG/DXF import, Place Types, wayfinding, sync to WSD |
| Space inventory | Workplace Core | Bulk load of buildings, floors, spaces |
| Neighborhoods and assignments | Space Planning (Workplace Central) | Assign users and neighborhoods on the floor map |
| Restacking and what-if | Scenario Planning, stack plan | Reallocate departments, compare scenarios |
| Moves after a restack | Move Scheduler / Workplace Case Management | Bulk move projects from a scenario |
| Occupancy and utilization | Workplace analytics, sensor integrations | Utilization KPIs, no-show rates |

## TRIRIGA → WSD migration

Migrate in four steps (back up, map, load by building, run in parallel), so TRIRIGA is retired only after WSD data is reconciled.

| TRIRIGA data | WSD target | How it moves |
| --- | --- | --- |
| Property, building, floor hierarchy | Workplace locations | TRIRIGA Integration Object export (flat file or JSON) → WSD bulk spreadsheet import |
| Spaces (type, area, capacity) | Workplace spaces and space types | Same export and bulk import |
| People and space assignments | User assignments, neighborhoods | Export, then reconcile against HR data |
| Future reservations | Workplace reservations | Move future bookings only, or freeze and re-book at cutover |
| AutoCAD floor plans | Indoor Mapping (Map Studio) | Reuse the source DWGs; check layer and space-ID standards |
| Integrations (HR, calendar, badges, sensors) | Integration Hub | Rebuild in ServiceNow; TRIRIGA's REST API can bridge during the parallel run |

1. **Back up:** full read-only export of all in-scope TRIRIGA data.
2. **Map:** TRIRIGA records and fields → WSD tables; anything with no home goes on the gap list.
3. **Load by building:** pilot building first, then waves.
4. **Parallel run, then retire:** keep both until users and data reconcile, then retire TRIRIGA.

Open questions for the first week:

- [ ] Which TRIRIGA version and modules does Truist use?
- [ ] Are the source DWG files and layer standards available, or only drawings stored in TRIRIGA?
- [ ] Does TRIRIGA also handle leases, projects or work orders that are out of WSD scope?

Export options: [IBM TRIRIGA integration and data migration](https://www.ibm.com/docs/en/SSDKWV/files/24_Integration_and_Data_Migration.html).

## Success measures and risks

**Success at day 90**

- 100% of in-scope requirements scored in the fit-gap matrix.
- At least 2 pilot floors live in the POC from real CAD files.
- All 4 core scenarios demoed by business users, not just by the consultant.
- Estimate and phased roadmap accepted by the sponsor.

**Risks and fallbacks**

| Risk | Fallback |
| --- | --- |
| CAD files are messy (no layers, text instead of blocks) | Clean 1–2 floors only; use PNG plans for the rest |
| WSD apps not licensed or out of date on the instance | Confirm in week 1; use a demo/PDI instance for the POC |
| Stakeholders compare against every feature of the current tool | Agree must-haves in the day-30 gate |
| Integration owners unavailable | Stub data feeds in the POC; list as dependencies |
| Scope creep into full implementation | Keep a backlog; build only the agreed scenarios |

## Sources

- [Implement Workplace Indoor Mapping in a day – ServiceNow Community](https://www.servicenow.com/community/wsd-blog/implement-workplace-indoor-mapping-in-a-day/ba-p/3589065)
- [What's available in Space Planning – ServiceNow Community](https://www.servicenow.com/community/wsd-blog/what-s-available-in-space-planning/ba-p/3579990)
- [Space Planning (Zurich) – ServiceNow Docs](https://www.servicenow.com/docs/r/SogDT~k7ktsbe1ZYegnaLg/6kAp1ztEZHCVJiKZtBxSOw)
- [Workplace Service Delivery applications – ServiceNow Docs](https://www.servicenow.com/docs/r/baBFTRuHLgu7HSwp0SUEQQ/PL5gfPn8MRBklAdU40KNkg)
- [Workplace Space Management release notes – ServiceNow Docs](https://www.servicenow.com/docs/r/C17ZqvSaMwUVpMBg8Nc5sg/GmNrnZzVEYhVB18pyPKRcQ)
- [Workplace Indoor Mapping – ServiceNow Store](https://store.servicenow.com/store/app/f4ebefea1b246a50a85b16db234bcbba)
