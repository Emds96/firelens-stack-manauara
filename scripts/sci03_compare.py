#!/usr/bin/env python3
"""SCI-03 relative activity distribution and withheld-year comparative evaluation.
All comparisons use ORIGINAL pixel counts. No model fitted to held-out years.
Separate SP/SP, SP/NRT, NRT/NRT processing strata. Python standard library.
"""
from __future__ import annotations
import argparse,datetime as dt,json,math
from collections import Counter
from pathlib import Path

MONTH_GROUPS={"jan_oct":list(range(1,11)),
              "sp_sp_jan_jul":list(range(1,8)),
              "mixed_august":[8],
              "nrt_nrt_sep_oct":[9,10]}

def counts(data):
    out=Counter()
    for row in data["data"]:
        if len(row)!=6:raise ValueError("malformed source data record")
        year,month,sensor,lat,lon,n=row
        if sensor not in ("Aqua","NOAA20") or not 1<=month<=10 or n<0:raise ValueError("invalid data")
        key=(year,month,sensor,lat,lon)
        if key in out:raise ValueError("duplicate aggregated source cell")
        out[key]=int(n)
    return out

def project(cells,year,sensor,months,dimension):
    projected=Counter()
    for (y,mo,s,lat,lon),v in cells.items():
        if y!=year or s!=sensor or mo not in months:continue
        k=mo if dimension=="month" else (lat,lon) if dimension=="spatial" else (mo,lat,lon)
        projected[k]+=v
    return projected

def shares(counts):
    total=sum(counts.values())
    return {key:value/total for key,value in counts.items()} if total>0 else {}

def total_variation(m,v):
    if sum(m.values())<=0 or sum(v.values())<=0:return None
    a,b=shares(m),shares(v)
    return .5*sum(abs(a.get(k,0)-b.get(k,0)) for k in set(a)|set(b))

def jsd_bits(m,v):
    if sum(m.values())<=0 or sum(v.values())<=0:return None
    p,q=shares(m),shares(v)
    s=0.
    for k in set(p)|set(q):
        a,b=p.get(k,0.),q.get(k,0.)
        mid=(a+b)/2
        if a:s+=.5*a*math.log2(a/mid)
        if b:s+=.5*b*math.log2(b/mid)
    return max(0.,min(1.,s))

def ranks(values):
    ordered=sorted(range(len(values)),key=lambda i:values[i])
    output=[0.]*len(values)
    pos=0
    while pos<len(ordered):
        end=pos+1
        while end<len(ordered) and values[ordered[end]]==values[ordered[pos]]:end+=1
        rank=(pos+1+end)/2
        for i in ordered[pos:end]:output[i]=rank
        pos=end
    return output

def pearson(a,b):
    if len(a)!=len(b) or len(a)<2:return None
    ma=sum(a)/len(a);mb=sum(b)/len(b)
    centered_a=[x-ma for x in a];centered_b=[y-mb for y in b]
    den=math.sqrt(sum(x*x for x in centered_a)*sum(y*y for y in centered_b))
    return sum(x*y for x,y in zip(centered_a,centered_b))/den if den else None

def spearman(m,v):
    keys=sorted(set(m)|set(v))
    return pearson(ranks([m.get(k,0) for k in keys]),ranks([v.get(k,0) for k in keys]))

def topk_keys(c,k):
    return [key for key,_ in sorted(c.items(),key=lambda x:(-x[1],str(x[0])))[:k]]

def agreement(m,v,k=10):
    if not m or not v:return None
    topm=set(topk_keys(m,k));topv=set(topk_keys(v,k))
    union=topm|topv
    return {"k":k,"intersect_count":len(topm&topv),"jaccard":len(topm&topv)/len(union) if union else None,
            "top_modis":[str(x) for x in topk_keys(m,k)],
            "top_noaa20":[str(x) for x in topk_keys(v,k)]}

