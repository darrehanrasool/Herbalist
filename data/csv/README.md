# Canonical Dataset & Knowledge CSV Directory

All tabular datasets, botanical knowledge catalogs, and agronomic parameters
in Herbalist AI are centrally consolidated in this directory using unified
`snake_case` naming standards:

| Canonical CSV Name | Records | Description & Standard |
| :--- | :--- | :--- |
| `medicinal_plants_master.csv` | 215 | 22-attribute global + Kashmir flora master (POWO/ICMR/AYUSH) |
| `kashmir_medicinal_plants.csv` | 15 | Priority high-altitude Kashmir endemic taxa (IUCN RedList) |
| `chemotaxonomy_hybridization.csv` | 12 | Interspecific breeding pairs, 2n karyotypes & metabolite synergy |
| `soil_pedological_requirements.csv`| 215 | pH ranges, soil textures, N-P-K bands & moisture envelopes |
| `agronomic_cultivation_protocols.csv`| 215 | Ex-situ propagation methods, harvest cycles, yield notes |
| `nutrient_fertilizer_guidelines.csv`| 215 | Farmyard manure (FYM t/ha), organic NPK strategies, micronutrients |
| `phytopathology_disease_ipm.csv` | 215 | Integrated pest management (IPM) & biological crop protection |
| `biochemical_literature.csv` | 200 | Pharmacological bioactives, traditional indications, preparation |
| `dataset_image_sample_counts.csv` | 200 | Image sample counts per taxon in training/val splits |
