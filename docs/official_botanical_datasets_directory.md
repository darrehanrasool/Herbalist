# Official Botanical Repositories, Dataset Directory & Kashmir Field Protocol

[![Institution: IUST Kashmir](https://img.shields.io/badge/Institution-CAI%20%7C%20IUST%20Kashmir-blue.svg)](https://iust.ac.in)
[![License: Strict Academic](https://img.shields.io/badge/License-Strict%20Academic%20Research-red.svg)](../LICENSE)
[![Standards: POWO%20%7C%20ICMR%20%7C%20NMPB](https://img.shields.io/badge/Standards-POWO%20%7C%20ICMR%20%7C%20NMPB-brightgreen.svg)](https://powo.science.kew.org)

This document establishes the official scientific data lineage, authoritative botanical repositories, and in-situ field collection protocols for the **Herbalist AI** platform, developed at the **Centre of Artificial Intelligence, Islamic University of Science and Technology (IUST), Kashmir**.

---

## 👥 Authorship & Research Governance

| Role | Investigator | Designation & Affiliation | Research Responsibilities |
| :--- | :--- | :--- | :--- |
| **Faculty Research Supervisor** | **Dr. M Abdul Jawad** | Professor & Faculty Supervisor, Centre for Artificial Intelligence, IUST | Research Conceptualization, Botanical Taxonomy Supervision & Strategic Architecture Direction |
| **Faculty Research Supervisor** | **Dr. Riyaz Ahmed** | Professor & Faculty Supervisor, Centre for Artificial Intelligence, IUST | Co-Supervision, System Architecture Advisory & Theoretical Oversight |
| **Contributing Researcher** | **Dar Rehan Rasool** | M.Tech Student, Centre for Artificial Intelligence, IUST | Dual-Tier Vision Models, Agronomic Pedology Pipeline & Scientific Engine Implementation |
| **Contributing Researcher** | **Muneeb Syed Shah** | M.Tech Student, Centre for Artificial Intelligence, IUST | High-Altitude Kashmir DSLR Collection Protocol, Agronomic Soil Modeling & Cross-Dataset Evaluation |
| **Contributing Researcher** | **Shafiya Bashir Pampori** | M.Tech Student, Centre for Artificial Intelligence, IUST | Pharmacognosy Data Modeling, Telemetry Quality Auditing & Taxonomic Data Integrity |

---

## 🏛️ Authoritative Botanical & Pharmacognosy Repositories

All taxon definitions, chemical classes, and agronomic attributes in Herbalist AI are anchored strictly to authenticated botanical authorities to prevent hallucination and reviewer rejection:

### 1. Royal Botanic Gardens, Kew: Plants of the World Online (POWO)
- **Role**: Primary international taxonomic backbone and nomenclatural authority.
- **Coverage**: Verification of valid botanical binomials, author citations, accepted synonyms, and world geographical distribution.
- **Accession Portal**: [https://powo.science.kew.org](https://powo.science.kew.org)
- **Usage in Herbalist**: Sanitizes scientific binomials (e.g. confirming *Picrorhiza kurroa* Royle ex Benth. vs *Neopicrorhiza scrophulariiflora*).

### 2. Indian Council of Medical Research (ICMR)
- **Compendium**: *Quality Standards of Indian Medicinal Plants* (Volumes 1–22) & *Medicinal Plants of India Monographs*.
- **Coverage**: Thin-layer chromatography (TLC), high-performance liquid chromatography (HPLC) quantitative assay standards, macroscopic and microscopic pharmacognostic markers.
- **Usage in Herbalist**: Chemical class profiles, primary bioactives (e.g., amarogentin, podophyllotoxin, picroside I & II, atisine), and therapeutic dosage safety limits.

### 3. National Medicinal Plants Board (NMPB), Ministry of AYUSH, Govt of India
- **Mandate**: Conservation, sustainable harvesting, and agro-technological cultivation packages for high-value commercial and endangered medicinal plants.
- **Coverage**: Soil pH requirements, N-P-K nutrient regimens, nursery propagation, seed stratification protocols, and altitude thresholds.
- **Accession Portal**: [https://www.nmpb.nic.in](https://www.nmpb.nic.in)
- **Usage in Herbalist**: Pedological envelopes in `knowledge/soil_requirements.csv` and ex-situ cultivation parameters in `knowledge/cultivation.csv`.

### 4. Botanical Survey of India (BSI) & Flora of Jammu & Kashmir
- **Monographs**: *Flora of Jammu and Kashmir* (Vols 1–3), *Red Data Book of Indian Plants*.
- **Coverage**: Altitudinal zoning (Montane, Sub-Alpine, Alpine Moraine), flowering phenology, endemism records, and micro-habitat notes across the Kashmir Valley, Pir Panjal, and Zanskar ranges.
- **Usage in Herbalist**: Baseline elevation ranges (`optimal_altitude_min_m`, `optimal_altitude_max_m`) and endemic status flags in `knowledge/medicinal_plants_global_curated.csv`.

### 5. VNPlant-200 Asian Medicinal Flora Benchmark
- **Coverage**: 200 medicinal taxa, over 25,000 field and botanical garden captures covering diverse Asian therapeutic flora.
- **Role**: Standardized multi-class visual recognition benchmark for transfer learning, baseline evaluation, and feature extraction.

### 6. ChEMBL & PubChem Molecular Databases
- **Accession Portals**: [ChEMBL (EMBL-EBI)](https://www.ebi.ac.uk/chembl/) · [PubChem (NCBI)](https://pubchem.ncbi.nlm.nih.gov/)
- **Usage in Herbalist**: Bioactive chemical structure cross-referencing, molecular SMILES, IUPAC identifiers, and known pharmacodynamics.

---

## 📸 Kashmir High-Altitude DSLR Field Protocol (`data/raw/kashmir/`)

To support genuine, unassailable academic contributions from the Himalayan region, the platform maintains a segregated raw image ingestion pipeline for Kashmir native and endangered flora.

### 1. Geographical & Elevation Zonation
Field expeditions must record GPS coordinates and elevation via barometric altimeter across four key ecological zones:

```
ECOLOGICAL ZONE                       ELEVATION RANGE         REPRESENTATIVE TAXA
Zone IV: High Alpine Scree / Moraine  3600m – 4400m a.s.l.   Picrorhiza kurroa, Jurinea dolomiaea
Zone III: Sub-Alpine Betula Ravines   2800m – 3600m a.s.l.   Aconitum heterophyllum, Saussurea costus, Rheum emodi
Zone II: Temperate Coniferous Forest  1800m – 2800m a.s.l.   Gentiana kurroo, Podophyllum hexandrum, Taxus wallichiana
Zone I: Montane Valley Scrub          1400m – 1800m a.s.l.   Berberis lycium, Artemisia absinthium, Colchicum luteum
```

### 2. Camera Hardware & Capture Parameters
- **Sensor Format**: 35mm Full-Frame or APS-C DSLR / Mirrorless (e.g. Nikon D850/Z6, Canon EOS R5/90D, Sony A7R).
- **Optics**: 100mm f/2.8 Macro Lens (for floral organ details) + 24-70mm f/2.8 (for whole-plant habitus).
- **Exposure Standards**:
  - Color Calibration: X-Rite ColorChecker Passport placed in initial shot under ambient alpine light.
  - File Format: Uncompressed 14-bit RAW (.NEF / .CR3 / .ARW) + Fine JPEG.
  - ISO: Base ISO (100–400) to eliminate sensor grain.
  - Aperture: $f/5.6 - f/11$ for complete depth-of-field across anatomical features.

### 3. Multi-Organ Anatomical Coverage (5 Angles Per Specimen)
Every specimen in `data/raw/kashmir/<genus_species>/` must have photographic documentation across 5 distinct organs:
1. `01_habit.jpg`: Whole plant in its native micro-habitat (soil, rocks, companion species).
2. `02_adaxial_leaf.jpg`: Upper leaf surface showing venation and trichomes.
3. `03_abaxial_leaf.jpg`: Lower leaf surface showing stomatal bands or glands.
4. `04_inflorescence.jpg`: Flower / inflorescence macro showing corolla, calyx, stamen, and pistil.
5. `05_rhizome_stem.jpg`: Root, bulb, corm, or woody stem cross-section where ethically permissible.

### 4. Non-Destructive Ethical Compliance
- Under Jammu & Kashmir Forest Protection Rules and National Biodiversity Authority (NBA) guidelines, **uprooting of Critically Endangered taxa (*Gentiana kurroo*, *Saussurea costus*, *Aconitum heterophyllum*) is strictly prohibited**.
- Root and rhizome morphological records must be obtained non-destructively through exposed scree crevices or cultivated nursery germplasm (e.g., IIIM Field Stations, University Botanical Gardens).

---

## 🧬 Chemotaxonomic Hybridization Methodology

The interspecific hybridization matrix (`knowledge/chemotaxonomy_hybridization.csv`) models cross-breeding potential to resolve the severe supply bottleneck of wild-harvested Himalayan endemics:

$$H_{\text{compat}} = \left(1 - \frac{|2n_1 - 2n_2|}{2n_1 + 2n_2}\right) \times (1 - D_{\text{genomic}})$$

Where:
- $2n_1, 2n_2$: Somatic chromosome numbers of parent species 1 and parent species 2.
- $D_{\text{genomic}}$: Interspecific genetic divergence index derived from ITS / matK / rbcL barcode sequence alignment.
- $H_{\text{compat}}$: Cytogenetic compatibility index governing F1 embryo rescue feasibility.

---

## 🔬 Directory Structure & Storage Manifest

```
data/
├── raw/
│   ├── kashmir/                      # Segregated Kashmir DSLR field photography
│   │   ├── Aconitum_heterophyllum/   # In-situ sub-alpine captures
│   │   ├── Gentiana_kurroo/          # Grassy slope captures
│   │   ├── Picrorhiza_kurroa/        # High alpine moraine captures
│   │   ├── Podophyllum_hexandrum/    # Forest understory captures
│   │   └── Saussurea_costus/         # Cultivated / conservation reserve captures
│   └── kaggle/
│       └── vnplant-200/              # Standard multi-class Asian flora benchmark
├── interim/                          # Standardized 512x512 normalized intermediates
└── processed/                        # Train / Val / Test stratified 180x180 splits
    ├── train/
    ├── val/
    ├── test/
    └── medicinal.csv                 # Production master catalog (215 species)
```

---

## 📜 Academic Reproducibility Checklist

- [x] All non-medicinal monoculture crops (`rice-leaf-diseases`, generic crop recommender) purged from the workspace.
- [x] Master botanical catalog (`knowledge/medicinal_plants_global_curated.csv`) populated with 22 authenticated attributes across 215 species.
- [x] Chemotaxonomic cross-breeding catalog (`knowledge/chemotaxonomy_hybridization.csv`) verified against botanical pharmacopeias.
- [x] 10 Publication-grade 300 DPI figures generated in `reports/figures/` and synced to `api/static/graphs/`.
- [x] Scientific dossier download API (`/api/export/json/<species>`, `/api/export/csv/<species>`) active on web platform.
- [x] Full unit test suite verified (`18/18 tests passing`).
