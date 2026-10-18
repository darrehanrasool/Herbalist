# Data Dictionary · Herbalist AI

This document establishes the precise metadata definitions, data types, constraints, and valid ranges for all tables across the repository.

---

## 1. Primary Catalog Schema (`data/processed/medicinal.csv` & `kashmir_medicinal.csv`)

| Field Name | Type | Nullable | Description & Constraints | Example Value |
|---|---|---|---|---|
| `Scientificname` | `string` | No | Accepted botanical binomial nomenclature (Genus species authority). Unique identifier. | `Saussurea costus` |
| `Biologicalname` | `string` | No | Common botanical synonym or widely accepted vernacular English name. | `Kuth` |
| `Medicinalvalue` | `string` | No | Pharmacological actions, therapeutic efficacy, and ethnomedicinal indications. | `Used for bronchial asthma, wound healing, and ulcers.` |
| `Family` | `string` | No | Angiosperm family classification (APG IV system). | `Asteraceae` |
| `CommonUses` | `string` | No | Primary clinical symptom targets or formulation types. | `Asthma, wound healing` |
| `ActiveCompounds` | `string` | Yes | Identified bioactive secondary metabolites (alkaloids, terpenoids, glycosides). | `Costunolide, dehydrocostus lactone` |
| `ToxicityLevel` | `string` | No | Categorical toxicity risk index: `None`, `Low`, `Moderate`, `High`, `Extreme`. | `Low` |
| `GeographicalDistribution` | `string` | Yes | Native ecological range or geopolitical distribution. | `Himalayas (Kashmir)` |
| `GrowthHabit` | `string` | Yes | Morphological architecture: `Herb`, `Shrub`, `Tree`, `Vine`, `Climber`, `Succulent`. | `Herb` |
| `PartsUsed` | `string` | Yes | Harvested plant organ: `Roots`, `Leaves`, `Bark`, `Seeds`, `Flowers`, `Rhizomes`. | `Roots` |
| `PreparationMethods` | `string` | Yes | Pharmacognostic processing: `Infusion`, `Decoction`, `Powder`, `Tincture`, `Oil`. | `Powder, Oil` |
| `ConservationStatus` | `string` | No | IUCN Red List conservation category: `Critically Endangered`, `Endangered`, `Vulnerable`, `Near Threatened`, `Least Concern`, `Not Evaluated`. | `Critically Endangered` |
| `Genus` | `string` | Generated | First token extracted from `Scientificname`. | `Saussurea` |
| `Toxicity_Ordinal` | `integer` | Generated | Numerical mapping: `0` (None), `1` (Low), `2` (Moderate), `3` (High), `4` (Extreme). | `1` |

---

## 2. Soil Requirements Schema (`knowledge/soil_requirements.csv`)

| Field Name | Type | Valid Range | Units | Description |
|---|---|---|---|---|
| `Scientificname` | `string` | N/A | Foreign Key | Links to primary plant catalog. |
| `pH_Min` | `float` | 3.5 – 9.0 | pH units | Minimum soil pH tolerance before chlorosis or nutrient lockout occurs. |
| `pH_Max` | `float` | 4.0 – 9.5 | pH units | Maximum soil pH tolerance. |
| `N_Min_mg_kg` | `float` | 0 – 300 | mg/kg | Minimum available elemental Nitrogen in root zone. |
| `P_Min_mg_kg` | `float` | 0 – 200 | mg/kg | Minimum available Phosphorus (P2O5 equivalent). |
| `K_Min_mg_kg` | `float` | 0 – 300 | mg/kg | Minimum available Potassium (K2O equivalent). |
| `Moisture_Min_pct`| `float` | 5 – 80 | % | Minimum volumetric soil moisture content. |
| `Moisture_Max_pct`| `float` | 10 – 95 | % | Field water capacity threshold before root hypoxia. |
| `Temp_Min_C` | `float` | -15 – 35 | °C | Minimum thermal growth envelope (crucial for alpine taxa). |
| `Temp_Max_C` | `float` | 15 – 50 | °C | Thermal stress upper ceiling. |

---

## 3. Real-Time Soil Sensor Ingestion Schema (`/api/sensors/ingest`)

| Parameter | Type | Required | Range | Description |
|---|---|---|---|---|
| `device_id` | `string` | Yes | Alphanumeric | Unique probe or IoT gateway identifier (e.g. `kashmir-field-01`). |
| `pH` | `float` | Yes | 0.0 – 14.0 | Direct probe potential of hydrogen reading. |
| `N` | `float` | Optional | 0.0 – 500.0 | Soil nitrogen concentration. |
| `P` | `float` | Optional | 0.0 – 500.0 | Soil phosphorus concentration. |
| `K` | `float` | Optional | 0.0 – 500.0 | Soil potassium concentration. |
| `moisture` | `float` | Optional | 0.0 – 100.0 | Soil moisture percentage. |
| `temperature` | `float` | Optional | -40.0 – 80.0 | Probe temperature in Celsius. |
| `ec` | `float` | Optional | 0.0 – 10.0 | Electrical conductivity in mS/cm. |
| `timestamp` | `string` | Auto-generated | ISO-8601 | UTC timestamp of observation. |
