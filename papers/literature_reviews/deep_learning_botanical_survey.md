# State of the Art: Deep Learning in Botanical Vision & Ethnopharmacology

## 1. Evolution of Plant Identification Models
Early automated plant recognition relied upon hand-crafted morphometric descriptors:
- Leaf shape eccentricity, aspect ratio, and perimeter-to-area circularity.
- Texture descriptors using Gray-Level Co-occurrence Matrices (GLCM) and Gabor wavelets.
- Curvature scale-space (CSS) boundary contour matching.

These hand-engineered features suffered severe degradation when confronted with in-the-wild field variations, occlusions, non-uniform background soil, insect perforations, and illumination dynamics.

With the advent of deep convolutional neural networks (AlexNet, VGG, ResNet, Inception, Xception), learned hierarchical representations displaced manual feature extraction. Modern botanical benchmarks (LifeCLEF, PlantNet, VNPlant-200) consistently demonstrate that **pretrained transfer learning** achieves Top-1 accuracies surpassing 94% on fine-grained species datasets.

---

## 2. Kashmir High-Altitude Alpine Flora: The Conservation Imperative
The Kashmir Himalaya represents a global biodiversity hotspot with extensive alpine meadows (Margs) and high endemism. Due to habitat fragmentation, unregulated bioprospecting, and climate change, species such as *Saussurea costus*, *Gentiana kurroo*, and *Aconitum heterophyllum* are severely threatened.

Digital automated identification provides two vital capabilities:
1. **Field Conservation Enforcement**: Enables forestry officials and field researchers to identify endangered taxa on-site.
2. **Cultivation & Agronomy Transition**: Provides precision farming advisories (soil pH, NPK balance, harvest cycles) enabling farmers to cultivate medicinal herbs ex-situ, alleviating wild harvesting pressure.