def compare(m,v):
    if not m or not v or sum(m.values())<=0 or sum(v.values())<=0:
        return {"status":"insufficient","reason":"one or both sensors have no retained detections"}
    return {"status":"observed","modis_pixels":sum(m.values()),"noaa20_pixels":sum(v.values()),
            "total_variation":round(total_variation(m,v),6),
            "jensen_shannon_divergence_bits":round(jsd_bits(m,v),6),
            "spearman_rho":None if spearman(m,v) is None else round(spearman(m,v),6),
            "top_overlap":agreement(m,v,10),
            "active_keys_modis":len(m),"active_keys_noaa20":len(v),
            "union_keys":len(set(m)|set(v))}

def simple_scale_wape(cells,test,train,months):
    """Published TEST-01 method re-run on exactly the same closed Jan-Oct window.
    Coefficient fit from PRIOR years only; not computable for 2026 SP/NRT mix.
    """
    training_modis=sum(v for (y,mo,s,la,lo),v in cells.items() if y in train and mo in months and s=="Aqua")
    training_noaa20=sum(v for (y,mo,s,la,lo),v in cells.items() if y in train and mo in months and s=="NOAA20")
    if not training_modis or not training_noaa20:return {"status":"insufficient"}
    factor=training_modis/training_noaa20
    keys={(mo,la,lo) for (y,mo,s,la,lo) in cells if y==test and mo in months}
    denominator=0;raw=0.;scaled=0.
    for mo,la,lo in keys:
        a=cells.get((test,mo,"Aqua",la,lo),0)
        b=cells.get((test,mo,"NOAA20",la,lo),0)
        denominator+=a;raw+=abs(a-b);scaled+=abs(a-factor*b)
    if not denominator:return {"status":"insufficient"}
    return {"status":"held_out","training_years":list(train),"holdout_year":test,
      "factor_prior_years_only":round(factor,8),
      "modis_reference_pixels":denominator,
      "wape_raw":round(raw/denominator,6),
      "wape_global_scaled":round(scaled/denominator,6),
      "interpretation":"WAPE is for absolute MODIS pixel counts, not actual fires; cannot compare numerically with TV/JSD."}

