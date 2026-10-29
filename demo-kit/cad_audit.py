"""CAD readiness audit for ServiceNow WSD Indoor Mapping (Map Studio).

Checks each DXF floor plan before import:
  1. Required layers exist (space outlines + space labels)
  2. Every space outline is a CLOSED polyline
  3. Every outline has exactly one label inside it
  4. Labels sit on the label layer (not stray layers)
  5. Labels match the space IDs in the TRIRIGA export (optional)

Usage:  python3 cad_audit.py <floor.dxf> [<floor2.dxf> ...] [--tririga tririga_space_export.csv]
"""
import csv
import sys
import ezdxf

SPACE_LAYER = "A-Area-Space"
LABEL_LAYER = "A-Area-Iden"


def inside(pt, pts):
    x, y = pt
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs) <= x <= max(xs) and min(ys) <= y <= max(ys)


def text_point(t):
    if t.dxftype() == "TEXT" and t.dxf.hasattr("align_point") and (t.dxf.halign or t.dxf.valign):
        return tuple(t.dxf.align_point)[:2]
    return tuple(t.dxf.insert)[:2]


def audit(path, tririga_ids):
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    issues, ok = [], 0
    # Map Studio's CAD importer failed on an R12 file with no $INSUNITS; R2000+ with units imported cleanly
    if doc.dxfversion < "AC1015":
        issues.append(f"DXF version {doc.dxfversion} is older than R2000; re-save as R2000 or newer")
    if not doc.header.get("$INSUNITS", 0):
        issues.append("Drawing units ($INSUNITS) not set; set units (e.g. feet) before import")
    layers = {l.dxf.name for l in doc.layers}
    for need in (SPACE_LAYER, LABEL_LAYER):
        if need not in layers:
            issues.append(f"Missing layer {need}")

    outlines = [p for p in msp.query(f'LWPOLYLINE[layer=="{SPACE_LAYER}"]')]
    labels = [t for t in msp.query("TEXT MTEXT") if t.dxf.layer == LABEL_LAYER]
    stray = [t for t in msp.query("TEXT MTEXT") if t.dxf.layer != LABEL_LAYER]

    found_ids = []
    for i, pl in enumerate(outlines, 1):
        pts = [(p[0], p[1]) for p in pl.get_points()]
        tag = f"Outline #{i} at ({pts[0][0]:.0f},{pts[0][1]:.0f})"
        if not pl.closed:
            issues.append(f"{tag}: polyline is not closed")
            continue
        inner = [t for t in labels if inside(text_point(t), pts)]
        if not inner:
            issues.append(f"{tag}: no space label inside")
        elif len(inner) > 1:
            issues.append(f"{tag}: {len(inner)} labels inside")
        else:
            sid = inner[0].dxf.text if inner[0].dxftype() == "TEXT" else inner[0].text
            found_ids.append(sid)
            if tririga_ids is not None and sid not in tririga_ids:
                issues.append(f"{tag}: label '{sid}' not found in TRIRIGA export")
            else:
                ok += 1
    for t in stray:
        txt = t.dxf.text if t.dxftype() == "TEXT" else t.text
        issues.append(f"Label '{txt}' is on layer '{t.dxf.layer}', expected {LABEL_LAYER}")

    total = len(outlines)
    score = round(100 * ok / total) if total else 0
    status = "READY" if not issues else ("NEEDS CLEANUP" if score >= 50 else "NOT READY")
    print(f"\n{path}\n  Spaces: {total}  |  Clean: {ok}  |  Score: {score}%  |  {status}")
    for msg in issues:
        print(f"   - {msg}")
    return found_ids


if __name__ == "__main__":
    args = sys.argv[1:]
    tririga_ids = None
    if "--tririga" in args:
        i = args.index("--tririga")
        with open(args[i + 1]) as f:
            tririga_ids = {r["triSpaceID"] for r in csv.DictReader(f)}
        args = args[:i] + args[i + 2:]
    for p in args:
        audit(p, tririga_ids)
