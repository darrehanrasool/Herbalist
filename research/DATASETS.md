# Research dataset log

Keep every source here for the thesis bibliography. **Do not mix all of these into one softmax.** Use them by task.

## Vision — species ID

| Dataset                                 | What it is                                                                | Link                                                                                                                                                                                                                              | Local folder                   | Status                                      |
| --------------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | ------------------------------------------- |
| VNPlant-200                             | 200 VN medicinal species, ~20k images; **this is the BTech training set** | Paper: <https://www.researchgate.net/publication/341667837_VNPlant-200_-_A_Public_and_Large-Scale_of_Vietnamese_Medicinal_Plant_Images_Dataset> · Images (community mirror): <https://github.com/kencoca/VietNam-Medicinal-Plant> | `data/raw/kaggle/vnplant-200/` | Download via `scripts/download_datasets.py` |
| Indian medicinal leaves (Kaggle search) | Extra Indian taxa for MTech                                               | <https://www.kaggle.com/search?q=medicinal+plant+leaves>                                                                                                                                                                          | `data/raw/kaggle/`             | Needs Kaggle API token                      |
| iNaturalist Research-grade              | Wild photos, noisy but huge                                               | <https://www.inaturalist.org> · GBIF Darwin Core                                                                                                                                                                                  | research only                  | Stream later; do not dump whole archive     |
| PlantCLEF / LifeCLEF                    | Fine-grained plant ID benchmarks                                          | <https://www.imageclef.org/>                                                                                                                                                                                                      | research only                  | Benchmark, not farmer UX                    |

## Vision — disease / stress

| Dataset      | What it is                            | Link                                                                  | Use                                                       |
| ------------ | ------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------- |
| PlantVillage | Crop leaf disease (mostly food crops) | <https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset> | Transfer ideas to medicinal IPM; **not** medicinal labels |
| PlantDoc     | In-the-wild disease photos            | <https://github.com/pratikkayal/PlantDoc-Dataset>                     | Harder than PlantVillage                                  |

## Names, geography, ethnobotany

| Dataset                                | Link                                                | Use                                        |
| -------------------------------------- | --------------------------------------------------- | ------------------------------------------ |
| GBIF occurrences                       | <https://www.gbif.org>                              | Country/state occurrence, not ID model     |
| POWO / WCVP (Kew)                      | <https://powo.science.kew.org>                      | Accepted scientific names                  |
| Herbolario (Philippines ethnomedicine) | <https://ipt.pensoft.net/resource?r=herbolariodata> | Use records                                |
| This repo BTech catalog                | `data/raw/catalog/medicinal.csv`                    | Serving table                              |
| Kashmir list                           | `data/raw/catalog/kashmir_medicinal.csv`            | Himalayan taxa **not in** Xception classes |

## Chemistry (literature, not your HPLC)

| Dataset                                               | Link                                                              | Use                          |
| ----------------------------------------------------- | ----------------------------------------------------------------- | ---------------------------- |
| KNApSAcK                                              | <http://www.knapsackfamily.com/>                                  | Species–compound occurrences |
| WikiData phytochemistry + VascularPlantChemodiversity | <https://github.com/alrichardbollans/VascularPlantChemodiversity> | Compound lists               |
| COCONUT / LOTUS                                       | <https://coconut.naturalproducts.net>                             | Natural product structures   |

## Soil / pedology / agronomy

| Dataset                               | Link                                            | Use                                         |
| ------------------------------------- | ----------------------------------------------- | ------------------------------------------- |
| Kaggle soil NPK / crop recommendation | <https://www.kaggle.com/search?q=soil+npk+crop> | Reference crop nutrient ranges              |
| ISRIC SoilGrids                       | <https://soilgrids.org>                         | Regional soil maps & pedological attributes |
| ICAR / NMPB crop advisories           | <https://nmpb.nic.in>                           | Cultivation & agronomic practices           |

## Scientific Reproducibility & Integrity Standards

This platform strictly enforces independent dataset partitions (train 70%, val 13%, test 17%) with zero data leakage. Evaluations reported in publication figures are conducted strictly on the independent, held-out test split.
