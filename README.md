# 🌿 Deforestasi & Banjir Kalimantan Selatan 2015–2024

**Dashboard Interaktif — LKTI BRIDA Kalsel 2026**

> *Tekanan Deforestasi dan Risiko Bencana Banjir di Kalimantan Selatan: Analisis Spasial dan Statistik Berbasis Data Terbuka*

🔗 **[Buka Dashboard →](https://wongrembang.github.io/kalsel-deforestasi-2026/)**

---

## 📊 Fitur Dashboard

| Tab | Deskripsi |
|-----|-----------|
| 🗺 **Peta Interaktif** | 6 mode tampilan: IKEH, Deforestasi, Banjir, % Izin, GWR R², β Defor |
| 📊 **Korelasi & OLS** | Uji Spearman, scatter plot, regresi OLS dengan HC3 robust SE |
| 🔬 **GWR Spasial** | Koefisien lokal per kabupaten, perbandingan OLS vs GWR |
| 🎯 **Simulasi Skenario** | Proyeksi dampak perubahan deforestasi terhadap banjir (berbasis GWR) |
| ⚖ **Simulasi IKEH** | What-if kebijakan: dampak moratorium izin dan rehabilitasi hutan |
| 📈 **Proyeksi 2030** | 3 skenario: Baseline, Optimis (moratorium), Pesimis (ekspansi) |
| 🧮 **Kalkulator Risiko** | Hitung IKEH wilayah baru dari input data spesifik |
| 📋 **Data Lengkap** | 130 observasi panel, sortable, searchable, export CSV |
| 📖 **Metodologi** | Penjelasan lengkap semua metode + alur analisis |
| 📽 **Mode Presentasi** | Full-screen 4-slide untuk presentasi ke juri |

---

## 🔬 Metodologi

- **Data Deforestasi**: Hansen Global Forest Change v1.11 via Google Earth Engine Python API (resolusi 30m, threshold kanopi 30%)
- **Data Banjir**: BNPB DIBI + BPS Kalsel Dalam Angka 2016–2024
- **Analisis**: Korelasi Spearman · Regresi OLS (HC3) · GWR (bandwidth 50km, Gaussian kernel)
- **Output**: IKEH (Indeks Kerentanan Ekologi-Hidrologi) per kabupaten/kota

## 📈 Temuan Kunci

| Indikator | Nilai |
|-----------|-------|
| Total deforestasi 2015–2023 | **370.730 ha** |
| Total kejadian banjir 2015–2024 | **773 kejadian** |
| Korelasi Spearman (loss rate vs banjir) | **r = −0.58** (p < 0.001) |
| OLS R² | **0.19** |
| GWR R² | **0.52** (+173%) |
| Kabupaten paling rentan (IKEH) | **Tanah Bumbu (49.85)** |

---

## 🗂 Struktur Repositori

```
├── index.html              # Dashboard utama (deploy ke GitHub Pages)
├── README.md               # Dokumentasi repo
├── data/
│   ├── dataset_panel_kalsel_FINAL.csv     # Data panel lengkap (130 obs)
│   ├── kalsel_deforestasi_2015_2024.csv   # Data GEE per kab per tahun
│   ├── kalsel_banjir_2015_2024.csv        # Data banjir BNPB/BPS
│   ├── kalsel_baseline_hutan_2000.csv     # Baseline tutupan hutan
│   └── kalsel_izin_ekstraktif.csv         # Data izin ekstraktif
└── scripts/
    ├── gee_extract.py      # Ekstraksi data Hansen GFC via GEE
    ├── banjir_extract.py   # Akuisisi data banjir BNPB
    └── merge_panel.py      # Merge & preprocessing dataset panel
```

---

## 🚀 Deploy ke GitHub Pages

1. Upload semua file ke repo `wongrembang/kalsel-deforestasi-2026`
2. Settings → Pages → Source: **Deploy from branch** → `main` → `/root`
3. Dashboard akan aktif di `https://wongrembang.github.io/kalsel-deforestasi-2026/`

---

## 📚 Referensi Utama

- Hansen et al. (2013). *High-resolution global maps of 21st-century forest cover change.* Science, 342(6160).
- Fotheringham et al. (2002). *Geographically Weighted Regression.* Wiley.
- Walhi Kalsel (2025). *Lingkungan Kalimantan Selatan makin rentan pada 2025.*

---

*Penelitian independen untuk LKTI BRIDA Provinsi Kalimantan Selatan 2026.*
