# Research Gaps: Kashmir High-Altitude Medicinal Plants & Future Work

## Identified Research Gaps

### 1. Scarcity of High-Altitude Alpine Image Datasets
While tropical and temperate food crops (PlantVillage, VNPlant) have tens of thousands of labeled foliar images, **endemic high-altitude Himalayan medicinal flora** (*Gentiana kurroo*, *Saussurea costus*, *Picrorhiza kurroa*, *Fritillaria roylei*) lack public benchmark vision callsets.
- **Proposed Solution**: Author field collection scripts and herbarium digitization protocols in collaboration with regional institutes (IUST Kashmir, University of Kashmir, IIIM Jammu).

### 2. Microclimate & Elevational Phenotype Shifts
Alpine plants exhibit morphological dwarfing, altered leaf pubescence, and anthocyanin pigmentation at 3,000m+ compared to lower valley specimens. Models trained strictly on lowland photography suffer domain shift when evaluated on alpine ridges.
- **Proposed Solution**: Domain adaptation with elevation-conditioned positional embeddings and self-supervised contrastive learning.

### 3. Multimodal Integration of Soil Chemistry with Foliar Vision
Existing computer vision systems treat classification purely as pixel mapping, ignoring soil chemistry. However, phytochemical potency is directly coupled to soil NPK, pH, and electrical conductivity.
- **Proposed Solution**: Multimodal fusion network combining foliar image embeddings with tabular soil sensor readings.
