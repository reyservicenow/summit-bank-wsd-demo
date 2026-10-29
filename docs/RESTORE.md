# Restore guide

Use this when `dev445147` is gone and you have a new developer instance. Restore in this order; each step depends on the one before.

## 1. Same release, same store apps

- Request a new developer instance on the same family as the backup (see `docs/INSTANCE_INVENTORY.md`; the backup was taken on Brazil, patch 1).
- Install the WSD store apps listed in `backups/<date>/installed-store-apps.json` from All > System Applications > All Available Applications. Install in this order so dependencies resolve: Workplace Core, Workplace Space Management (brings Stack Plan), Workplace Reservation Management, Workplace Central, Workplace Indoor Mapping (brings Indoor Mapping and Space Mapping).
- Store apps are not in the update sets. Update sets only hold your changes on top of them.

## 2. The custom app (Summit Bank WSD Demo)

1. Elevate to `security_admin`.
2. System Update Sets > Retrieved Update Sets > **Import Update Set from XML**.
3. Upload the published app update set (`Summit_Bank_WSD_Demo_1.0.0.xml` or similar) from `backups/<date>/update-sets/`.
4. Open it > **Preview Update Set** > resolve any problems (usually "missing table" if a store app is missing; go back to step 1) > **Commit Update Set**.

This recreates the scoped app `x_189579_wsddemo`: the TRIRIGA import table, data source, transform map with its scripts, and the Meeting rooms reservable module.

## 3. Other update sets

Import, preview and commit the remaining files in `update-sets/` the same way, oldest first. Skip any "Default" set whose changes you don't need.

## 4. Data records

Data (spaces, reservations and so on) is not in update sets. For each file in `backups/<date>/data/`, in number order:

1. Open the table's list view (the table name is in the file and in `instance-scripts/data-tables.txt`).
2. Right-click any column header > **Import XML** > choose the file > **Upload**.

Notes:
- XML import keeps the original sys_ids, so references between files (space → floor → building) line up.
- XML import skips business rules. That is why this guide restores data in hierarchy order.
- Users in reservations and profiles (abel.tuter, beth.anglin, …) are standard demo users that exist on every developer instance.

## 5. Attachments

Attachments are not in update sets or list XML. Re-attach:

- `demo-kit/tririga_space_export.csv` to the data source **Summit Bank - TRIRIGA Space Export**.
- `demo-kit/summit_tower_10_r2000.dxf` and `summit_tower_11_r2000.dxf` to the two Map Studio AutoCAD sources, then rerun them from Map Studio > campus > Floor plan sources > Configure.

Alternative to step 4 for spaces only: re-attach the CSV and click **Load All Records** then **Run Transform** on the data source. The transform rebuilds site, campus, building, floors, spaces, departments and profiles (new sys_ids).

## 6. Check

- 50 spaces where `wsd_source = TRIRIGA`; 4 neighborhoods; 9 reservations.
- Workplace Central > Summit Tower stack plan by Neighborhood shows three teams per floor.
- Map Studio Preview shows Floors 10 and 11.
- Your admin user needs `sn_wsd_core.admin` and `sn_wsd_core.workplace_user` for the Employee Center booking page; log out and back in after adding roles.
