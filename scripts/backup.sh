#!/usr/bin/env bash
# Summit Bank WSD demo – BACKUP STEPS 2 and 3 (Mac / Linux / Git Bash)
#
#   Step 2: downloads every update set listed in backups/export-links.txt
#           (paste the EXPORT lines printed by instance-scripts/01_export_update_sets.js)
#   Step 3: exports the demo DATA records (instance-scripts/data-tables.txt) as XML
#
# Usage:  ./scripts/backup.sh [instance]        e.g. ./scripts/backup.sh dev445147
# The password is asked for and never written to disk.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INSTANCE="${1:-dev445147}"
BASE="https://${INSTANCE}.service-now.com"
STAMP="$(date +%Y-%m-%d)"
OUT="$ROOT/backups/$STAMP"
mkdir -p "$OUT/update-sets" "$OUT/data"

read -r -p "ServiceNow user [admin]: " SN_USER; SN_USER="${SN_USER:-admin}"
read -r -s -p "Password for $SN_USER@$INSTANCE: " SN_PASS; echo
AUTH=(-u "$SN_USER:$SN_PASS")

# --- quick login check ---------------------------------------------------------
code=$(curl -s -o /dev/null -w '%{http_code}' "${AUTH[@]}" \
  "$BASE/api/now/table/sys_user?sysparm_limit=1&sysparm_fields=sys_id")
if [ "$code" != "200" ]; then
  echo "Login failed (HTTP $code). Is the instance awake? Wake it at developer.servicenow.com."; exit 1
fi

# --- step 2: update sets -------------------------------------------------------
LINKS="$ROOT/backups/export-links.txt"
if [ -s "$LINKS" ]; then
  echo "== Update sets"
  grep '^EXPORT|' "$LINKS" | while IFS='|' read -r _ name app state count url; do
    safe=$(echo "$name" | tr -c 'A-Za-z0-9._-' '_' | sed 's/_*$//')
    file="$OUT/update-sets/${safe}.xml"
    if curl -fsS "${AUTH[@]}" "$url" -o "$file" && grep -q '<sys_remote_update_set' "$file"; then
      echo "  OK  $name ($count changes) -> update-sets/${safe}.xml"
    else
      echo "  FAIL $name – open this link in your browser instead: $url"; rm -f "$file"
    fi
  done
else
  echo "== Update sets: skipped (no backups/export-links.txt – run instance-scripts/01_export_update_sets.js first)"
fi

# --- step 3: data records ------------------------------------------------------
echo "== Data records"
grep -v '^#' "$ROOT/instance-scripts/data-tables.txt" | grep -v '^$' | while IFS='|' read -r fname table query; do
  file="$OUT/data/${fname}.xml"
  if curl -fsS -G "${AUTH[@]}" "$BASE/${table}_list.do" \
       --data-urlencode "UNL" --data-urlencode "sysparm_query=${query}" -o "$file"; then
    n=$(grep -c "<${table} action=" "$file" || true)
    echo "  OK  $fname ($table): $n records"
  else
    echo "  FAIL $fname ($table)"; rm -f "$file"
  fi
done

# --- inventory -----------------------------------------------------------------
curl -fsS -G "${AUTH[@]}" "$BASE/api/now/table/sys_store_app" \
  --data-urlencode "sysparm_query=scopeSTARTSWITHsn_wsd^ORscopeSTARTSWITHsn_map" \
  --data-urlencode "sysparm_fields=name,scope,version,active" -o "$OUT/installed-store-apps.json" \
  && echo "== Saved list of installed WSD / map store apps and versions"

unset SN_PASS
echo
echo "Backup written to backups/$STAMP"
echo "Next: git add backups && git commit -m \"Backup $STAMP\" && git push"
