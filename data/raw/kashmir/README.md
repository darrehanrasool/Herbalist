# Kashmir Endemic High-Altitude Flora · Dataset Manifest & Protocol

This directory is designated for **in-house and field-collected datasets of high-altitude medicinal flora endemic to the Kashmir Himalayas**.

## 1. Directory Structure

```
data/raw/kashmir/
├── README.md               <- This protocol document
├── images/                 <- Raw high-resolution field captures (.jpg, .png)
│   ├── aconitum_heterophyllum/
│   ├── gentiana_kurroo/
│   ├── picrorhiza_kurroa/
│   ├── saussurea_costus/
│   ├── podophyllum_hexandrum/
│   ├── arnebia_benthamii/
│   └── ...
├── metadata/               <- Field metadata records
│   ├── gps_elevation_logs.csv
│   └── microclimate_readings.csv
└── kashmir_flora_survey.csv<- Curated taxonomic index with conservation status
```

## 2. Priority Taxa & Conservation Statuses

| Botanical Name | Local / Kashmiri Name | IUCN Conservation Status | Altitude Range (masl) | Key Bioactive Secondary Metabolites |
| :--- | :--- | :--- | :--- | :--- |
| *Gentiana kurroo* | Neel Kanth / Nilkanth | Critically Endangered (CR) | 1,800 – 3,000 m | Gentiopicroside, Amarogentin |
| *Saussurea costus* (syn. *S. lappa*) | Kuth / Costus | Critically Endangered (CR) | 2,500 – 3,800 m | Costunolide, Dehydrocostus lactone |
| *Picrorhiza kurroa* | Kutki / Kour | Endangered (EN) | 3,000 – 4,500 m | Picroside I, Picroside II, Kutkoside |
| *Aconitum heterophyllum* | Patris / Atis | Critically Endangered (CR) | 2,400 – 4,000 m | Atisine, Heteratisine |
| *Podophyllum hexandrum* | Wanwangan / Bankakri | Endangered (EN) | 2,700 – 4,200 m | Podophyllotoxin |
| *Arnebia benthamii* | Kahzaban | Critically Endangered (CR) | 3,000 – 4,300 m | Shikonin derivatives |
| *Inula racemosa* | Poshkar | Endangered (EN) | 2,000 – 3,200 m | Alantolactone, Isoalantolactone |
| *Rheum webbianum* | Pambchalan | Vulnerable (VU) | 2,800 – 4,200 m | Emodin, Rhein, Chrysophanol |

## 3. Data Collection Protocol
When photographing specimens in Kashmir (Gulmarg, Sonamarg, Pahalgam, Gurez, Sinthan Top):
1. **Multiple Morphological Angles:** Capture close-up adaxial (top) leaf surface, abaxial (underside) venation, stem attachment, and inflorescence/flower when available.
2. **Metadata Logging:** Record GPS coordinates, elevation (in meters above sea level), date/season, and immediate soil type.
3. **Conservation Ethics:** Follow non-destructive botanical photography guidelines without uprooting wild specimens.
