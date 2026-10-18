"""Generate clean, valid Jupyter notebooks for the research pipeline."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT / "notebooks"
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)


def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.15"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }


def md_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    }


def code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.strip().split("\n")]
    }


# Notebook 1: Data Exploration
nb1 = make_notebook([
    md_cell("# 01. Data Exploration & Botanical Taxonomy Analysis\nHerbalist AI Research Pipeline"),
    code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load processed catalogs
med_df = pd.read_csv('../data/processed/medicinal.csv')
kashmir_df = pd.read_csv('../data/processed/kashmir_medicinal.csv')
print(f"VNPlant-200 Catalog: {len(med_df)} taxa")
print(f"Kashmir Himalayan Catalog: {len(kashmir_df)} taxa")"""),
    code_cell("""# Inspect Kashmir endemic taxa
kashmir_df[['Scientificname', 'Biologicalname', 'Family', 'ConservationStatus', 'ToxicityLevel']]"""),
    code_cell("""# Distribution of families in 200 species benchmark
top_families = med_df['Family'].value_counts().head(10)
plt.figure(figsize=(10, 5))
top_families.plot(kind='bar', color='#1fb890')
plt.title('Top 10 Botanical Families in Benchmark')
plt.xlabel('Family')
plt.ylabel('Species Count')
plt.show()"""),
])

# Notebook 2: Data Quality
nb2 = make_notebook([
    md_cell("# 02. Data Quality & Schema Integrity\nHerbalist AI Research Pipeline"),
    code_cell("""import pandas as pd
from src.herbalist.data import compute_data_quality_report, load_manifest, verify_manifest_checksums

# Verify dataset manifest
manifest = load_manifest()
checksums = verify_manifest_checksums()
print("Dataset Manifest Checksums:", checksums)"""),
    code_cell("""# Compute quality report for master knowledge table
master_df = pd.read_csv('../knowledge/plants_master.csv')
report = compute_data_quality_report(master_df)
print(f"Total Rows: {report['total_rows']}")
print(f"Overall Completeness: {report['overall_completeness_pct']}%")
print("Missing percentages per column:")
for col, pct in report['missing_percentages'].items():
    print(f"  {col:<25}: {pct}%")"""),
])

# Notebook 3: Feature Analysis
nb3 = make_notebook([
    md_cell("# 03. Phytochemical & Agronomic Feature Analysis\nHerbalist AI Research Pipeline"),
    code_cell("""import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

soil_df = pd.read_csv('../knowledge/soil_requirements.csv')
soil_df.describe()"""),
    code_cell("""# Correlation analysis across soil parameters
from src.herbalist.visualization import plot_correlation_heatmap
plot_correlation_heatmap(soil_df, output_path=Path('../visualizations/data_exploration/soil_corr.png'))"""),
])

# Notebook 4: Model Comparison
nb4 = make_notebook([
    md_cell("# 04. Model Comparison & Baseline Verification\nHerbalist AI Research Pipeline"),
    code_cell("""import pandas as pd
from src.herbalist.models.deep_learning import load_trained_vision_model
from src.herbalist.research.baseline_reproduction import verify_btech_baseline

baseline = verify_btech_baseline()
print("Reported BTech Xception Baseline:")
for k, v in baseline.items():
    print(f"  {k}: {v}")"""),
    code_cell("""# Model architecture summary
model = load_trained_vision_model()
if model:
    print(f"Parameters: {model.count_params():,}")
    model.summary()"""),
])

notebooks = {
    "01_data_exploration.ipynb": nb1,
    "02_data_quality.ipynb": nb2,
    "03_feature_analysis.ipynb": nb3,
    "04_model_comparison.ipynb": nb4,
}

for name, content in notebooks.items():
    out_file = NOTEBOOKS_DIR / name
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
    print(f"✅ Generated notebook: {out_file.relative_to(ROOT)}")
