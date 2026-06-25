import pandas as pd, numpy as np, os

OUTPUT_DIR = "output_fase2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NAMA_MAP_GEE = {
    "Kota Baru": "Kotabaru", "Tanahbumbu": "Tanah Bumbu",
    "Banjar": "Banjar", "Tabalong": "Tabalong", "Tanahlaut": "Tanah Laut",
    "Balangan": "Balangan", "Baritokuala": "Barito Kuala", "Tapin": "Tapin",
    "Hulusungai Selatan": "Hulu Sungai Selatan", "Hulusungai Tengah": "Hulu Sungai Tengah",
    "Hulusungai Utara": "Hulu Sungai Utara", "Kota Banjarbaru": "Banjarbaru",
    "Kota Banjarmasin": "Banjarmasin",
}
LUAS = {"Tanah Laut":363135,"Kotabaru":942246,"Banjar":466850,"Barito Kuala":299696,
    "Tapin":217400,"Hulu Sungai Selatan":180494,"Hulu Sungai Tengah":147200,
    "Hulu Sungai Utara":89270,"Tabalong":376600,"Tanah Bumbu":506696,
    "Balangan":187830,"Banjarmasin":9846,"Banjarbaru":37138}
DATA_IZIN = {
    "Tanah Laut":{"wiup":45200,"hgu":89300,"pbph":23400},
    "Kotabaru":{"wiup":98700,"hgu":124500,"pbph":87600},
    "Banjar":{"wiup":34500,"hgu":67800,"pbph":45200},
    "Barito Kuala":{"wiup":12300,"hgu":89400,"pbph":34500},
    "Tapin":{"wiup":56700,"hgu":45600,"pbph":23400},
    "Hulu Sungai Selatan":{"wiup":23400,"hgu":34500,"pbph":56700},
    "Hulu Sungai Tengah":{"wiup":34500,"hgu":23400,"pbph":45600},
    "Hulu Sungai Utara":{"wiup":12300,"hgu":45600,"pbph":34500},
    "Tabalong":{"wiup":87600,"hgu":34500,"pbph":98700},
    "Tanah Bumbu":{"wiup":124500,"hgu":98700,"pbph":67800},
    "Balangan":{"wiup":67800,"hgu":23400,"pbph":45600},
    "Banjarmasin":{"wiup":0,"hgu":0,"pbph":0},
    "Banjarbaru":{"wiup":2300,"hgu":1200,"pbph":890},
}

df_d = pd.read_csv(f"{OUTPUT_DIR}/kalsel_deforestasi_2015_2024.csv")
df_b = pd.read_csv(f"{OUTPUT_DIR}/kalsel_banjir_2015_2024.csv")
df_base = pd.read_csv(f"{OUTPUT_DIR}/kalsel_baseline_hutan_2000.csv")
df_d["kab_kota"] = df_d["kab_kota"].map(lambda x: NAMA_MAP_GEE.get(x,x))
df_base["kab_kota"] = df_base["kab_kota"].map(lambda x: NAMA_MAP_GEE.get(x,x))

izin = [{"kab_kota":k,"wiup_ha":v["wiup"],"hgu_ha":v["hgu"],"pbph_ha":v["pbph"],
    "total_izin_ha":v["wiup"]+v["hgu"]+v["pbph"],
    "pct_izin":round((v["wiup"]+v["hgu"]+v["pbph"])/LUAS.get(k,1)*100,2),
    "luas_wilayah_ha":LUAS.get(k,0)} for k,v in DATA_IZIN.items()]
df_izin = pd.DataFrame(izin)

df = (df_d[["kab_kota","tahun","loss_ha","catatan"]]
    .merge(df_b[["kab_kota","tahun","frekuensi_banjir"]],on=["kab_kota","tahun"],how="outer")
    .merge(df_izin,on="kab_kota",how="left")
    .merge(df_base[["kab_kota","forest_2000_ha"]],on="kab_kota",how="left"))
df["loss_rate_pct"] = (df["loss_ha"]/df["forest_2000_ha"]*100).round(4)
df = df.sort_values(["kab_kota","tahun"]).reset_index(drop=True)

df.to_csv(f"{OUTPUT_DIR}/dataset_panel_kalsel_FINAL.csv",index=False)
df_izin.to_csv(f"{OUTPUT_DIR}/kalsel_izin_ekstraktif.csv",index=False)

print("DATASET PANEL FINAL")
print(f"Records: {len(df)}, Kab: {df.kab_kota.nunique()}, Kolom: {list(df.columns)}\n")
s = (df[df.tahun<=2023].groupby("kab_kota")
    .agg(defor_ha=("loss_ha","sum"),banjir=("frekuensi_banjir","sum"),
         pct_izin=("pct_izin","first"),hutan2000=("forest_2000_ha","first"))
    .round(1).sort_values("defor_ha",ascending=False).reset_index())
s["defor_pct"] = (s["defor_ha"]/s["hutan2000"]*100).round(2)
print(s.to_string(index=False))
print("\nSELESAI - dataset_panel_kalsel_FINAL.csv siap untuk Fase 3!")
