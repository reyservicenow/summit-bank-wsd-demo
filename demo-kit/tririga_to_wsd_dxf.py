"""Convert a TRIRIGA CAD Integrator-style floor plan into a WSD-ready DXF.

TRIRIGA style : space outlines are polylines on A-Area-Space, room IDs are plain
                TEXT on A-Area-Iden.
WSD Core style: each space is a BLOCK reference whose ATTRIBUTES carry the data
                (e.g. SPACE_ID), which the floor-plan upload maps to space fields.

Usage: python3 tririga_to_wsd_dxf.py <in.dxf> <out.dxf>
"""
import sys
import ezdxf

SPACE_LAYER, LABEL_LAYER, OUT_LAYER = "A-Area-Space", "A-Area-Iden", "WSD-SPACES"


def text_point(t):
    if t.dxf.hasattr("align_point") and (t.dxf.halign or t.dxf.valign):
        return tuple(t.dxf.align_point)[:2]
    return tuple(t.dxf.insert)[:2]


def convert(src, dst):
    doc = ezdxf.readfile(src)
    msp = doc.modelspace()
    if OUT_LAYER not in doc.layers:
        doc.layers.add(OUT_LAYER, color=4)
    labels = [t for t in msp.query("TEXT") if t.dxf.layer == LABEL_LAYER]
    converted, skipped = 0, []
    for pl in list(msp.query(f'LWPOLYLINE[layer=="{SPACE_LAYER}"]')):
        pts = [(p[0], p[1]) for p in pl.get_points()]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        inner = [t for t in labels if min(xs) <= text_point(t)[0] <= max(xs) and min(ys) <= text_point(t)[1] <= max(ys)]
        if not pl.closed or len(inner) != 1:
            skipped.append(pts[0])
            continue
        sid = inner[0].dxf.text
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        name = "SPACE_" + "".join(c if c.isalnum() else "_" for c in sid)
        blk = doc.blocks.new(name=name, base_point=(0, 0))
        blk.add_lwpolyline([(x - cx, y - cy) for x, y in pts], close=True, dxfattribs={"layer": "0"})
        blk.add_attdef("SPACE_ID", insert=(0, 0), height=1.0, dxfattribs={"layer": "0"})
        ins = msp.add_blockref(name, (cx, cy), dxfattribs={"layer": OUT_LAYER})
        ins.add_auto_attribs({"SPACE_ID": sid})
        msp.delete_entity(pl)
        msp.delete_entity(inner[0])
        labels.remove(inner[0])
        converted += 1
    doc.saveas(dst)
    print(f"{src} -> {dst}: {converted} spaces converted to blocks with SPACE_ID attributes"
          + (f", {len(skipped)} skipped (open outline or missing/duplicate label)" if skipped else ""))


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
