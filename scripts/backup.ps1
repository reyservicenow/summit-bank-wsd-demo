# Summit Bank WSD demo – BACKUP STEPS 2 and 3 (Windows PowerShell 5+ / PowerShell 7)
#
#   Step 2: downloads every update set listed in backups\export-links.txt
#           (paste the EXPORT lines printed by instance-scripts\01_export_update_sets.js)
#   Step 3: exports the demo DATA records (instance-scripts\data-tables.txt) as XML
#
# Usage:  .\scripts\backup.ps1 -Instance dev445147
param([string]$Instance = "dev445147")
$ErrorActionPreference = "Stop"

$Root  = Split-Path -Parent $PSScriptRoot
$Base  = "https://$Instance.service-now.com"
$Stamp = Get-Date -Format "yyyy-MM-dd"
$Out   = Join-Path $Root "backups\$Stamp"
New-Item -ItemType Directory -Force -Path "$Out\update-sets", "$Out\data" | Out-Null

$Cred = Get-Credential -Message "ServiceNow login for $Instance" -UserName "admin"
$Pair = "$($Cred.UserName):$($Cred.GetNetworkCredential().Password)"
$Headers = @{ Authorization = "Basic " + [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Pair)) }

try { Invoke-WebRequest -UseBasicParsing -Headers $Headers -Uri "$Base/api/now/table/sys_user?sysparm_limit=1" | Out-Null }
catch { Write-Host "Login failed. Is the instance awake? Wake it at developer.servicenow.com."; exit 1 }

# --- step 2: update sets
$Links = Join-Path $Root "backups\export-links.txt"
if (Test-Path $Links) {
  Write-Host "== Update sets"
  Get-Content $Links | Where-Object { $_ -like "EXPORT|*" } | ForEach-Object {
    $p = $_.Split("|"); $name = $p[1]; $count = $p[4]; $url = $p[5]
    $safe = ($name -replace '[^A-Za-z0-9._-]', '_').TrimEnd('_')
    $file = "$Out\update-sets\$safe.xml"
    try {
      Invoke-WebRequest -UseBasicParsing -Headers $Headers -Uri $url -OutFile $file
      if (Select-String -Path $file -Pattern "<sys_remote_update_set" -Quiet) { Write-Host "  OK  $name ($count changes)" }
      else { throw "not an update set file" }
    } catch { Write-Host "  FAIL $name - open in your browser instead: $url"; Remove-Item $file -ErrorAction SilentlyContinue }
  }
} else { Write-Host "== Update sets: skipped (run instance-scripts\01_export_update_sets.js and save backups\export-links.txt first)" }

# --- step 3: data records
Write-Host "== Data records"
Get-Content (Join-Path $Root "instance-scripts\data-tables.txt") | Where-Object { $_ -and -not $_.StartsWith("#") } | ForEach-Object {
  $p = $_.Split("|"); $fname = $p[0]; $table = $p[1]; $query = [Uri]::EscapeDataString($p[2])
  $file = "$Out\data\$fname.xml"
  try {
    Invoke-WebRequest -UseBasicParsing -Headers $Headers -Uri "$Base/${table}_list.do?UNL&sysparm_query=$query" -OutFile $file
    $n = (Select-String -Path $file -Pattern "<$table action=" -AllMatches).Matches.Count
    Write-Host "  OK  $fname ($table): $n records"
  } catch { Write-Host "  FAIL $fname ($table)"; Remove-Item $file -ErrorAction SilentlyContinue }
}

# --- inventory
$q = [Uri]::EscapeDataString("scopeSTARTSWITHsn_wsd^ORscopeSTARTSWITHsn_map")
Invoke-WebRequest -UseBasicParsing -Headers $Headers -OutFile "$Out\installed-store-apps.json" `
  -Uri "$Base/api/now/table/sys_store_app?sysparm_query=$q&sysparm_fields=name,scope,version,active"

Write-Host "`nBackup written to backups\$Stamp"
Write-Host "Next: git add backups; git commit -m `"Backup $Stamp`"; git push"