def run(historical,recent):
    if historical["status"]!="historical_verified" or recent["status"]!="all_2026_jan_oct_windows_downloaded":
        raise ValueError("Missing verified source downloads; cannot publish SCI03 metrics")
    if historical["geometry_sha256"]!=recent["geometry_sha256"]:
        raise ValueError("Inconsistent Amazonas geometry across years")
    data=counts({"data":historical["data"]+recent["data"]})
    years=(2023,2024,2025,2026)
    out={"id":"SCI-03","created_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
      "status":"metrics_computed_review_pending",
      "scientific_question":"Do MODIS Aqua and VIIRS NOAA-20 agree about relative monthly/geographic activity, especially 2025/2026?",
      "geometry_sha256":historical["geometry_sha256"],
      "sources":{"historical":historical["file_provenance"],
                 "recent_availability":recent["availability"],
                 "recent_windows":recent["windows"]},
      "methods":{
        "window":"closed UTC calendar months Jan-Oct (2023–2026), same 1° grid and simplified Amazonas polygon",
        "sensor_filters":"daytime; MODIS Aqua >=30, NOAA20 n/h, type=0 where available",
        "normalization":"Each sensor's original counts in a given year and period divided by its own total for that year and period",
        "total_variation":"0.5*sum absolute differences in relative shares, 0 perfect, 1 maximal",
        "jensen_shannon_divergence_bits":"JS divergence, range 0..1 bits, 0 identical",
        "spearman_rho":"rank correlation on union of active cells/months; ties receive average ranks",
        "top_k":"top 10 one-degree spatial cells per sensor ranked by original counts; overlap/jaccard",
        "baseline":"global factor trained on preceding historical year(s), evaluated on held-out 2024/2025 Jan-Oct; no 2026 absolute WAPE because SP/NRT difference",
        "no_target_modis_leakage":"share comparison uses both sensors' observed totals for descriptive comparison only, not for predictive calibration",
        "invariance":"positive global multiplication of VIIRS count leaves share distribution, ranks and top-k exactly unchanged"},
      "years":[],"cross_year_relative_activity":[],"absolute_count_baseline":[],"warnings":[
        "Pattern agreement is not validated physical harmonization or a replacement for absolute count validation.",
        "No observational coverage/opportunity or cloud-free denominator; sensor detections are not fires.",
        "2026 SP/NRT mixing and missing NRT type attribute limit interannual comparability.",
        "Aug 2026 MODIS SP versus NOAA20 NRT; Jan-Jul both SP; Sep-Oct both NRT.",
        "Amazonas boundary simplified and not precision-validated against official IBGE.",
        "Jan-Oct excludes incomplete Nov 2026. 2026 NRT may be revised."]}
    for year in years:
        for name,mo in MONTH_GROUPS.items():
            entry={"year":year,"period":name,"months":mo,
                "processing_context":"archived" if year<=2025 else
                    "SP/SP" if name=="sp_sp_jan_jul" else
                    "SP/NRT" if name=="mixed_august" else
                    "NRT/NRT" if name=="nrt_nrt_sep_oct" else "SP+NRT/varies_by_sensor"}
            for dimension in ("month","spatial","spatiotemporal"):
                x=project(data,year,"Aqua",mo,dimension)
                y=project(data,year,"NOAA20",mo,dimension)
                entry[dimension]=compare(x,y)
                if dimension=="month" and name=="mixed_august":
                    entry[dimension]={"status":"not_informative","reason":"one month only: temporal share agreement would equal 1 by construction"}
            out["years"].append(entry)
        # same sensor annual monthly relative distribution, no temporal model
        if year>2023:
            for sensor in ("Aqua","NOAA20"):
                previous=project(data,year-1,sensor,MONTH_GROUPS["jan_oct"],"month")
                current=project(data,year,sensor,MONTH_GROUPS["jan_oct"],"month")
                out["cross_year_relative_activity"].append({
                    "sensor":sensor,"prior_year":year-1,"year":year,
                    "monthly_tv":round(total_variation(previous,current),6) if total_variation(previous,current)!=None else None,
                    "monthly_spearman":round(spearman(previous,current),6) if spearman(previous,current)!=None else None})
    for test,train in ((2024,(2023,)),(2025,(2023,2024))):
        out["absolute_count_baseline"].append(simple_scale_wape(data,test,train,MONTH_GROUPS["jan_oct"]))
    # Algebraic control: a positive scalar cannot change the relative distribution
    base=project(data,2025,"NOAA20",MONTH_GROUPS["jan_oct"],"spatial")
    scalar=out["absolute_count_baseline"][-1]["factor_prior_years_only"]
    after={k:v*scalar for k,v in base.items()}
    maximum=max(abs(shares(base)[k]-shares(after)[k]) for k in base)
    if maximum>1e-12:raise AssertionError("positive global scale unexpectedly changed shares")
    out["invariance_demonstrated_max_share_difference"]=maximum
    out["overall_interpretation"]="Relative shares summarize where/when each sensor concentrates detected pixels, but global multiplicative scaling produces identical share/rank patterns. They are complementary descriptive views, NOT more accurate physical harmonization."
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--historical",default="/tmp/sci03_historical.json")
    p.add_argument("--recent",default="/tmp/sci03_recent.json")
    p.add_argument("--out",default="data/sci03_resultados.json")
    a=p.parse_args()
    hist=json.loads(Path(a.historical).read_text())
    recent=json.loads(Path(a.recent).read_text())
    result=run(hist,recent)
    dst=Path(a.out);dst.parent.mkdir(exist_ok=True,parents=True)
    dst.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    for x in result["years"]:
        if x["period"]=="jan_oct":
            print("SCI03",x["year"],"MONTH-TV",x["month"].get("total_variation"),
                  "SPATIAL-TV",x["spatial"].get("total_variation"),
                  "TOP10",x["spatial"].get("top_overlap",{}).get("intersect_count"),flush=True)
    print("SCI03 OUTPUT",a.out,flush=True)
if __name__=="__main__":main()
