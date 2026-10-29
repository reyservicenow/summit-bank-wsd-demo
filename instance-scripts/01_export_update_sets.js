/*
 * Summit Bank WSD demo – BACKUP STEP 1: export update sets to XML
 *
 * Run in: System Definition > Scripts - Background, scope = global, as admin.
 *
 * What it does
 *   1. Finds every local update set that has changes since SINCE.
 *   2. Optionally marks them Complete first (ServiceNow requires local update sets
 *      to be Complete before the "Export to XML" related link appears).
 *   3. Makes the same export copy the "Export to XML" UI action makes
 *      (UpdateSetExport -> sys_remote_update_set) and prints one download link per set.
 *
 * After it runs
 *   - Click each EXPORT link while logged in (the browser saves an .xml file), OR
 *   - copy the EXPORT lines into backups/export-links.txt and run
 *     scripts/download-update-sets.sh (Mac/Linux) or scripts/download-update-sets.ps1 (Windows).
 *   Each link deletes its temporary export copy after the download (delete_when_done=true).
 *
 * Run "Publish to Update Set" on the Summit Bank WSD Demo app BEFORE this script,
 * so the published app update set is included (see README step 1).
 */

var SINCE = '2026-10-28 00:00:00';   // changes on or after this date (UTC)
var MARK_COMPLETE = false;            // true = set each update set to Complete before export
var SKIP_NAMES = [];                  // e.g. ['Default'] to leave out Default update sets

var base = gs.getProperty('glide.servlet.uri');   // https://<instance>.service-now.com/

var sets = [];
var ga = new GlideAggregate('sys_update_xml');
ga.addQuery('sys_updated_on', '>=', SINCE);
ga.addNotNullQuery('update_set');
ga.addAggregate('COUNT');
ga.groupBy('update_set');
ga.query();
while (ga.next()) {
    sets.push({ id: ga.getValue('update_set'), count: ga.getAggregate('COUNT') });
}

gs.print('Update sets with changes since ' + SINCE + ': ' + sets.length);
gs.print('Format: EXPORT|name|application|state|changes|download URL');

var exporter = new UpdateSetExport();
sets.forEach(function (s) {
    var us = new GlideRecord('sys_update_set');
    if (!us.get(s.id)) return;
    if (SKIP_NAMES.indexOf(us.getValue('name')) > -1) return;
    if (MARK_COMPLETE && us.getValue('state') != 'complete') {
        us.setValue('state', 'complete');
        us.update();
    }
    var remoteId = exporter.exportUpdateSet(us);
    gs.print('EXPORT|' + us.getValue('name') + '|' + us.application.getDisplayValue() + '|' +
        us.getValue('state') + '|' + s.count + '|' + base +
        'export_update_set.do?sysparm_sys_id=' + remoteId + '&sysparm_delete_when_done=true');
});

gs.print('Done. Download every EXPORT link above.');
