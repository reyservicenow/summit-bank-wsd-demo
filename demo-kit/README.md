Summit Bank – TRIRIGA to ServiceNow WSD demo kit (fictional data)

tririga_space_export.csv      Sample TRIRIGA space export (50 spaces, 3 floors) loaded into WSD on dev445147
summit_tower_10.dxf / _11     TRIRIGA CAD Integrator-style floor plans (A-Area-Space outlines + A-Area-Iden labels)
summit_tower_12_messy.dxf     A floor with typical CAD problems (open outline, missing label, wrong layer, unknown ID)
*_wsd_ready.dxf               Same floors converted to WSD block + attribute format (SPACE_ID)
*.png                         Rendered previews of the floor plans
cad_audit.py                  CAD readiness audit:  python3 cad_audit.py *.dxf --tririga tririga_space_export.csv
tririga_to_wsd_dxf.py         Converter:            python3 tririga_to_wsd_dxf.py in.dxf out.dxf
make_demo_files.py            Regenerates the CSV and DXF files
audit_output.txt              Last audit run

Needs: pip install ezdxf
