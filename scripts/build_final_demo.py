#!/usr/bin/env python3
"""FIN-01: rebuild the public seven-slide English PDF with REAL FireLens screenshots.

Inputs: fresh browser captures of the actual deployed UI served locally,
       audited static TEST-02 JSON, and existing scientific results.
No generated or invented satellite detections. AI-assisted layout credit.
"""
from __future__ import annotations
import datetime as dt
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader, simpleSplit
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

W,H=960,540
BG="#0a1822";SURFACE="#142936";ACC="#ff9568";CYAN="#80e0d9";WHITE="#f4f8f8";MUTED="#b3c7d0";LINE="#2d4a55"
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/"demo"/"FireLens_7_Slide_Demo_2026.pdf"
CASE=json.loads((ROOT/"data"/"caso_visao_aguia_20261110.json").read_text())
TEST=json.loads((ROOT/"data"/"test02_resultados.json").read_text())
SCI03=json.loads((ROOT/"data"/"sci03_agregados.json").read_text(encoding="utf-8"))
TEAM=[
    "Crhystopher Ferreira de Aguiar",
    "Eder Magalhães dos Santos",
    "Leonardo de Souza Pinheiro",
    "Luís Henrique da Silva Carvalho",
    "Mirna do Amaral Maquiné Nascimento",
    "Paulo Elias Cajado Pinto",
]
assert SCI03["id"]=="SCI-03" and len(SCI03["rows"])==4434
assert SCI03["columns"]==["year","month","sensor","cell_south_lat","cell_west_lon","pixels"]
assert set((r[0],r[1],r[2]) for r in SCI03["rows"])=={
    (year,month,sensor)
    for year in (2023,2024,2025,2026)
    for month in range(1,11)
    for sensor in ("Aqua","NOAA20")
}
SEPT_2026={sensor:sum(r[5] for r in SCI03["rows"]
                           if r[0]==2026 and r[1]==9 and r[2]==sensor)
           for sensor in ("Aqua","NOAA20")}
assert SEPT_2026=={"Aqua":3518,"NOAA20":16489},SEPT_2026
# Embed one Unicode font solely for the six exact accented names.
font_candidates=[
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
]
name_font_path=next((p for p in font_candidates if p.exists()),None)
if name_font_path is None:
    raise RuntimeError("Unicode TrueType font unavailable for exact team-name rendering")
pdfmetrics.registerFont(TTFont("FireLensTeam",str(name_font_path)))
assert CASE["analysis"]["identity_confirmed"] is False
assert len(CASE["records"])==3
assert CASE["analysis"]["delta_minutes"]==107
assert abs(CASE["analysis"]["viirs_frp_sum_mw"]-13.09)<1e-8
d11=next(x for x in TEST["daily"] if x["date_utc"]=="2026-11-11")
assert d11["eligible_diurnal_modis_aqua"]==12
assert d11["eligible_diurnal_noaa20"]==222
assert d11["four_locks_candidate_groups_8k"]==0
for file in ("/tmp/firelens_recent.png","/tmp/firelens_eagle.png","/tmp/firelens_history.png"):
    assert Path(file).is_file() and Path(file).stat().st_size>1000,file

c=canvas.Canvas(str(DEST),pagesize=(W,H),pageCompression=1)
c.setTitle("FireLens | 7-slide Project Demo | DEMO-02")
c.setAuthor("Stack Manauara | AI-assisted slide layout and text")
c.setSubject("NASA FIRMS MODIS/VIIRS observations; real 2026 candidate association, not confirmed physical fire identity")

def color(hex):
    c.setFillColor(hex)
def strok(hex):
    c.setStrokeColor(hex)
def rbox(x,y,w,h,fill=SURFACE,stroke=LINE,r=16):
    color(fill);strok(stroke);c.roundRect(x,y,w,h,r,fill=1,stroke=1)
def txt(s,x,y,size=18,col=WHITE,bold=False):
    color(col);c.setFont("Helvetica-Bold" if bold else "Helvetica",size)
    c.drawString(x,y,str(s))
def wrapped(text,x,top,maxw,fontsize=14,leading=20,col=MUTED,bold=False,maxlines=10):
    lines=simpleSplit(text,"Helvetica-Bold" if bold else "Helvetica",fontsize,maxw)
    color(col);c.setFont("Helvetica-Bold" if bold else "Helvetica",fontsize)
    for i,line in enumerate(lines[:maxlines]):
        c.drawString(x,top-i*leading,line)
    return top-len(lines[:maxlines])*leading
