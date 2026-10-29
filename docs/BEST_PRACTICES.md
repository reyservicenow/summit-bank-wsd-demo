# Backup best practices applied here

Summary of the ServiceNow guidance this backup follows, with sources.

## Custom application → Publish to Update Set

- Publishing a scoped app to an update set copies the **current version of every app file** into a new update set and marks it Complete. ServiceNow names this as a way to keep an audit backup of the app or move it to another instance.
- Give it a version (for example `1.0.0`); later publishes are numbered on from there.
- Leave **Include data** off: it only packages a limited sample of data records, and ServiceNow advises against it for data migration.
- Requires admin, or delegated developer with the Publish To Update Set permission.

Source: [Publish an application to an Update Set](https://www.servicenow.com/docs/r/application-development/t_PublishApplicationsToAnUpdateSet.html)

## Update sets → Export to XML

- Local update sets must be **Complete** before the *Export to XML* related link is offered. `01_export_update_sets.js` uses the same export code as that link, so it also works on In progress sets; set `MARK_COMPLETE = true` to follow the rule strictly.
- Restore: elevate to `security_admin`, Retrieved Update Sets > Import Update Set from XML, then preview and commit.
- Saving update sets as XML is the documented way to back up customizations or move them without a connection between instances.

Sources: [Save an update set as an XML file](https://docs.servicenow.com/bundle/paris-application-development/page/build/system-update-sets/task/t_SaveAnUpdateSetAsAnXMLFile.html) · [Exploring system update sets](https://www.servicenow.com/docs/r/application-development/system-update-sets/exploring-system-update-sets.html)

## Data → XML export (unload format)

- Update sets carry configuration, not data. Small sets of data records are moved with list **Export > XML** and **Import XML**.
- XML keeps sys_ids and created/updated dates, so references survive.
- Import skips business rules and does no transformation, and image fields are not preserved. Use import sets instead when data must be validated or transformed.
- Recommended for small, infrequent batches like this demo (about 200 records).

Source: [Export and import XML files](https://www.servicenow.com/docs/r/zurich/platform-administration/table-administration-and-data-management/c_ExportAndImportXMLFiles.html)

## Optional: Studio source control (ongoing backup)

ServiceNow Studio can link a scoped app to a Git repository and commit app files to a branch:

- Use a dedicated repository for the app and a GitHub personal access token limited to that repo, stored as a basic auth credential.
- Studio > app > App details > Source control > **Link to source control** > HTTPS URL, branch, credential, default email.
- Only on non-production instances. Every user who commits needs an email on their user record.
- It backs up the app files only. Data and the other update sets still need the XML backup above.

Source: [Link an app to source control in ServiceNow Studio](https://www.servicenow.com/docs/r/9Lur8HBNLjdzEcjznSAFzA/AJB3RRVvlbN9W7aSTZbKvw)

## Other habits

- One update set per piece of work, named for it (here: *Summit Bank WSD Demo - TRIRIGA migration*), and the application picker set to the app before changing anything. This demo already hit the cost of skipping that: early changes landed in the Vehicle Tracking app.
- Back up again after each meaningful change, and before a developer instance is likely to be reclaimed (inactive for about 10 days).
- Keep the repository private.
