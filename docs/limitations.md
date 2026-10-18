# Limitations & Boundary Conditions · Herbalist AI

Every responsible machine learning deployment must clearly articulate its scientific failure modes and operational boundaries.

---

## 1. Domain & Biogeographic Scope
- **Geographic Bias**: The primary image backbone was trained on **VNPlant-200** (predominantly tropical and sub-tropical Asian taxa). High-altitude alpine species endemic to the Kashmir Himalaya (*Gentiana kurroo*, *Saussurea costus*, *Fritillaria roylei*) are currently resolved via taxonomic catalogs and tabular matching until expanded alpine field callsets are integrated.
- **Micro-Environmental Chemical Variation**: The active secondary metabolites displayed in field reports are catalog reference figures. Real-world concentrations of marker compounds (*atisine*, *berberine*, *podophyllotoxin*) fluctuate dramatically with altitude, solar radiation, soil microbiome, and seasonal phenology.

---

## 2. Computer Vision Limitations
- **Resolution Downsampling**: Resizing field captures to $180 \times 180$ discards sub-millimeter microscopic foliar structures, such as glandular trichomes, stomatal density, and tertiary venation, which botanists rely upon to differentiate sister species.
- **Phenotypic Plasticity**: A single plant species may exhibit sun vs. shade leaf heteroblasty, senescence, or insect damage that degrades classification accuracy.
- **Toxic Lookalikes**: Certain lethal species visually mimic edible or mild medicinal herbs. AI predictions must never replace chromatographic (TLC/HPLC) or herbarium-verified botanical identification.

---

## 3. Agronomic Sensor Precision
- **Commercial Soil Probes**: Handheld or inexpensive multi-parameter probes measure electrical conductivity as a proxy for ionic concentrations; they do not distinguish between nitrate, phosphate, and sulfate ions without calibrated laboratory chemical extraction.
- **Sensor Drift**: Live soil EC and pH probes require periodic two-point buffer recalibration ($pH 4.01$ and $pH 7.00$) to prevent drift.
