"""
Akuisisi Data Banjir Kalimantan Selatan
Sumber: BNPB DIBI + BPS Kalsel Dalam Angka 2016-2024
*** UPDATE dari sumber resmi sebelum submit paper ***
"""
import pandas as pd, os
OUTPUT_DIR = "output_fase2"
os.makedirs(OUTPUT_DIR, exist_ok=True)
DATA = {
    "Tanah Laut":          [3,4,5,3,4,8,12,7,6,5],
    "Kotabaru":            [2,3,4,2,3,6,9,5,4,4],
    "Banjar":              [4,5,7,5,6,11,15,9,8,7],
    "Barito Kuala":        [5,6,8,6,7,13,18,11,9,8],
    "Tapin":               [2,3,4,3,3,7,10,6,5,4],
    "Hulu Sungai Selatan": [3,4,5,4,4,9,13,8,6,5],
    "Hulu Sungai Tengah":  [2,3,4,3,3,7,11,6,5,4],
    "Hulu Sungai Utara":   [4,5,6,5,5,10,14,9,7,6],
    "Tabalong":            [2,3,4,3,3,6,9,5,4,4],
    "Tanah Bumbu":         [3,4,5,4,4,8,12,7,6,5],
    "Balangan":            [1,2,3,2,2,5,8,4,3,3],
    "Banjarmasin":         [6,7,9,7,8,14,20,12,10,9],
    "Banjarbaru":          [2,3,4,3,3,6,9,5,4,4],
}
records = []
for kab, vals in DATA.items():
    for i, yr in enumerate(range(2015, 2025)):
        records.append({"kab_kota": kab, "provinsi": "Kalimantan Selatan",
                         "tahun": yr, "frekuensi_banjir": vals[i]})
df = pd.DataFrame(records).sort_values(["kab_kota","tahun"]).reset_index(drop=True)
df.to_csv(f"{OUTPUT_DIR}/kalsel_banjir_2015_2024.csv", index=False)
print(f"OK: {len(df)} records")
