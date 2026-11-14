#!/usr/bin/env python3
"""Stack Manauara / VAL-TRAD-02. Reproduce NOAA-20 versus Aqua tests.
Run: python validacao_tradutor1_reproduzivel.py --cache ./firms_cache > results.json
Uses official public FIRMS archive CSV via HTTPS; no external Python packages.
WARNING: no retrieval is made of boundary adjacent years; year-crossing LST observations
are excluded and counted as incomplete, not silently included in incorrect months.
"""
import argparse
import csv
import datetime as dt
import io
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from urllib.request import Request, urlopen

BASE = "https://firms.modaps.eosdis.nasa.gov/data/country/"
REGIONS = {"A": (-65, -9, -58, -2), "B": (-58, -9, -51, -2)}


def local_year_month(row, longitude):
    t = (row.get("acq_time") or "0").zfill(4)
    utc = dt.datetime.strptime(row["acq_date"] + t, "%Y-%m-%d%H%M")
    solar = utc + dt.timedelta(hours=longitude / 15.0)
    return solar.year, solar.month


def open_firms(year, satellite, cache):
    name = f"{satellite}_{year}_Brazil.csv"
    path = cache / name
    if path.is_file():
        return path.open("r", encoding="utf-8", newline="")
    req = Request(BASE + name, headers={"User-Agent": "StackManauara-VAL-TRAD-02/1.0"})
    return io.TextIOWrapper(urlopen(req, timeout=120), encoding="utf-8", newline="")


def ingest(year, satellite, cache, records, stats):
    with open_firms(year, satellite, cache) as infile:
        for row in csv.DictReader(infile):
            if row.get("type") not in (None, "", "0"):
                continue
            if row.get("daynight") not in ("D", "N"):
                continue
            if satellite == "modis":
                if row.get("satellite") not in ("Aqua", "A"):
                    continue
                if float(row.get("confidence") or 0) < 30:
                    continue
                sensor = "Aqua"
            else:
                if row.get("confidence", "").lower() not in ("n", "h"):
                    continue
                sensor = "NOAA20"
            lat, lon = float(row["latitude"]), float(row["longitude"])
            region = next((name for name, (west, south, east, north) in REGIONS.items()
                           if west <= lon < east and south <= lat < north), None)
            if region is None:
                continue
            ly, lm = local_year_month(row, lon)
            if ly != year:
                stats["omitted_local_year_crossings"] += 1
                continue
            records[(region, sensor, row["daynight"], ly, lm,
                     math.floor(lat), math.floor(lon))] += 1
            stats["retained"] += 1


def score(y, pred):
    active = [i for i in range(len(y)) if y[i] or pred[i]]
    errors = [y[i] - pred[i] for i in active]
    sy = sum(y)
    return {
        "WAPE": round(sum(abs(e) for e in errors) / sy, 4) if sy else None,
        "MAE_active": round(sum(abs(e) for e in errors) / len(active), 3) if active else None,
        "RMSE_active": round(math.sqrt(sum(e*e for e in errors) / len(active)), 3) if active else None,
        "bias_pred_minus_obs": round((sum(pred) - sy) / sy, 4) if sy else None,
        "active_cells_month": len(active), "MODIS_sum": sy,
        "NOAA20_pred_sum": round(sum(pred), 1),
    }


def evaluate(data, region, daynight, train_years, test_year, kappa=2500):
    west, south, east, north = REGIONS[region]
    def get(years, sensor):
        return [(year, month, lat, lon,
                 data.get((region, sensor, daynight, year, month, lat, lon), 0))
                for year in years for month in range(1, 13)
                for lat in range(south, north) for lon in range(west, east)]
    vtrain, mtrain = get(train_years, "NOAA20"), get(train_years, "Aqua")
    vtest, mtest = get([test_year], "NOAA20"), get([test_year], "Aqua")
    denom = sum(a[4] for a in vtrain)
    if not denom:
        return {"error": "no VIIRS observations in training"}
    global_factor = sum(a[4] for a in mtrain) / denom
    month_coef = {}
    for month in range(1, 13):
        v = sum(a[4] for a in vtrain if a[1] == month)
        m = sum(a[4] for a in mtrain if a[1] == month)
        raw = m / v if v else global_factor
        regularized = v / (v + kappa) * raw + kappa / (v + kappa) * global_factor
        month_coef[month] = (raw, regularized)
    y = [a[4] for a in mtest]
    v = [a[4] for a in vtest]
    predictions = {
        "raw": [float(x) for x in v],
        "global": [global_factor*x for x in v],
        "monthly": [month_coef[a[1]][0]*x for a, x in zip(vtest, v)],
        "regularized": [month_coef[a[1]][1]*x for a, x in zip(vtest, v)],
    }
    return {"region": region, "daynight": daynight, "training": train_years,
            "holdout": test_year, "global_coefficient": round(global_factor, 7),
            "methods": {name: score(y, pred) for name, pred in predictions.items()}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, default=Path("firms_cache"))
    args = parser.parse_args()
    result = {"source": BASE, "year_range": [2022, 2023, 2024],
              "sensors": ["modis Aqua", "viirs-jpss1 NOAA20"],
              "filters": "type=0 when available; MODIS confidence>=30; VIIRS n/h; D and N separate",
              "regions": REGIONS, "files": [], "experiments": []}
    records = defaultdict(int)
    for year in [2022, 2023, 2024]:
        for satellite in ["modis", "viirs-jpss1"]:
            st = Counter()
            ingest(year, satellite, args.cache, records, st)
            result["files"].append({"year": year, "satellite": satellite,
                                    "url": BASE+f"{satellite}_{year}_Brazil.csv", **dict(st)})
    for region in REGIONS:
        for daynight in ("D", "N"):
            for tr, te in [([2022], 2023), ([2022, 2023], 2024)]:
                result["experiments"].append(evaluate(records, region, daynight, tr, te))
    result["limitations"] = ["Not independently validated against fires or burned area",
                             "Solar local year-crossing records excluded; adjacent UTC-year files needed for complete local calendar",
                             "Cloud/clear-sky observation denominators unavailable in FIRMS hotspot CSVs",
                             "No operational NRT or NOAA-21 validation", "No calibrated uncertainty intervals"]
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
