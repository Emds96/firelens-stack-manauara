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

W,H=960,540
BG="#0a1822";SURFACE="#142936";ACC="#ff9568";CYAN="#80e0d9";WHITE="#f4f8f8";MUTED="#b3c7d0";LINE="#2d4a55"
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/"demo"/"FireLens_7_Slide_Demo_2026.pdf"
CASE=json.loads((ROOT/"data"/"caso_visao_aguia_20261110.json").read_text())
TEST=json.loads((ROOT/"data"/"test02_resultados.json").read_text())
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
c.setTitle("FireLens - Two Translators | 7-slide Project Demo | FIN-01")
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

# 1: Intro
title("Two sensors. Two translators. One clearer view.","NASA SPACE APPS 2026",1)
txt("Real satellite thermal observations,",70,363,28,WHITE,True)
txt("explained without overstating the evidence.",70,318,24,CYAN,True)
wrapped("FireLens turns NASA FIRMS detections into an interactive map, a tested historical count comparison, and a transparent observation-level research example.",70,260,780,16,23,MUTED,maxlines=4)
rbox(70,88,820,72,"#173541","#3b7475",12)
txt("ONE OBSERVED PIXEL",97,132,13,CYAN,True)
arrow(310,125,356)
txt("ONE CLEAR INTERPRETATION",372,132,13,WHITE,True)
txt("Not a confirmed individual fire; not a burned-area outline.",97,106,12,MUTED)
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

# 5: historical calendar
title("04  |  Put observations in context","HISTORY / PILOT REGIONS A & B",5)
photo("/tmp/firelens_history.png",45,93,590,324)
txt("2022-2024",667,383,18,CYAN,True)
wrapped("72 checked region-month records in two experimental pilot rectangles (A/B).",667,351,237,13,20,WHITE,maxlines=5)
wrapped("Not a municipality-level history of all Amazonas.",667,267,235,12,18,ACC,maxlines=4)
txt("A separate Amazonas test:",667,174,12,MUTED,True)
txt("WAPE 2024  23.11%",667,151,12,WHITE)
txt("WAPE 2025  50.73%",667,129,12,WHITE)
wrapped("Absolute-count error versus MODIS, not physical fire accuracy.",667,105,226,10,13,MUTED,maxlines=3)
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
wrapped("Original NASA fields, dated JSON, TEST-02 methods, source hashes, and 47 passing Python tests are published.",70,173,800,14,20,MUTED,maxlines=3)
txt("github.com/Emds96/firelens-stack-manauara",70,100,15,CYAN,True)
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
wrapped("Satellite data: NASA FIRMS. Map: OpenStreetMap contributors. Slide design and text prepared with ChatGPT assistance. FireLens is independent and not endorsed by NASA.",65,60,820,9,12,MUTED,maxlines=2)
c.showPage()
c.save()
print(f"FIN-01 PDF {DEST} bytes={DEST.stat().st_size} seven_slides=verified_by_source_logic",flush=True)
