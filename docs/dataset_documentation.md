# Dataset Documentation · Herbalist AI

## 1. Overview & Data Sources

Herbalist AI utilizes a multimodal data corpus comprising high-resolution foliar/floral imagery, clinical/ethnopharmacological catalogs, and agronomic soil chemistry.

```
data/
├── raw/
│   ├── clinical/
│   │   ├── Kashmere.csv            # 15 Kashmir Himalayan endemic medicinal taxa
│   │   └── medicinal.csv           # 200 VNPlant-200 species benchmark catalog
│   └── imaging/                    # Unprocessed field captures
├── interim/                        # Cleaned & standardized staging tables
├── processed/
│   ├── kashmir_medicinal.csv       # Validated Kashmir flora with genus and toxicity encodings
│   └── medicinal.csv               # 200 species master serving catalog
└── manifests/
    ├── dataset_manifest.json       # SHA-256 cryptographic verification manifest
    └── imagesamplecount.csv        # Class sample distribution
```

---

## 2. Kashmir High-Altitude Medicinal Flora (`data/processed/kashmir_medicinal.csv`)

Kashmir's unique biogeography and high alpine altitudes (1,800m – 4,500m AMSL) foster endemic flora renowned in Ayurvedic, Unani, and traditional Kashmiri folk medicine.

| Taxon | Local/Common Name | Family | Active Phytochemicals | IUCN Red List Status | Primary Traditional Application |
|---|---|---|---|---|---|
| **Aconitum heterophyllum** | Indian Atees | Ranunculaceae | Atisine, aconitine (non-toxic form) | **Endangered** | Antiperiodic, dyspepsia, fever |
| **Artemisia absinthium** | Wormwood / Tethwan | Asteraceae | Thujone, absinthin | Least Concern | Antiparasitic, liver ailments |
| **Berberis lycium** | Kashmiri Barberry / Kawdakh | Berberidaceae | Berberine, palmatine | **Near Threatened** | Ophthalmia, jaundice, glycemic control |
| **Colchicum luteum** | Yellow Colchicum / Suranjan-i-Talkh | Colchicaceae | Colchicine | **Vulnerable** | Acute gout, rheumatism |
| **Datura stramonium** | Thorn Apple / Dhatura | Solanaceae | Scopolamine, hyoscyamine | Least Concern | Analgesic, bronchodilator (toxic) |
| **Fritillaria roylei** | Himalayan Fritillary / Sheethkhar | Liliaceae | Peimine, peiminine | **Endangered** | Chronic cough, expectorant |
| **Gentiana kurroo** | Indian Gentian / Nilkanth | Gentianaceae | Gentiopicrin, amarogentin | **Critically Endangered** | Gastric stimulant, hepatoprotection |
| **Hyoscyamus niger** | Henbane / Bazarbhang | Solanaceae | Hyoscyamine, scopolamine | Least Concern | Antispasmodic, neurological sedatives |
| **Jurinea dolomiaea** | Dhoop / Gugal | Asteraceae | Essential oils, sesquiterpenes | **Near Threatened** | Fumigation, antiseptics |
| **Picrorhiza kurroa** | Kutki / Kour | Plantaginaceae | Kutkin, picroside I & II | **Endangered** | Autoimmune, hepatomegaly, jaundice |
| **Podophyllum hexandrum** | Himalayan Mayapple / Bankakri | Berberidaceae | Podophyllotoxin | **Endangered** | Antineoplastic, condyloma acuminata |
| **Rheum emodi** | Himalayan Rhubarb / Pambchalan | Polygonaceae | Rhein, emodin, chrysophanol | **Vulnerable** | Purgative, astringent, hemostatic |
| **Saussurea costus** | Kuth / Costus | Asteraceae | Costunolide, dehydrocostus lactone | **Critically Endangered** (CITES I) | Bronchial asthma, ulcers, skin diseases |
| **Taxus wallichiana** | Himalayan Yew / Posthal | Taxaceae | Paclitaxel (Taxol) | **Endangered** | Chemotherapeutic antineoplastic |
| **Valeriana jatamansi** | Indian Valerian / Mushkbala | Caprifoliaceae | Valerenic acid, jatamansone | **Near Threatened** | Anxiety, neurosis, insomnia |

---

## 3. Global Benchmark Dataset (`data/processed/medicinal.csv`)

- **Total Classes**: 200 species.
- **Image Corpus**: VNPlant-200 (17,973 images total: 12,000 training, 5,973 validation/test).
- **Taxonomic Diversity**: Malvaceae, Fabaceae, Asteraceae, Zingiberaceae, Acanthaceae, Solanaceae, Lamiaceae, and related medicinal angiosperms.
- **Attributes per Class**:
  - `Scientificname`: Binomial nomenclature (e.g. *Aloe vera*, *Centella asiatica*).
  - `Biologicalname`: Common vernacular or botanical synonym.
  - `Medicinalvalue`: Verified therapeutic and clinical pharmacological indications.
  - `Family`: Botanical plant family.
  - `ActiveCompounds`: Key secondary metabolites (alkaloids, flavonoids, terpenoids, saponins, glycosides).
  - `ToxicityLevel`: None, Low, Moderate, High, or Extreme.
  - `GeographicalDistribution`: Native ecological biomes.
  - `GrowthHabit`: Herb, Shrub, Tree, Climber, Succulent.
  - `PartsUsed`: Leaves, Rhizomes, Roots, Bark, Seeds, Flowers, Whole Plant.
  - `PreparationMethods`: Infusion, Decoction, Poultice, Maceration, Tincture, Controlled extraction.

---

## 4. Worldwide & India Datasets Tracked for Future Fine-Tuning

| Dataset Name | Scope & Taxa | Access Mechanism | Disk Footprint | Intended Future Usage |
|---|---|---|---|---|
| **Indian Medicinal Leaves (Kaggle)** | 80 Common Indian taxa | Kaggle API (`aryashah2k/indian-medicinal-leaves-dataset`) | ~9.2 GB | Subcontinent domain expansion |
| **Mendeley Indian Medicinal Plants** | 40 Ayurvedic species, 4000+ photos | Mendeley Data DOI:10.17632/nny2ndvf38.1 | ~2.5 GB | Cross-dataset domain generalization |
| **PlantVillage** | 14 Crop species, 38 healthy/diseased classes | Kaggle (`abdallahalidev/plantvillage-dataset`) | ~1.5 GB | Foliar disease & stress IPM transfer learning |
| **PlantDoc** | In-the-wild field crop disease imagery | GitHub (`pratikkayal/PlantDoc-Dataset`) | ~800 MB | Robustness under occluded, noisy field conditions |
| **GBIF Kashmir Occurrence Coordinates** | Alpine coordinates and observation points | GBIF REST API | ~50 MB | Spatial bioclimatic validation |
| **KNApSAcK & COCONUT** | Comprehensive phytochemistry and natural products | Open REST / SDF download | ~400 MB | Automated LC-MS / HPLC compound mapping |
