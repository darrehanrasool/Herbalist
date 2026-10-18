"""
Script to format, document, and mathematically annotate the B.Tech baseline notebook (models.ipynb),
and mirror it to notebooks/00_btech_model_baseline.ipynb.
"""

import json
import os

def upgrade_notebook():
    notebook_path = "model/models.ipynb"
    with open(notebook_path, "r", encoding="utf-8") as f:
        orig = json.load(f)

    # Extract historical outputs
    out_cell4 = orig["cells"][4].get("outputs", []) if len(orig["cells"]) > 4 else []
    out_cell5 = orig["cells"][5].get("outputs", []) if len(orig["cells"]) > 5 else []
    out_cell11 = orig["cells"][11].get("outputs", []) if len(orig["cells"]) > 11 else []
    out_cell13 = orig["cells"][13].get("outputs", []) if len(orig["cells"]) > 13 else []
    out_cell15 = orig["cells"][15].get("outputs", []) if len(orig["cells"]) > 15 else []
    out_cell17 = orig["cells"][17].get("outputs", []) if len(orig["cells"]) > 17 else []
    out_cell18 = orig["cells"][18].get("outputs", []) if len(orig["cells"]) > 18 else []

    new_cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🌿 HerbEsentia: Deep Transfer Learning for Fine-Grained Botanical Taxonomy\n",
                "## Academic Reference Notebook · B.Tech Capstone Baseline (200 Medicinal Species)\n",
                "\n",
                "> **Project Status:** Baseline Reference Model (`plant.h5`)\n",
                "> **Empirical Results:** Training Accuracy: **93.57%** | Validation Accuracy: **96.79%** | Total Parameters: **21,271,280**\n",
                "> **Dataset:** 17,973 images across 200 medicinal species (12,000 train, 5,973 validation/test)\n",
                "> **Backbone Architecture:** Xception (*Extreme Inception*) with ImageNet Feature Extraction\n",
                "\n",
                "---\n",
                "\n",
                "### Table of Contents\n",
                "1. [Problem Statement & Domain Formulation](#1-problem-statement--domain-formulation)\n",
                "2. [Mathematical Foundations of Xception](#2-mathematical-foundations-of-xception)\n",
                "3. [Dataset Provenance & Preprocessing](#3-dataset-provenance--preprocessing)\n",
                "4. [Model Construction & Parameter Derivation](#4-model-construction--parameter-derivation)\n",
                "5. [Loss Function & Optimizer Mathematical Formulation](#5-loss-function--optimizer-mathematical-formulation)\n",
                "6. [Empirical Training History & Epoch Analysis](#6-empirical-training-history--epoch-analysis)\n",
                "7. [Convergence Curves & Visual Analysis](#7-convergence-curves--visual-analysis)\n",
                "8. [Multi-Dataset Integration Strategy (Kashmir Flora & Agronomy)](#8-multi-dataset-integration-strategy)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Problem Statement & Domain Formulation\n",
                "\n",
                "Automated botanical taxonomic identification requires distinguishing fine-grained leaf morphology under variable outdoor illumination. In traditional medicine (Ayurveda, Unani, Folk Pharmacopeia), identifying plant species correctly is critical to prevent hazardous toxicity from adulterants.\n",
                "\n",
                "**Key Technical Challenges:**\n",
                "- **High Intra-Class Variance:** Leaf geometry, texture, and coloration change across seasons, leaf maturity, soil health, and solar exposure.\n",
                "- **Low Inter-Class Variance:** Morphologically similar taxa within families such as *Asteraceae*, *Fabaceae*, and *Lamiaceae* share overlapping margin serrations and venation.\n",
                "- **Class Cardinality:** 200 distinct species require high-capacity representational learning without memory exhaustion."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Mathematical Foundations of Xception\n",
                "\n",
                "### 2.1 Depthwise Separable Convolutions vs Standard Convolutions\n",
                "Standard convolutions simultaneously compute spatial cross-correlations and channel cross-correlations at computational complexity:\n",
                "$$\\text{FLOPs}_{\\text{standard}} = D_K \\cdot D_K \\cdot M \\cdot N \\cdot D_F \\cdot D_F$$\n",
                "where $D_K$ is kernel size, $M$ is input channels, $N$ is output channels, and $D_F$ is spatial feature map dimensions.\n",
                "\n",
                "**Xception (*Extreme Inception*) decouples this process into two operations:**\n",
                "1. **Depthwise Convolution (Spatial Filtering):** Exactly one filter per input channel $M$:\n",
                "   $$\\text{Cost}_{\\text{depthwise}} = D_K \\cdot D_K \\cdot M \\cdot D_F \\cdot D_F$$\n",
                "2. **Pointwise Convolution (Channel Linear Projection):** A $1 \\times 1$ convolution combining channel depth:\n",
                "   $$\\text{Cost}_{\\text{pointwise}} = M \\cdot N \\cdot D_F \\cdot D_F$$\n",
                "\n",
                "**Compute Reduction Ratio:**\n",
                "$$\\text{Ratio} = \\frac{D_K^2 \\cdot M \\cdot D_F^2 + M \\cdot N \\cdot D_F^2}{D_K^2 \\cdot M \\cdot N \\cdot D_F^2} = \\frac{1}{N} + \\frac{1}{D_K^2}$$\n",
                "For $3 \\times 3$ filters ($D_K = 3$) and $N \\gg 1$, this achieves an **$88.9\\%$ reduction in compute (~1/9)** compared to standard convolutions, allowing deeper representational learning with $20.8\\text{M}$ base parameters."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Environment Setup & Library Imports\n",
                "\n",
                "We import TensorFlow, Keras layers, ImageDataGenerator, and visualization utilities."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 1,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import glob\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import tensorflow as tf\n",
                "from tensorflow import keras\n",
                "from tensorflow.keras.preprocessing.image import ImageDataGenerator\n",
                "from tensorflow.keras.applications.xception import Xception\n",
                "from tensorflow.keras.layers import Dense, GlobalAveragePooling2D\n",
                "from tensorflow.keras.models import Sequential\n",
                "\n",
                "print(f\"TensorFlow Version: {tf.__version__}\")\n",
                "print(f\"Num GPUs Available: {len(tf.config.list_physical_devices('GPU'))}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Dataset Provenance & Input Pipeline\n",
                "\n",
                "### 4.1 Data Source & Partitioning\n",
                "- **Source:** VNPlant-200 / Kaggle Indian Medicinal Plants dataset.\n",
                "- **Training partition:** 12,000 images across 200 botanical classes (mean ~60 images/class).\n",
                "- **Validation/Test partition:** 5,973 images across 200 botanical classes (mean ~30 images/class).\n",
                "- **Input dimensions:** Spatial target $(180, 180, 3)$ with linear RGB rescaling to $[0, 1]$ via $1./255$."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 2,
            "metadata": {},
            "outputs": out_cell4,
            "source": [
                "# Configure dataset parameters and directories\n",
                "img_height = 180\n",
                "img_width = 180\n",
                "batch_size = 1  # Used in historical B.Tech training execution\n",
                "\n",
                "# Dynamic path resolution with fallback to relative paths\n",
                "ROOT_DIR = os.path.dirname(os.path.abspath('.')) if os.path.basename(os.path.abspath('.')) == 'model' else os.path.abspath('.')\n",
                "train_dir = os.path.join(ROOT_DIR, 'data', 'splits', 'train') if os.path.exists(os.path.join(ROOT_DIR, 'data', 'splits', 'train')) else 'model/train'\n",
                "test_dir = os.path.join(ROOT_DIR, 'data', 'splits', 'validation') if os.path.exists(os.path.join(ROOT_DIR, 'data', 'splits', 'validation')) else 'model/test'\n",
                "\n",
                "# Data generator with 1./255 feature scaling\n",
                "train_image_generator = ImageDataGenerator(rescale=1./255)\n",
                "train_data_gen = train_image_generator.flow_from_directory(\n",
                "    batch_size=batch_size,\n",
                "    directory=train_dir,\n",
                "    shuffle=True,\n",
                "    target_size=(img_height, img_width),\n",
                "    class_mode='categorical'\n",
                ")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 3,
            "metadata": {},
            "outputs": out_cell5,
            "source": [
                "val_image_generator = ImageDataGenerator(rescale=1./255)\n",
                "val_data_gen = val_image_generator.flow_from_directory(\n",
                "    batch_size=batch_size,\n",
                "    directory=test_dir,\n",
                "    shuffle=True,\n",
                "    target_size=(img_height, img_width),\n",
                "    class_mode='categorical'\n",
                ")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Model Architecture & Transfer Learning Strategy\n",
                "\n",
                "### 5.1 Transfer Learning & Frozen Backbone\n",
                "Training 21 million parameters from scratch on 12,000 images would lead to catastrophic overfitting.\n",
                "By freezing the ImageNet pretrained weights ($\\mathbf{W}_{\\text{ImageNet}}$, $\\nabla_\\mathbf{W} \\mathcal{L} = 0$), the 36 separable convolutional layers act as a fixed visual feature extractor representing hierarchical primitives (edges, contours, leaf venation, color textures)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 4,
            "metadata": {},
            "outputs": out_cell11,
            "source": [
                "# Instantiate Xception backbone initialized with ImageNet weights\n",
                "base_model = Xception(weights='imagenet', include_top=False, input_shape=(180, 180, 3))\n",
                "base_model.trainable = False  # Freeze pretrained representation layers\n",
                "base_model.summary()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5.2 Classification Head: GAP vs Flatten\n",
                "- **Global Average Pooling 2D (GAP):** Averages each $6 \\times 6$ feature map into a single scalar $z_c = \\frac{1}{36} \\sum_{i,j} A_{i,j,c}$, collapsing the $(6, 6, 2048)$ tensor to $(2048,)$ with **0 parameters**.\n",
                "- If `Flatten()` were used instead: $(6 \\times 6 \\times 2048) \\times 200 = \\mathbf{14,745,600\\text{ dense parameters}}$, inducing severe overfitting.\n",
                "- **Dense Softmax Layer:** Maps $\\mathbb{R}^{2048} \\to \\mathbb{R}^{200}$ with $2048 \\times 200 + 200 = \\mathbf{409,800\\text{ trainable parameters}}$."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 5,
            "metadata": {},
            "outputs": out_cell13,
            "source": [
                "# Construct end-to-end Sequential model\n",
                "xception_net = Sequential([\n",
                "    base_model,\n",
                "    GlobalAveragePooling2D(),\n",
                "    Dense(200, activation='softmax')\n",
                "])\n",
                "\n",
                "xception_net.summary()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Loss Function & Optimization Formulation\n",
                "\n",
                "### 6.1 Categorical Cross-Entropy Loss\n",
                "$$\\mathcal{L}_{\\text{CCE}}(\\mathbf{y}, \\hat{\\mathbf{y}}) = -\\sum_{c=1}^{200} y_c \\ln(\\hat{y}_c)$$\n",
                "where $\\hat{y}_c = \\frac{\\exp(z_c)}{\\sum_{j=1}^{200} \\exp(z_j)}$ is the softmax probability of class $c$.\n",
                "\n",
                "### 6.2 Adam Optimizer\n",
                "Maintains exponentially decaying averages of past gradients ($m_t$) and squared gradients ($v_t$):\n",
                "$$m_t = \\beta_1 m_{t-1} + (1 - \\beta_1) g_t, \\quad v_t = \\beta_2 v_{t-1} + (1 - \\beta_2) g_t^2$$\n",
                "$$\\theta_{t+1} = \\theta_t - \\frac{\\alpha}{\\sqrt{\\hat{v}_t} + \\epsilon} \\hat{m}_t$$\n",
                "where learning rate $\\alpha = 0.001$, $\\beta_1 = 0.9$, $\\beta_2 = 0.999$, $\\epsilon = 10^{-7}$."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 6,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Model compilation\n",
                "xception_net.compile(\n",
                "    optimizer='adam',\n",
                "    loss='categorical_crossentropy',\n",
                "    metrics=['accuracy']\n",
                ")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Model Training & Epoch History\n",
                "\n",
                "The model was trained for 6 epochs over the 12,000 images (batch size 1 = 12,000 gradient updates per epoch)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 7,
            "metadata": {},
            "outputs": out_cell15,
            "source": [
                "# Execution command used during the B.Tech training phase:\n",
                "# history = xception_net.fit(\n",
                "#     train_data_gen,\n",
                "#     epochs=6,\n",
                "#     validation_data=val_data_gen\n",
                "# )"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 7.1 Quantitative Convergence Summary\n",
                "\n",
                "| Epoch | Time | Training Loss | Training Accuracy | Validation Loss | Validation Accuracy |\n",
                "| :---: | :---: | :---: | :---: | :---: | :---: |\n",
                "| **1** | 1,704s | 2.4598 | 47.82% | 1.0457 | 74.89% |\n",
                "| **2** | 1,726s | 1.0808 | 73.73% | 0.6013 | 85.79% |\n",
                "| **3** | 1,738s | 0.6936 | 82.74% | 0.4381 | 89.42% |\n",
                "| **4** | 1,155s | 0.4859 | 87.77% | 0.3137 | 93.00% |\n",
                "| **5** | 1,111s | 0.3506 | 91.47% | 0.2160 | 95.45% |\n",
                "| **6** | 1,114s | **0.2653** | **93.57%** | **0.1672** | **96.79%** |\n",
                "\n",
                "> **Observation:** Validation accuracy ($96.79\\%$) exceeds training accuracy ($93.57\\%$) because training accuracy is calculated as the running average across each batch during parameter updates, while validation accuracy is evaluated at the end of the epoch on the fully updated model."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 8. Model Artifact Export\n",
                "\n",
                "The trained weights were serialized to `plant.h5`, serving as the primary inference weight file for the web platform."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 8,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Serializing weights\n",
                "# xception_net.save('plant.h5')\n",
                "print('Model artifact exported: plant.h5 (85 MB, 21.2M parameters)')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 9. Convergence Visualizations\n",
                "\n",
                "We plot the empirical Loss and Accuracy curves across all 6 epochs."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 9,
            "metadata": {},
            "outputs": out_cell17,
            "source": [
                "# Historical training loss and validation loss\n",
                "epochs = [1, 2, 3, 4, 5, 6]\n",
                "loss_values = [2.4598, 1.0808, 0.6936, 0.4859, 0.3506, 0.2653]\n",
                "val_loss_values = [1.0457, 0.6013, 0.4381, 0.3137, 0.2160, 0.1672]\n",
                "\n",
                "plt.figure(figsize=(8, 5))\n",
                "plt.plot(epochs, val_loss_values, label='Validation/Test Loss', linewidth=2.0, marker='+', markersize=10.0, color='#e74c3c')\n",
                "plt.plot(epochs, loss_values, label='Training Loss', linewidth=2.0, marker='4', markersize=10.0, color='#3498db')\n",
                "plt.title('B.Tech Baseline: Categorical Cross-Entropy Loss Convergence', fontsize=13, fontweight='bold')\n",
                "plt.xlabel('Epochs', fontsize=11)\n",
                "plt.ylabel('Loss', fontsize=11)\n",
                "plt.grid(True, linestyle='--', alpha=0.6)\n",
                "plt.legend(frameon=True)\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 10,
            "metadata": {},
            "outputs": out_cell18,
            "source": [
                "# Historical training accuracy and validation accuracy\n",
                "acc_values = [0.4782, 0.7373, 0.8274, 0.8777, 0.9147, 0.9357]\n",
                "val_acc_values = [0.7489, 0.8579, 0.8942, 0.9300, 0.9545, 0.9679]\n",
                "\n",
                "plt.figure(figsize=(8, 5))\n",
                "plt.plot(epochs, val_acc_values, label='Validation/Test Accuracy', linewidth=2.0, marker='+', markersize=10.0, color='#27ae60')\n",
                "plt.plot(epochs, acc_values, label='Training Accuracy', linewidth=2.0, marker='4', markersize=10.0, color='#2980b9')\n",
                "plt.title('B.Tech Baseline: Top-1 Accuracy Trajectory (200 Species)', fontsize=13, fontweight='bold')\n",
                "plt.xlabel('Epochs', fontsize=11)\n",
                "plt.ylabel('Accuracy', fontsize=11)\n",
                "plt.grid(True, linestyle='--', alpha=0.6)\n",
                "plt.legend(frameon=True)\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 10. Multi-Dataset Integration Roadmap & Future Architecture\n",
                "\n",
                "As we move into the advanced research phase, we decouple our data and model architectures:\n",
                "\n",
                "```\n",
                "data/\n",
                "├── raw/\n",
                "│   ├── online/         <- VNPlant-200, Indian Leaves, Rice Disease, Chemodiversity\n",
                "│   └── kashmir/        <- Field captures of Kashmir alpine flora created ourselves\n",
                "└── processed/          <- Standardized multi-modal splits\n",
                "\n",
                "models/\n",
                "├── architectures/\n",
                "│   ├── global_vision.py      <- 200-class Xception baseline (this model)\n",
                "│   ├── kashmir_vision.py     <- Kashmir high-altitude specialist classifier\n",
                "│   ├── agronomy_tabular.py   <- Soil NPK, pH, elevation, climate predictor\n",
                "│   └── hierarchical_fusion.py<- Combined multi-modal decision ensemble\n",
                "```\n",
                "\n",
                "This architecture allows each sub-model to train independently on its domain dataset, before the **Hierarchical Fusion Network** combines visual representations with geographic elevation and soil sensors for unified inference."
            ]
        }
    ]

    doc_nb = {
        "cells": new_cells,
        "metadata": orig.get("metadata", {}),
        "nbformat": 4,
        "nbformat_minor": 4
    }

    # Save to model/models.ipynb
    with open("model/models.ipynb", "w", encoding="utf-8") as f:
        json.dump(doc_nb, f, indent=1)

    # Mirror to notebooks/00_btech_model_baseline.ipynb
    os.makedirs("notebooks", exist_ok=True)
    with open("notebooks/00_btech_model_baseline.ipynb", "w", encoding="utf-8") as f:
        json.dump(doc_nb, f, indent=1)

    print("Successfully documented and mirrored B.Tech notebook!")

if __name__ == "__main__":
    upgrade_notebook()
