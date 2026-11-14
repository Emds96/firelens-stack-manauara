#!/usr/bin/env python3
"""Generate SCI-03 Markdown report directly from audited results."""
import argparse,json
from pathlib import Path
from scripts.sci03_compare import counts,project,topk_keys,MONTH_GROUPS

def f(v,n=3):
    return "—" if v is None else format(v,f".{n}f")

def top(c,kind,k=3):
    total=sum(c.values())
    if not total:return "insufficient"
    return "; ".join( (f"month {key:02d}" if kind=="month" else f"1° cell southwest ({key[0]},{key[1]})")
        +f": {c[key]} ({100*c[key]/total:.1f}%)" for key in topk_keys(c,k))

def render(r,h,n):
    data=counts({"data":h["data"]+n["data"]})
    all_rows=[row for row in r["years"] if row["period"]=="jan_oct"]
    recent_rows=[row for row in r["years"] if row["year"]==2026]
    lines=[
      "# SCI-03 — Relative thermal-activity patterns, MODIS Aqua and VIIRS NOAA-20",
      "",
      "Stack Manauara · FireLens · 14/11/2026 · **Scientific decision pending main session**",
      "",
      "## Conclusion first",
      "",
      "**Relative normalization is defensible as DESCRIPTIVE pattern comparison, not yet a validated harmonization or demonstrated improvement in physical fire estimates.** A global positive multiplicative adjustment leaves shares, ranks and top-k unchanged by algebra. Thus identical relative pattern scores after global scaling cannot establish superiority of a new correction method.",
      "",
      "## 2026 prioritized — 1 January through 31 October, UTC, closed months",
      "",
      "FIRMS Area API was used for non-overlapping source/product date ranges; every response is listed with SHA-256, sanitized URL, SP/NRT category and CSV attributes in the accompanying JSON. Dates of query availability do not prove cloud-free overpasses or continuous physical coverage.",
      "",
      "Jan–Jul both SP; Aug MODIS SP and NOAA-20 NRT; Sep–Oct both NRT. November 2026 excluded as incomplete. The type attribute is not present in observed NRT rows; vegetated-fire filtering differs from SP records.",
      "",
      "| 2026 scope | MODIS pixels | NOAA-20 pixels | Monthly TV | Spatial TV | Spatial Spearman | Shared top-10 1-degree cells |",
      "|---|---:|---:|---:|---:|---:|---:|"]
    for row in recent_rows:
        m,s=row["month"],row["spatial"]
        o=s.get("top_overlap") or {}
        lines.append("| {} ({}) | {} | {} | {} | {} | {} | {} |".format(
            row["period"],row["processing_context"],
            s.get("modis_pixels","—"),s.get("noaa20_pixels","—"),
            f(m.get("total_variation")),f(s.get("total_variation")),
            f(s.get("spearman_rho")),o.get("intersect_count","—")))
    lines += [
      "",
      "TV is total variation distance: 0=identical normalized distribution, 1=disjoint. Spearman rho measures rank agreement. For a single month (August), temporal agreement is not informative. Neither metric measures error against individual fires.",
      "",
      "## Ranking of most observed months and 1-degree cells (2025 and 2026)",
      ""]
    for year in (2025,2026):
        lines.append("### "+str(year)+" — January through October")
        for sensor in ("Aqua","NOAA20"):
            mo=project(data,year,sensor,MONTH_GROUPS["jan_oct"],"month")
            sp=project(data,year,sensor,MONTH_GROUPS["jan_oct"],"spatial")
            lines.append("- **{}**: highest monthly shares: {}. Most active cells: {}.".format(
                sensor,top(mo,"month"),top(sp,"spatial")))
        lines.append("")
    lines += [
      "## Independent years: descriptive agreement 2023, 2024, 2025, 2026",
      "",
      "Each year is evaluated independently; no coefficient is fitted using its observations for held-out WAPE. Share distributions are normalized per sensor within the observed window for descriptive comparisons, **not** a predictive calibration. Same geographic 1° cells and UTC January–October months for all four years.",
      "",
      "| Year | MODIS pixels | NOAA-20 pixels | TV months | JS divergence months (bits) | Spearman months | TV spatial | Spearman spatial | Shared top-10 spatial |",
      "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for row in all_rows:
        mo,sp=row["month"],row["spatial"]
        lines.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            row["year"],mo.get("modis_pixels","—"),mo.get("noaa20_pixels","—"),
            f(mo.get("total_variation")),f(mo.get("jensen_shannon_divergence_bits")),
            f(mo.get("spearman_rho")),f(sp.get("total_variation")),
            f(sp.get("spearman_rho")),(sp.get("top_overlap") or {}).get("intersect_count","—")))
    lines += [
      "",
      "JS is Jensen–Shannon divergence in bits, 0=identical. Rank correlation and TV are distinct from accuracy of estimated fire counts.",
      "",
      "## Control: absolute-count global scaling, fitted only on earlier years",
      "",
      "| Prior training years | Held-out year | Global factor (Jan–Oct) | Raw WAPE | Scaled WAPE |",
      "|---|---:|---:|---:|---:|"]
    for v in r["absolute_count_baseline"]:
        lines.append("| {} | {} | {} | {}% | {}% |".format(
            ",".join(map(str,v["training_years"])),v["holdout_year"],
            f(v["factor_prior_years_only"],8),f(100*v["wape_raw"],2),
            f(100*v["wape_global_scaled"],2)))
    lines += [
      "",
      "These WAPEs were computed for January–October only and DO NOT replace original full-year TEST-01 values (2024 23.11%; 2025 50.73%). They are absolute count errors relative to MODIS observations, **not** directly comparable numerically with TV, JS or Spearman. No 2026 WAPE was computed with the old factor because the SP/NRT mix and missing NRT type field prevent claiming equivalent processing.",
      "",
      "## Method and reproducibility",
      "",
      "1. Redownload annual NASA FIRMS Brazil CSVs 2023–2025, verify original SHA-256 and annual eligible counts against TEST-01; clip Jan–Oct.",
      "2. Requery 2026 NASA FIRMS Area API using dates and SP-preferred, NRT-gap-filling source selection, in 1–5 day disjoint windows. Exclude November.",
      "3. Filter MODIS Aqua confidence ≥30, NOAA-20 n/h, daytime D, type=0 if available, inside simplified Amazonas polygon; aggregate 1° × UTC month.",
      "4. Compute relative share in a year/period = native sensor pixel count in a month/cell divided by that same sensor's total in period. Then compute TV, Jensen–Shannon divergence, Spearman on union of active categories, and overlap among top 10 1-degree spatial cells.",
      "5. Evaluate global factor trained only on earlier years on historical independent years 2024/2025; never optimize with test year.",
      "6. Delimit 2026 SP/SP Jan–Jul, SP/NRT August and NRT/NRT Sep–Oct, disclose field disparities. Distinct SP and NRT product records never overlap per sensor/day.",
      "",
      "Sources: https://firms.modaps.eosdis.nasa.gov/data/country/ ; https://firms.modaps.eosdis.nasa.gov/api/area/ ; https://firms.modaps.eosdis.nasa.gov/api/data_availability/ ; https://www.earthdata.nasa.gov/data/tools/firms",
      "Detailed archive SHA-256 and 2026 API response SHA-256 / date windows are stored in data/sci03_resultados.json without revealing FIRMS_MAP_KEY.",
      "",
      "### Historical source hashes",
      "| Year | Product | SHA-256 |",
      "|---|---|---|"]
    for entry in h["file_provenance"]:
        lines.append("| {} | {} | {} |".format(entry["year"],entry["source"],entry["sha256"]))
    lines += [
      "",
      "## Scientific interpretation, uncertainties and decision",
      "",
      "**Observed:** native pixel distributions, ranked months, ranked 1° cells and quantified agreement for each sensor/period.",
      "**Mathematically established:** global positive scale factor cannot improve the ranking or relative shares, so greater clarity is the main benefit of displaying percentages.",
      "**Hypotheses only:** changing orbit coverage, cloud obscuration, fire cause, climate trends, or physical difference in individual fires. These were not tested.",
      "**Restrictions:** 2026 NRT type field absent; different sensor resolutions/sensitivity and observation schedules; no clear-sky denominator; simplified, not officially verified Amazonas border; NRT can be revised; low detection counts affect share variability; spatial 1° aggregation smooths detail.",
      "**Recommended for FireLens:** consider a future view showing separate month and area shares **for both sensors** with clearly different SP/NRT processing and caveats. Do NOT call relative normalization validated sensor correction, fire risk, prediction or proof of true fire events.",
      "",
      "**Decision SCI-03 / status:** evidence-ready proposal, pending review and approval by main session. No UI changes and no TEST-02. Reason: relative metrics help explain observed concentration, not outperform absolute count scaling on a commensurable metric. Alternative: new complex model declined until evidence and time allow. Validation: reproduce source hashes, independent WAPE, distributions, tests and cross-version limits. Responsible: Stack Manauara engineering · 14/11/2026.",
      "",
      "## Reproduction",
      "Run unit tests: python -m unittest discover -s tests -v",
      "Historical: python -m scripts.sci03_sources historical --out /tmp/sci03_historical.json",
      "2026: python -m scripts.sci03_sources recent --out /tmp/sci03_recent.json (requires FIRMS_MAP_KEY from GitHub Actions secret)",
      "Compare: python -m scripts.sci03_compare --historical /tmp/sci03_historical.json --recent /tmp/sci03_recent.json --out data/sci03_resultados.json",
      "Report: python -m scripts.sci03_report --results data/sci03_resultados.json --historical /tmp/sci03_historical.json --recent /tmp/sci03_recent.json",
      ""
    ]
    return "\n".join(lines)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--results",default="data/sci03_resultados.json")
    p.add_argument("--historical",default="/tmp/sci03_historical.json")
    p.add_argument("--recent",default="/tmp/sci03_recent.json")
    p.add_argument("--out",default="docs/SCI-03_HARMONIZACAO_PADROES.md")
    args=p.parse_args()
    r=json.loads(Path(args.results).read_text())
    h=json.loads(Path(args.historical).read_text())
    n=json.loads(Path(args.recent).read_text())
    report=render(r,h,n)
    target=Path(args.out)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(report,encoding="utf8")
    print("SCI03 REPORT",target,"bytes",len(report),flush=True)
if __name__=="__main__":main()
