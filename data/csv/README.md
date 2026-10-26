# Canonical Dataset & Knowledge CSV Directory

All tabular datasets, botanical knowledge catalogs, and agronomic parameters
in Herbalist AI are centrally consolidated in this directory:

### 🌟 Core Canonical CSV Files (Unified 216 Taxa: 200 Global + 16 Kashmir)

| Canonical CSV File | Records | Key Attributes & Focus |
| :--- | :--- | :--- |
| `medicinal.csv` | **216** | Master catalog: Botanical taxonomy, Kashmiri/Hindi vernacular, bioactive chemomarkers, Ayurvedic/Unani attributes, IUCN status, elevation envelopes, safe clinical indications. |
| `fertiliser.csv` (mirror `fertilizer.csv`) | **216** | Species-specific agronomy: Basal FYM (t/ha), specific N-P-K kg/ha ratios, application schedules, biofertilizers (VAM, Azotobacter, Rhizobium), micronutrients, and species-specific hazards to avoid. |
| `chemicaltaxonomy.csv` | **216** | Phytochemical & Cytogenetic profile: Plant order, primary/secondary chemical classes, biosynthetic pathways (MEP, MVA, Shikimate), diagnostic chemomarkers, 2n karyotypes, and hybridization objectives. |

---

### 📚 Specialized Agronomic & Research Catalogs

| Catalog Name | Records | Scientific Scope |
| :--- | :--- | :--- |
| `kashmir_medicinal_plants.csv` | **16** | Priority high-altitude Kashmir endemic taxa (including *Crocus sativus*, *Gentiana kurroo*, *Picrorhiza kurroa*, *Saussurea costus*, *Aconitum heterophyllum*). |
| `chemotaxonomy_hybridization.csv` | **12** | Inter-specific breeding pairs, genetic distances, chromosome numbers, and secondary metabolite synergy models. |
| `agronomic_cultivation_protocols.csv` | **216** | Propagation methods (stratified seed, corms, rhizomes, stem cuttings), planting windows, spacing, shade envelopes, yields. |
| `phytopathology_disease_ipm.csv` | **216** | Species-specific disease threats (Fusarium, Pythium, Cercospora, blights), preventative sanitation, and biological controls. |
| `soil_pedological_requirements.csv` | **216** | Soil textures (Karewa loam, scree, sand), pH ranges, N-P-K bands, and irrigation strategies. |
| `biochemical_literature.csv` | **216** | Pharmacological literature citations, primary and secondary metabolites, chromatographic assay standards. |
| `kashmir_dslr_splits.csv` | Variable | Audit logs and stratified splits for locally ingested high-resolution DSLR camera raw captures. |
| `tabular_splits/` | Sub-dir | Contains stratified train/val/test splits for tabular metadata models (`plants_tabular_*.csv`). |

---

### 📷 Note on Vision vs Tabular Datasets
- **Vision Image Training Data**: Stored in `data/processed/train/<class_name>/`, `data/processed/val/<class_name>/`, and `data/processed/test/<class_name>/` (containing actual `.jpg` images partitioned by species).
- **Tabular Data**: Stored strictly in this directory (`data/csv/`).
