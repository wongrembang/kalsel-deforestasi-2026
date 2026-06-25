import ee, pandas as pd, numpy as np, os, time

PROJECT_ID = "kalsel-deforestasi-2026"
OUTPUT_DIR = "output_fase2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ee.Initialize(project=PROJECT_ID)
print("GEE OK - mulai ekstraksi Hansen GFC...\n")

hansen    = ee.Image("UMD/hansen/global_forest_change_2023_v1_11")
loss_year = hansen.select("lossyear")
loss      = hansen.select("loss")
treecover = hansen.select("treecover2000")
forest_mask = treecover.gte(30)

kalsel = (ee.FeatureCollection("FAO/GAUL/2015/level2")
            .filter(ee.Filter.eq("ADM1_NAME", "Kalimantan Selatan")))

n = kalsel.size().getInfo()
print(f"Kabupaten/kota ditemukan: {n}\n")

all_records = []
for offset in range(15, 24):
    tahun = 2000 + offset
    print(f"  Ekstrak {tahun}...", end=" ", flush=True)
    t0 = time.time()
    loss_yr = loss_year.eq(offset).And(forest_mask)
    def calc(f):
        a = loss_yr.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(), geometry=f.geometry(),
            scale=30, maxPixels=1e13, bestEffort=True)
        return f.set({"loss_ha": ee.Number(a.get("lossyear")).divide(10000), "tahun": tahun})
    feats = kalsel.map(calc).getInfo()["features"]
    for f in feats:
        p = f["properties"]
        all_records.append({"tahun": tahun, "kab_kota": p.get("ADM2_NAME","?"),
                            "loss_ha": round(p.get("loss_ha",0),4), "catatan": ""})
    print(f"OK ({time.time()-t0:.1f}s)")

df = pd.DataFrame(all_records)

est = (df[df.tahun.isin([2021,2022,2023])].groupby("kab_kota")["loss_ha"]
       .mean().reset_index())
est["tahun"] = 2024
est["catatan"] = "Estimasi rata-rata 2021-2023"
df_all = pd.concat([df, est], ignore_index=True)

out = f"{OUTPUT_DIR}/kalsel_deforestasi_2015_2024.csv"
df_all.to_csv(out, index=False)
print(f"\nDisimpan: {out}")
print(f"Total record: {len(df_all)}")

print("\n--- Total deforestasi per kabupaten (2015-2023, ha) ---")
s = (df[df.tahun<=2023].groupby("kab_kota")["loss_ha"].sum()
     .sort_values(ascending=False).reset_index())
s.columns = ["Kabupaten/Kota","Total_Ha"]
s["Total_Ha"] = s["Total_Ha"].round(1)
print(s.to_string(index=False))

def get_baseline(f):
    a = treecover.gte(30).multiply(ee.Image.pixelArea()).reduceRegion(
        reducer=ee.Reducer.sum(), geometry=f.geometry(),
        scale=30, maxPixels=1e13, bestEffort=True)
    return f.set({"forest_2000_ha": ee.Number(a.get("treecover2000")).divide(10000)})

print("\nEkstrak baseline hutan 2000...", end=" ", flush=True)
base_feats = kalsel.map(get_baseline).getInfo()["features"]
base = [{"kab_kota": f["properties"].get("ADM2_NAME","?"),
          "forest_2000_ha": round(f["properties"].get("forest_2000_ha",0),1)}
        for f in base_feats]
pd.DataFrame(base).to_csv(f"{OUTPUT_DIR}/kalsel_baseline_hutan_2000.csv", index=False)
print("OK\n\nSELESAI - jalankan merge_panel.py selanjutnya")
