# WSD Demo Script – Summit Bank TRIRIGA Migration

Oct 28, 2026 · @RAI

A 10-minute live demo on dev445147 showing a fictional bank (Summit Bank) moving 50 spaces from a TRIRIGA export into ServiceNow WSD: migration, location hierarchy, neighborhoods on a stack plan, reservations, and a CAD readiness check.

## Demo flow (about 10 minutes)

**Opening line:** "I built a small version of this engagement on my own instance: a bank moving off TRIRIGA into WSD. Same approach I'd use with Truist: back up, map, load by building, run in parallel."

1. **The TRIRIGA export (1 min).** Open the data source *Summit Bank - TRIRIGA Space Export* and its CSV attachment.
   - Say: "This mimics a TRIRIGA space export: property, building, floor, space ID, class, area, capacity, org and primary occupant. 50 spaces across 3 floors."
2. **The migration (3 min).** Open the transform map *Summit Bank - TRIRIGA Space to WSD Space*, then the latest import set.
   - Show the coalesce on `external_id` = `TRIRIGA:<space ID>`. Say: "Re-running the load updates, never duplicates, so we can do a trial load, a delta load and a final cutover load."
   - Show the transform script: it builds site, campus, building and floors on the fly, maps TRIRIGA space classes to WSD space types, sets flex vs. assigned, and creates departments.
   - Show the onAfter script and the import log warnings: TRIRIGA had two offices for the same person, WSD keeps one primary location per employee. Say: "The migration surfaces data-quality issues instead of hiding them."
   - Optional live step: on the data source, click **Load All Records**, then **Run Transform**. Result: 50 rows updated, same warnings.
3. **The result in WSD (2 min).** Open Workplace Central, then Space Optimization, then *Summit Tower*.
   - Stack plan, view by **Neighborhood**: Retail Banking, Wealth Management and Technology on each floor. Say: "TRIRIGA org became WSD neighborhoods, so planners can restack from day one."
4. **Restack scenario (1 min).** In Space Optimization, open *Summit Tower restack - consolidate Technology on Floor 12*.
   - In **Edit scenario** mode, drag a neighborhood bar to another floor and watch the capacity numbers update. Say: "This is the what-if before anyone moves; once approved it becomes a move plan."
   - Leave it as a draft. Don't publish.
5. **Reservations (1 min).** In Workplace Central, open **Lists**, then *Event Planner - Open reservations for the next month*: 9 bookings on migrated desks, meeting rooms and a focus room. Click **Open schedule view** for the calendar.
   - Switch to Employee Center (Make a reservation) and book a desk in Summit Tower as an employee.
6. **From CAD to map (3 min).** Share your screen with the demo kit folder, then Map Studio.
   - Run `python3 cad_audit.py *.dxf --tririga tririga_space_export.csv`: floors 10 and 11 READY, floor 12 NOT READY (open outline, missing label, wrong layer, unknown space ID), and an old R12 file flagged for missing units.
   - In **Map Studio**, open the campus, then **Floor plan sources**: the TRIRIGA-style DXF was imported with the AutoCAD importer. Layers mapped: ASF = building outline, GSFI = walls, A-Area-Space = rooms, A-Area-Iden text = space names.
   - Click **Preview**, then the Summit Tower marker: Floor 10 and Floor 11 as interactive indoor maps on downtown Charlotte, each place linked to its migrated WSD space.
   - Say: "Map Studio reads TRIRIGA's layer-and-text drawings directly. The older Workplace Core floor plan upload wants blocks with attributes, so I also wrote a converter for that route."

**Close:** "That's the shape of the 90-day plan: prove the data path and the gaps early on real floors, then size the rollout."

## Links (open these in tabs before the call)

