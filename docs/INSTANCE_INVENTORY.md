# Instance inventory (as of Oct 28–29, 2026)

Recorded during the build. The backup script also saves a live copy (`backups/<date>/installed-store-apps.json`).

## Instance

| Item | Value |
| --- | --- |
| Instance | dev445147.service-now.com (personal developer instance) |
| Build | glide-brazil-08-25-2026, patch 1 (09-21-2026) |

## Store apps installed for the demo

| App | Scope | Version |
| --- | --- | --- |
| Workplace Core | sn_wsd_core | 2.29.9 |
| Workplace Space Management | sn_wsd_spcmgmt | 1.20.30 |
| Workplace Stack Plan | sn_wsd_stackplan | 1.5.12 |
| Workplace Reservation Management | sn_wsd_rsv | 3.7.0 |
| Workplace Central | sn_wsd_central | 1.16.30 |
| Workplace Indoor Mapping | sn_wsd_indoor_map | 1.18.12 |
| Workplace Space Mapping | sn_wsd_space_map | 1.20.10 |
| Indoor Mapping (core) | sn_map_core | 1.18.0 |
| Map component | sn_map_component | 1.6.1 |

## Custom work

| Item | Where |
| --- | --- |
| Scoped app | Summit Bank WSD Demo (`x_189579_wsddemo`) |
| Update set | Summit Bank WSD Demo - TRIRIGA migration |
| Import table | `x_189579_wsddemo_tririga_space_import` |
| Data source | Summit Bank - TRIRIGA Space Export |
| Transform map | Summit Bank - TRIRIGA Space to WSD Space (coalesce on `external_id` = `TRIRIGA:<space ID>`; transform script + onAfter script) |
| Reservable module | Meeting rooms (app copy). A stray duplicate may remain in the Vehicle Tracking app; it has no bookings. |

## Demo data (not in update sets; see `instance-scripts/data-tables.txt`)

| Data | Count |
| --- | --- |
| Site / campus / building | Charlotte, NC / Summit Bank Charlotte Campus / Summit Tower |
| Floors | Summit Tower - Floor 10, 11, 12 |
| Spaces (`wsd_source = TRIRIGA`) | 50 |
| Neighborhoods | Retail Banking, Wealth Management, Technology, Risk & Compliance |
| Reservations | 9 (desks, meeting rooms, focus room) |
| Scenario | Summit Tower restack - consolidate Technology on Floor 12 (draft) |
| Map Studio | Campus, building, Floor 10 and 11, 46 places, 2 AutoCAD sources, Default and Scenario Planning views |

## Admin user roles added

`sn_wsd_core.admin`, `sn_wsd_core.workplace_user` (needed for the Employee Center booking page).
