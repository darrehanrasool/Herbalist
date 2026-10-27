# Canonical Dataset & Knowledge CSV Directory

All tabular datasets, botanical knowledge catalogs, agronomic parameters, and label mappings in Herbalist AI are centrally consolidated in this directory:

### 🌟 4 Canonical Master CSV Catalogs (216 Taxa: 200 Working Model + 16 Kashmir Future)

Every single record across all 4 master CSVs has been enriched with authoritative, non-repetitive botanical, agronomic, phytochemical, and phytopathological data from POWO 2024, ICMR, AYUSH, and CSIR-CIMAP:

| Canonical CSV File | Records | Key Scientific Scope & Attributes |
| :--- | :--- | :--- |
| `medicinal.csv` | **216** | Botanical taxonomy, Kashmiri/Hindi/Vernacular names, bioactive chemomarkers, Ayurvedic/Unani/Siddha rasapanchaka, IUCN Red List status, altitude envelopes, soil pH range, toxicological warnings, and pharmacopeial standards. |
| `fertiliser.csv` | **216** | Precision agronomic requirements: Basal FYM (t/ha), specific N-P-K kg/ha ratios, split application schedules, biofertilizers (Azotobacter, PSB, VAM), micronutrients (Zn, B), irrigation strategies, yield expectations, and hazards to avoid. |
| `chemicaltaxonomy.csv` | **216** | Chemotaxonomy & cytogenetics: Taxonomic order, primary and secondary chemical classes, dominant secondary metabolites, biosynthetic pathways, diagnostic chemomarkers, diploid karyotypes ($2n$), congeneric relatives, hybridization compatibility, and altitude chemodiversity. |
| `disease.csv` | **216** | Phytopathology & IPM: Major fungal, bacterial, viral diseases, diagnostic foliar symptoms, preventative cultural sanitation, biological organic IPM controls, and strict chemical pesticide warnings. |

---

### 🗺️ Unified Neural Label Mapping (`label_mapping.csv`)

| Mapping File | Records | Purpose |
| :--- | :--- | :--- |
| `label_mapping.csv` | **216** | One-to-one mapping connecting neural network output indices (`0..199` for Model 1, `200..215` for Model 2), dataset folder names, scientific names, vernacular names, botanical families, and unique `HERB-xxx` IDs across all 4 master CSVs. |

---

### 📁 Tabular Splits
- `tabular_splits/`: Contains stratified train/val/test splits for tabular metadata models (`plants_tabular_train.csv`, `plants_tabular_val.csv`, `plants_tabular_test.csv`).

---

### 📷 Vision Datasets Directory Structure
- **Working Model (200 Taxa)**: `data/working_model/train/`, `data/working_model/val/`, `data/working_model/test/`
- **Kashmir Model (16 Taxa)**: `data/kashmir/train/`, `data/kashmir/val/`, `data/kashmir/test/`