def title(s,kicker,n):
    color(BG);c.rect(0,0,W,H,fill=1,stroke=0)
    color(ACC);c.roundRect(40,H-78,5,33,2,fill=1,stroke=0)
    txt(kicker.upper(),59,H-48,11,ACC,True)
    txt(s,59,H-83,27,WHITE,True)
    strok(LINE);c.line(45,45,W-45,45)
    txt("FIRELENS  /  STACK MANAUARA",48,25,9,CYAN,True)
    txt("NASA FIRMS data  |  AI-assisted slides  |  Independent team project",278,25,8,MUTED)
    txt(str(n)+" / 7",885,25,9,MUTED)
def team_name(s,x,y,size=11.8):
    if pdfmetrics.stringWidth(s,"FireLensTeam",size)>365:
        raise ValueError("Team name does not fit its slide column: "+s)
    color(WHITE);c.setFont("FireLensTeam",size);c.drawString(x,y,s)

def arrow(x,y,endx):
    strok(CYAN);c.setLineWidth(2);c.line(x,y,endx,y)
    c.line(endx-7,y+4,endx,y);c.line(endx-7,y-4,endx,y)
def photo(path,x,y,w,h):
    im=Image.open(path).convert("RGB")
    iw,ih=im.size
    ratio=min(w/iw,h/ih)
    ww,hh=iw*ratio,ih*ratio
    rbox(x-5,y-5,w+10,h+10,"#10202a","#4a6470",10)
    c.drawImage(ImageReader(im),x+(w-ww)/2,y+(h-hh)/2,width=ww,height=hh,preserveAspectRatio=True,mask='auto')

# 1: FireLens and all six correctly accented team members
title("FireLens","NASA SPACE APPS CHALLENGE 2026",1)
txt("Harmonization of MODIS and VIIRS Hot Spots",70,402,19,CYAN,True)
txt("One clearer view of satellite observations.",70,359,23,WHITE,True)
wrapped("An interactive NASA FIRMS map, an Amazonas monthly history, and an honest observation-level MODIS / VIIRS case.",70,320,814,14,20,MUTED,maxlines=2)
rbox(68,91,823,170,"#173541","#3b7475",12)
txt("STACK MANAUARA  /  THE SIX TEAM MEMBERS",89,229,12,CYAN,True)
for idx,name in enumerate(TEAM):
    col=idx//3;row=idx%3
    team_name(name,89+col*399,195-row*30,11.8)
c.showPage()

# 2: Live map
title("01  |  Start with the map","THREE AREAS / MAP",2)
photo("/tmp/firelens_recent.png",45,82,600,335)
txt("NASA FIRMS NRT",682,385,15,CYAN,True)
wrapped("The live map plots real NOAA-20 and NOAA-21 detections.",682,358,226,14,19,WHITE,maxlines=4)
wrapped("Choose a point. First read a plain-language explanation; open measurements only when needed.",682,263,226,13,18,MUTED,maxlines=7)
wrapped("Observation time is different from retrieval time. A stored snapshot may be outdated.",682,160,226,12,17,ACC,maxlines=5)
c.showPage()

# 3: The eagle example with real screenshot
title("02  |  Eagle's View: a real 2026 case","ARCHIVED RESEARCH / NOT LIVE",3)
photo("/tmp/firelens_eagle.png",45,83,594,334)
txt("10 NOV 2026",674,390,14,CYAN,True)
txt("MODIS Aqua",674,355,15,WHITE,True)
txt("15:49 AMT  /  18.62 MW",674,329,13,MUTED)
txt("VIIRS NOAA-20",674,284,15,WHITE,True)
txt("14:02 AMT  /  13.09 MW",674,258,13,MUTED)
rbox(668,144,235,69,"#213844","#3f6d71",9)
txt("107 minutes apart",685,185,16,CYAN,True)
wrapped("Nearby detections, NOT a confirmed same fire.",685,166,199,11,15,WHITE,maxlines=2)
wrapped("1 MODIS pixel + 2 VIIRS pixels. Distinct from current NOAA-20/21 NRT.",670,122,229,11,15,MUTED,maxlines=3)
c.showPage()

