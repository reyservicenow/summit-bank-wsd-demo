# Summit Bank WSD Demo – Backup

Backup of the ServiceNow Workplace Service Delivery (WSD) demo built on `dev445147` for the Truist / Compucom interview: a fictional bank ("Summit Bank") migrating 50 spaces from an IBM TRIRIGA export into WSD, with neighborhoods, a restack scenario, reservations and Map Studio floor plans.

If the developer instance is reclaimed, everything needed to rebuild it is here or is produced by the steps below.

## What's in this repo

| Folder | Contents |
| --- | --- |
| `instance-scripts/` | `01_export_update_sets.js` (run in Scripts - Background) and `data-tables.txt` (list of demo data records to export) |
| `scripts/` | `backup.sh` (Mac/Linux) and `backup.ps1` (Windows): download the update sets and data as XML |
| `backups/<date>/` | The XML backups: `update-sets/`, `data/`, and `installed-store-apps.json` |
| `demo-kit/` | TRIRIGA CSV, CAD floor plans (DXF + previews), CAD audit and converter scripts |
| `docs/` | 90-day plan, demo script, [restore guide](docs/RESTORE.md), [best practices](docs/BEST_PRACTICES.md), [instance inventory](docs/INSTANCE_INVENTORY.md) |

## Take a backup (about 10 minutes)

1. **Publish the custom app to an update set.** All > System Applications > My Company Applications > In Development > **Summit Bank WSD Demo** > related link **Publish to Update Set**. Version `1.0.0`, leave *Include data* unchecked, click **Publish**. This creates a Complete update set with the current version of every app file.
2. **Create the update set exports.** All > System Definition > **Scripts - Background**, scope `global`, paste `instance-scripts/01_export_update_sets.js`, click **Run script**. It prints one `EXPORT|...` line per update set changed since Oct 28, 2026 (including the one from step 1).
3. **Download them.** Either click each link while logged in, or copy all `EXPORT|...` lines into `backups/export-links.txt` and run:
   - Mac/Linux: `./scripts/backup.sh dev445147`
   - Windows: `.\scripts\backup.ps1 -Instance dev445147`

   The script also exports the demo **data** records (sites, buildings, floors, spaces, neighborhoods, reservations, scenario, Map Studio campus/floors/places) and the list of installed WSD apps with versions.
4. **Commit and push.**
   ```bash
   git add backups && git commit -m "Backup $(date +%F)" && git push
   ```

If you clicked the links in step 3 instead of running the script, move the downloaded `.xml` files into `backups/<date>/update-sets/` before committing, then run the script anyway for the data export (it skips update sets when `export-links.txt` is missing).

## Restore

See [docs/RESTORE.md](docs/RESTORE.md). Short version: install the same WSD store apps, import the app update set, import the other update sets, import the data XML in file-number order, re-attach the CSV and DXF files from `demo-kit/`.

## Notes

- Keep this repository **private**: the XML contains user names and instance sys_ids.
- Passwords are prompted for and never saved. `.gitignore` blocks common credential files.
- Optional ongoing backup: link the app to this repo with ServiceNow Studio source control (see [docs/BEST_PRACTICES.md](docs/BEST_PRACTICES.md)).
