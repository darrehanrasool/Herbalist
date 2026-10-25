# Security Policy · Herbalist-AI

## 1. Supported Versions

We provide security patches, integrity audits, and vulnerability updates for the following releases of Herbalist-AI:

| Version | Supported | Status | Notes |
| :--- | :--- | :--- | :--- |
| **2.0.x** | :white_check_mark: | **Active / Current** | Enterprise modular architecture & Kashmir multi-modal fusion |
| **1.0.x** | :x: | **Deprecated** | Legacy B.Tech monolithic implementation |

---

## 2. Research & AI Platform Security Priorities

Herbalist-AI operates at the intersection of deep vision, ethnopharmacology, and agricultural IoT telemetry. We enforce strict defensive security across four critical domains:

### 2.1 Model Serialization & Deserialization Security
- **Arbitrary Code Execution Prevention**: Deserializing untrusted model weights (such as arbitrary pickle `.pkl` files or unsafe Keras lambdas) can execute malicious shell commands.
- **Strict Architecture Instantiation**: We prioritize declarative model definitions (`ModelFactory`) and load weights strictly via verified weight files (`.h5`, `.weights`) rather than executing arbitrary pickled objects.
- **Cryptographic Hash Verification**: All production weights (`plant.h5`) must match their recorded SHA-256 signatures in `data/manifests/dataset_manifest.json`.

### 2.2 Data Poisoning & Pharmacological Integrity
- **Adulterant Injection Defense**: In clinical pharmacognosy, misclassifying a toxic species (such as *Atropa belladonna* or *Aconitum ferox*) as a safe therapeutic herb can lead to severe poisoning.
- **Rigorous Catalog Auditing**: Any modification to `data/raw/clinical/`, `data/processed/`, or `knowledge/` requires independent botanical review and cannot be merged without verification against accepted pharmacopeia.
- **Manifest Integrity**: Automated CI/CD pipelines verify dataset checksums to detect unauthorized modifications.

### 2.3 Geospatial Privacy & Biodiversity OPSEC
- **Anti-Poaching Protection**: High-altitude alpine species like *Gentiana kurroo*, *Saussurea costus*, and *Picrorhiza kurroa* are critically endangered and subject to illegal bioprospecting.
- **Location Masking**: Precision GPS coordinates collected during wild field surveys in Kashmir must be truncated or obfuscated before publication to prevent unauthorized commercial exploitation of natural habitats.

### 2.4 Web Application & Upload Security
- **File Upload Sanitization**: All user-submitted leaf images uploaded via `/upload` or `/platform/identify` undergo strict validation:
  - Extension whitelist restricted to `.jpg`, `.jpeg`, `.png`, and `.webp`.
  - Binary magic byte validation using Pillow/OpenCV to verify authentic image streams.
  - Strict upload payload limits ($< 16\text{ MB}$) to prevent denial-of-service memory exhaustion.
  - Secure filename scrubbing via `werkzeug.utils.secure_filename`.

---

## 3. Reporting a Vulnerability

We appreciate the responsible security community and take all vulnerability reports seriously.

If you identify a security issue, vulnerability, or potential exploit:

1. **Do NOT open a public GitHub issue.** Public disclosure exposes researchers and users to zero-day exploitation before a patch can be developed.
2. **Submit a Private Vulnerability Report**:
   - Email: **`darrehanrasool@gmail.com`**
   - Subject: `[SECURITY] Herbalist-AI Vulnerability Report - <Brief Description>`
3. **Include Relevant Technical Details**:
   - Clear description of the vulnerability and potential impact.
   - Minimal proof-of-concept (PoC) code or step-by-step reproduction instructions.
   - Affected component, route, or model architecture.

### Coordinated Disclosure Timeline
- **Initial Acknowledgment**: Within **48 hours** of report receipt.
- **Triaging & Verification**: Within **5 business days**, detailing vulnerability scope and planned remediation.
- **Security Patch Release**: An expedited patch will be released, followed by public attribution in the release notes (if desired by the reporter).

---

## 4. Academic Institution Affiliation

- **Institutional Oversight**: Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India.
- **Ethics & Security Contact**: Department Maintainers via `darrehanrasool@gmail.com`.