# 4: physical measurement explanations
title("03  |  What can we compare?","OBSERVED / INTERPRETED / NOT PROVEN",4)
cards=[
("01","APPROXIMATE GEOMETRY","scan x track suggests pixel dimensions, not exact oriented satellite footprints."),
("02","OBSERVATION TIME","VIIRS 18:02 UTC; Aqua 19:49 UTC. 107 minutes apart is compatible, not proof."),
("03","BRIGHTNESS TEMPERATURE","MODIS T31: 297.36 K. Mean VIIRS TI5: 293.98 K. Different channels."),
("04","RADIATIVE POWER","FRP Aqua: 18.62 MW. Sum VIIRS: 13.09 MW; difference: 5.53 MW. Not conserved energy.")
]
for i,(num_,h,body) in enumerate(cards):
    col=i%2;row=i//2;xx=55+col*452;yy=285-row*179
    rbox(xx,yy,424,162)
    txt(num_,xx+18,yy+123,13,ACC,True)
    txt(h,xx+56,yy+123,15,WHITE,True)
    wrapped(body,xx+18,yy+91,380,13,21,MUTED,maxlines=4)
txt("These four observations are descriptive tests, not four proofs of physical fire identity.",59,63,12,CYAN,True)
c.showPage()

# 5: refreshed HIST-02: actual state calendar, not the hidden pilot A/B view
title("04  |  Amazonas: the updated history","HIST-02 / NASA FIRMS 2023-2026",5)
photo("/tmp/firelens_history.png",45,91,590,326)
txt("AMAZONAS",668,385,16,CYAN,True)
txt("Jan-Oct 2023-2026",668,359,15,WHITE,True)
wrapped("MODIS Aqua and VIIRS NOAA-20 are selectable separately.",668,328,229,12,18,MUTED,maxlines=3)
wrapped("2026 is PARTIAL. SP and provisional NRT are labeled by month.",668,260,230,12,18,ACC,maxlines=3)
wrapped("Nov-Dec are unavailable in this dataset, NOT months without fire.",668,198,230,12,17,MUTED,maxlines=4)
txt("Separate pilot: A/B, 2022-2024",668,118,11,CYAN,True)
wrapped("Different regions and filters; not combined with statewide counts.",668,98,229,10,13,MUTED,maxlines=3)
c.showPage()

# 6: source validation and caveat
title("05  |  The difference is part of the finding","NASA FIRMS / 10-14 NOV 2026",6)
rbox(62,257,386,153,"#152d38","#3f626b")
txt("10 NOVEMBER",88,370,14,CYAN,True)
txt("2 candidate association groups",88,329,19,WHITE,True)
wrapped("Both passed exploratory proximity, time, T11 and FRP comparisons. Neither was proven to be one physical fire.",88,300,328,12,17,MUTED,maxlines=4)
rbox(475,257,421,153,"#152d38","#3f626b")
txt("11 NOVEMBER",504,370,14,ACC,True)
txt("12 Aqua  /  222 NOAA-20",504,329,19,WHITE,True)
wrapped("Eligible daytime detections; zero groups met all four exploratory criteria within 120 minutes.",504,300,355,12,17,MUTED,maxlines=4)
txt("Evidence can be reproduced.",70,208,20,WHITE,True)
wrapped("Source-verified NASA fields, versioned methods, original SCI-03 records and automated tests are public.",70,174,810,14,20,MUTED,maxlines=3)
txt("Historical global scaling: held-out WAPE rose from 23.11% (2024) to 50.73% (2025).",70,123,12,ACC,True)
txt("github.com/Emds96/firelens-stack-manauara",70,91,15,CYAN,True)
c.showPage()

# 7: limitations, credit and clear ending
title("06  |  Useful evidence needs honest limits","CLEAR SCIENCE / ACCESSIBLE INTERFACE",7)
statements=[
("OBSERVED","Satellite-detected thermal pixels, times, source products and measurement fields."),
("CANDIDATE","Spatial-temporal proximity with descriptive T31/TI5 and FRP comparisons."),
("NOT PROVEN","A single shared fire, understory fire, a smoke source, burned area or validated physical harmonization.")
]
for i,(label,body) in enumerate(statements):
    y=353-94*i
    rbox(55,y,850,78,"#152b36","#35515e",10)
    txt(label,74,y+48,13,CYAN if i<2 else ACC,True)
    wrapped(body,222,y+48,647,12,17,WHITE,maxlines=2)
txt("Open the map  |  Explore a case  |  Learn the limits",66,103,20,WHITE,True)
txt("emds96.github.io/firelens-stack-manauara/",66,76,13,CYAN,True)
wrapped("Data: NASA FIRMS. Map: OpenStreetMap contributors. ChatGPT assisted with slides and code. FireLens is an independent project, not endorsed by NASA.",65,60,820,9,12,MUTED,maxlines=2)
c.showPage()
c.save()
print(f"DEMO-02 PDF {DEST} bytes={DEST.stat().st_size} pages=7 team={len(TEAM)} sci03_cells={len(SCI03['rows'])} sep2026={SEPT_2026}",flush=True)