| Stop | Screen | What's there |
| --- | --- | --- |
| 1 | [Data source](https://dev445147.service-now.com/sys_data_source.do?sys_id=6aeacd90c3d0571014d3b91ed4013185) | TRIRIGA CSV attached; Load All Records |
| 2 | [Transform map](https://dev445147.service-now.com/sys_transform_map.do?sys_id=330b05d0c3d0571014d3b91ed4013162) | Field maps, coalesce, transform and onAfter scripts |
| 2 | [Latest import set](https://dev445147.service-now.com/sys_import_set.do?sys_id=180b01d0c3d0571014d3b91ed40131b6) | 14 rows updated, 36 unchanged, import log warnings |
| 3 | [Migrated spaces](https://dev445147.service-now.com/sn_wsd_core_space_list.do?sysparm_query=wsd_source%3DTRIRIGA) | 50 spaces with type, floor, department, external ID |
| 3 | [Neighborhoods](https://dev445147.service-now.com/sn_wsd_core_neighborhood_list.do) | Retail Banking, Wealth Management, Technology, Risk & Compliance |
| 3 | [Workplace Central: Summit Tower](https://dev445147.service-now.com/now/workplace-management/building-overview/c4483858c35c171014d3b91ed4013164/params/heading/BLDG0001052) | Stack plan; set View by to Neighborhood |
| 4 | [All reservations](https://dev445147.service-now.com/sn_wsd_rsv_reservation_list.do) | 9 bookings on migrated desks and rooms |
| 4 | [Reservable modules](https://dev445147.service-now.com/sn_wsd_rsv_reservable_module_list.do) | Desks and Meeting rooms |
| 5 | Demo kit folder (download from chat) | Floor plans, audit, converter, TRIRIGA CSV |

All demo configuration lives in the scoped app **Summit Bank WSD Demo** (x\_189579\_wsddemo), tracked in the update set *Summit Bank WSD Demo - TRIRIGA migration*.

| Stop | Screen | What's there |
| --- | --- | --- |
| 4 | [Restack scenario](https://dev445147.service-now.com/now/workplace-management/scenario-planning/scenario/86a08ddcc310571014d3b91ed4013117) | Draft scenario, stack plan in edit mode |
| 5 | [Workplace Central lists](https://dev445147.service-now.com/now/workplace-management/list/params/list-id/cdb355d493b7121071c233337489186c/tiny-id/nadEgn0MJeSQbR9w5p71O5VdTcvzvEwS) | Event Planner: open reservations, schedule view |
| 5 | [Employee booking page](https://dev445147.service-now.com/esc?id=wsd_search) | Book a desk (after the role fix) |
| 6 | [Map Studio](https://dev445147.service-now.com/sn_map_core_indoor_mapping_studio.do) | Campus, floor plan sources, Preview |
| 6 | [AutoCAD sources](https://dev445147.service-now.com/sn_map_core_autocad_source_list.do) | The two imported TRIRIGA-style DXF files and their layer mapping |

## Talking points and honest gaps

**What the demo proves**

- A repeatable TRIRIGA → WSD load using standard import sets and transform maps; no custom tables in WSD.
- Hierarchy (site → campus → building → floor → space) is built from the export, which also satisfies WSD rules such as a mandatory building time zone.
- Data-quality issues are logged, not silently fixed: duplicate occupants, unknown space IDs, open CAD outlines.

**Findings worth raising**

- **CAD format:** TRIRIGA drawings (outlines plus text) need either Map Studio (Indoor Mapping) or conversion to blocks with attributes for the Workplace Core floor plan upload. Ask which route Truist prefers.
- **One location per person:** TRIRIGA can hold several assignments per employee; WSD workplace profiles keep one primary location. Decide the rule before migration.
- **Department vs. neighborhood:** on this instance the stack plan's Department view did not pick up the department set on each space; it groups by Space Management's own allocation data. In the demo, TRIRIGA orgs became neighborhoods so the stack plan works immediately.

**Remaining gaps (say so if asked)**

- **Workplace Central floor map:** the Floor map tab finds the building on the Charlotte map but doesn't draw the floor yet; the Indoor Mapping to WSD sync still needs to run. Show the floor plans in Map Studio Preview instead.
- **Employee booking page:** fixed. The Make a reservation page in Employee Center now opens for admin.
- **Space IDs:** the demo stores the TRIRIGA ID in the space's `external_id`. Indoor Mapping sync also uses external IDs, so in a real project keep the TRIRIGA ID in its own field.
- **CAD file format:** Map Studio's importer failed on an old R12 DXF without drawing units and worked on R2000 with units set to feet. The audit script now checks both.

**Questions for the hiring manager**

- Which TRIRIGA modules and version, and is space data the only thing moving, or leases and projects too?
- Who owns the DWG files today, and are room numbers the same as TRIRIGA space IDs?
- Which WSD apps are licensed: Reservation Management, Space Management, Indoor Mapping?
- What does success look like by Feb 28: a POC decision, or a first building live?

## Before and after the interview

- [ ] Wake the instance an hour before: developer instances sleep when idle.
- [ ] Fix the booking page once: open your **admin** user record, Roles tab, **Edit**, add `sn_wsd_core.admin`, save, then add `sn_wsd_core.workplace_user`. Log out and back in, then open `/esc?id=wsd_search`.
- [ ] Log in and open every link in the table above in its own tab.
- [ ] In Workplace Central, set the stack plan View by to Neighborhood.
- [ ] Open Map Studio Preview once so the map tiles are cached.
- [ ] Unzip the demo kit, run `pip install ezdxf`, and test the audit command once.
- [ ] Use only the Summit Bank name on screen; no Truist data is in the demo.
- [ ] After the interview, run the cleanup script below in Scripts - Background if you want the demo removed.

Cleanup (removes only the demo records):

```javascript
var r = new GlideRecord('sn_wsd_rsv_reservation'); r.addQuery('workplace_location.wsd_source', 'TRIRIGA'); r.deleteMultiple();
var sc = new GlideRecord('sn_wsd_spcmgmt_scenario_plan'); sc.addQuery('name', 'STARTSWITH', 'Summit Tower restack'); sc.deleteMultiple();
['Retail Banking', 'Wealth Management', 'Technology', 'Risk & Compliance'].forEach(function (n) {
  var nb = new GlideRecord('sn_wsd_core_neighborhood');
  if (nb.get('name', n)) { var m = new GlideRecord('sn_wsd_core_neighborhood_m2m_space'); m.addQuery('neighborhood', nb.getUniqueValue()); m.deleteMultiple(); nb.deleteRecord(); }
});
var mc = new GlideRecord('sn_map_core_campus');
if (mc.get('name', 'Summit Bank Charlotte Campus')) {
  ['sn_map_core_autocad_source', 'sn_map_core_place'].forEach(function (t) { var g = new GlideRecord(t); g.addQuery('campus', mc.getUniqueValue()); g.deleteMultiple(); });
  var mf = new GlideRecord('sn_map_core_floor'); mf.addQuery('building.campus', mc.getUniqueValue()); mf.deleteMultiple();
  var mb = new GlideRecord('sn_map_core_building'); mb.addQuery('campus', mc.getUniqueValue()); mb.deleteMultiple();
  mc.deleteRecord();
}
['sn_wsd_core_space', 'sn_wsd_core_floor', 'sn_wsd_core_building', 'sn_wsd_core_campus', 'sn_wsd_core_site'].forEach(function (tbl) {
  var g = new GlideRecord(tbl); g.addQuery('wsd_source', 'TRIRIGA'); g.deleteMultiple();
});
```
