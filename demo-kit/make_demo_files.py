"""Builds the sample TRIRIGA export (CSV) and a TRIRIGA-style CAD floor plan (DXF)
for the WSD migration demo. All data is fictional ("Summit Bank")."""
import csv
import ezdxf

BUILDING = "Summit Tower"
FLOORS = ["Floor 10", "Floor 11"]

# ---- Floor layout (same grid both floors): name, type, x, y, w, h, capacity, reservable
def layout(floor_no):
    rooms = []
    # 2 rows of 8 desks
    for row, y in enumerate([10, 22]):
        for i in range(8):
            n = f"{floor_no}-D{row * 8 + i + 1:02d}"
            rooms.append((n, "Desk", 10 + i * 8, y, 6, 6, 1, True))
    # meeting rooms along the bottom
    rooms.append((f"{floor_no}-MR1 Blue Ridge", "Meeting room", 10, 34, 18, 12, 8, True))
    rooms.append((f"{floor_no}-MR2 Piedmont", "Meeting room", 30, 34, 14, 12, 6, True))
    rooms.append((f"{floor_no}-FOCUS1", "Focus room", 46, 34, 8, 12, 1, True))
    # private offices along the right
    for j in range(3):
        rooms.append((f"{floor_no}-OFF{j + 1}", "Office", 78, 10 + j * 12, 12, 10, 1, False))
    rooms.append((f"{floor_no}-BRK", "Break room", 56, 34, 18, 12, 12, False))
    return rooms

DEPTS = ["Retail Banking", "Wealth Management", "Technology", "Risk & Compliance"]
PEOPLE = ["abel.tuter", "abraham.lincoln", "beth.anglin", "bud.richman", "fred.luddy",
          "charlie.whitherspoon", "david.loo", "don.goodliffe"]

# ---- 1. TRIRIGA-style export (column names mimic TRIRIGA triBuilding/triFloor/triSpace fields)
with open("tririga_space_export.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["triPropertyName", "triBuildingName", "triFloorName", "triSpaceID",
                "triSpaceClass", "triAreaNU", "triCapacityNU", "triReservableBL",
                "triOrgName", "triPrimaryOccupant", "triStatus"])
    k = 0
    for fi, floor in enumerate(FLOORS):
        fno = floor.split()[1]
        for (n, t, x, y, wd, ht, cap, res) in layout(fno):
            dept = DEPTS[(k // 6) % len(DEPTS)]
            occ = PEOPLE[k % len(PEOPLE)] if t == "Office" else ""
            w.writerow(["Summit Bank Charlotte Campus", BUILDING, floor, n, t,
                        wd * ht, cap, "TRUE" if res else "FALSE", dept, occ, "Active"])
            k += 1
    # Floor 12 exists in TRIRIGA, but its CAD file is messy (see section 3)
    for d in range(1, 5):
        w.writerow(["Summit Bank Charlotte Campus", BUILDING, "Floor 12", f"12-D{d:02d}", "Desk",
                    100, 1, "TRUE", "Technology", "", "Active"])

# ---- 2. TRIRIGA CAD Integrator-style DXF, one per floor
for floor in FLOORS:
    fno = floor.split()[1]
    doc = ezdxf.new("R2018", setup=True)
    doc.units = ezdxf.units.FT
    msp = doc.modelspace()
    for name, color in [("ASF", 1), ("GSFI", 3), ("A-Area-Space", 5), ("A-Area-Iden", 2), ("A-Wall", 8)]:
        doc.layers.add(name, color=color)
    # gross outline + interior outline
    msp.add_lwpolyline([(0, 0), (100, 0), (100, 55), (0, 55)], close=True, dxfattribs={"layer": "ASF"})
    msp.add_lwpolyline([(2, 2), (98, 2), (98, 53), (2, 53)], close=True, dxfattribs={"layer": "GSFI"})
    for (n, t, x, y, wd, ht, cap, res) in layout(fno):
        msp.add_lwpolyline([(x, y), (x + wd, y), (x + wd, y + ht), (x, y + ht)], close=True,
                           dxfattribs={"layer": "A-Area-Space"})
        msp.add_text(n, height=1.0, dxfattribs={"layer": "A-Area-Iden"}).set_placement(
            (x + wd / 2, y + ht / 2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    doc.saveas(f"summit_tower_{fno}.dxf")

# ---- 3. A deliberately "messy" floor to show what the audit catches
doc = ezdxf.new("R2018", setup=True)
msp = doc.modelspace()
doc.layers.add("A-Area-Space"); doc.layers.add("A-Area-Iden"); doc.layers.add("0-MISC")
msp.add_lwpolyline([(0, 0), (10, 0), (10, 10), (0, 10)], close=True, dxfattribs={"layer": "A-Area-Space"})
msp.add_text("12-D01", height=1, dxfattribs={"layer": "A-Area-Iden"}).set_placement((5, 5))
msp.add_lwpolyline([(12, 0), (22, 0), (22, 10), (12, 10)], close=False, dxfattribs={"layer": "A-Area-Space"})  # open outline
msp.add_lwpolyline([(24, 0), (34, 0), (34, 10), (24, 10)], close=True, dxfattribs={"layer": "A-Area-Space"})    # no label
msp.add_text("12-D04", height=1, dxfattribs={"layer": "0-MISC"}).set_placement((41, 5))                       # wrong layer
msp.add_lwpolyline([(36, 0), (46, 0), (46, 10), (36, 10)], close=True, dxfattribs={"layer": "A-Area-Space"})
msp.add_text("12-D99", height=1, dxfattribs={"layer": "A-Area-Iden"}).set_placement((41, 5))                  # not in TRIRIGA
doc.saveas("summit_tower_12_messy.dxf")
print("done")
