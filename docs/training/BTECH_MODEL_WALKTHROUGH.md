# How the BTech Herbalist model was trained

Use this note when you explain the project to your professor. It is taken from `model/models.ipynb`, `Accuracy.txt`, `api/app.py`, and the VNPlant-200 paper — not from memory.

## One-sentence summary

A **frozen ImageNet Xception CNN** classified **200 Vietnamese medicinal plant species** from **180×180 RGB photos**, then the predicted **scientific name** was joined to **`medicinal.csv`** to show uses, compounds, and toxicity. The network did **not** learn chemistry or soil.

## Dataset

| Item                             | Value                                              |
| -------------------------------- | -------------------------------------------------- |
| Public name                      | **VNPlant-200** (Nguyen Quoc & Truong Hoang, 2020) |
| Classes                          | 200 species                                        |
| Notebook counts                  | **12,000** train images, **5,973** test images     |
| Typical split in the source repo | 60 images/class train, 40/class test               |
| Image sizes in the paper         | 256×256 and 512×512 releases                       |
| What you fed the net             | Resized to **180×180**, pixels `/ 255.0`           |

The class list in `api/app.py` (`PLANT_CLASSES`) matches VNPlant-200 names (including noisy labels such as `Clycyrrhiza uralensis fish`, `Lpomoea sp`).

`Kashmere.csv` is a **separate Himalayan catalog**. Those species were **not** training classes.

## Pipeline (step by step)

1. Folder dataset: `train_dir` / `test_dir` on a Windows path in the notebook (`C:/Users/sheikhmudhat/...`). That means the notebook you kept is a working copy; original local paths are gone.
2. `ImageDataGenerator(rescale=1./255)` — **rescale only**. The notebook you saved does **not** actually apply rotation/flip in the generator cells that ran.
3. `flow_from_directory`, `class_mode='categorical'`, `target_size=(180, 180)`.
4. `batch_size = 1` in the saved notebook (very slow; unusual for Xception).
5. Base model: `Xception(weights='imagenet', include_top=False, input_shape=(180,180,3))`.
6. `base_model.trainable = False` — **transfer learning, backbone frozen**.
7. Head: `GlobalAveragePooling2D()` → `Dense(200, softmax)`.
8. Loss: **categorical cross-entropy**. Optimizer: **Adam** (Keras default learning rate 0.001 unless changed — notebook does not set a custom LR).
9. Metric: **accuracy** (AUC is registered at load time in Flask as `auc_roc`, but the compile line in the notebook is accuracy).
10. `fit` for **6 epochs**.
11. Saved as `plant.h5`.
12. Flask loads an image, `argmax` on softmax, maps index → scientific name, filters `medicinal.csv`.

## Reported numbers (`Accuracy.txt`)

- Algorithm: Xception (file says “Exception” — typo).
- Training accuracy: **93.34%**
- Validation accuracy: **96.79%**

Validation higher than training is possible with a frozen backbone + a similar test split, but it is **not** field accuracy on Kashmir farm photos. Say that clearly.

## Algorithms involved (what to name in a viva)

| Algorithm / idea                            | Role                                                     |
| ------------------------------------------- | -------------------------------------------------------- |
| Convolutional neural network                | Learns leaf/plant appearance                             |
| Depthwise separable convolutions (Xception) | Cheaper spatial + channel filtering than a plain ConvNet |
| Transfer learning                           | ImageNet features reused                                 |
| Frozen feature extractor                    | Only the 200-way head was trained                        |
| Softmax                                     | Class probabilities                                      |
| Categorical cross-entropy                   | Training loss                                            |
| Adam                                        | Adaptive gradient optimizer                              |
| Global average pooling                      | Vectorizes the 6×6×2048 map without a huge Dense flatten |
| Argmax                                      | Chosen species at inference                              |
| Tabular lookup                              | Medicinal text is **not** predicted                      |

The original VNPlant-200 paper used **SIFT/SURF + Random Forest**, not Xception. Your BTech contribution is **deep transfer learning on that dataset** plus a Flask report UI.

## What the website computed vs what it displayed

- Computed from pixels: class index, confidence.
- Displayed from CSV: medicinal value, active compounds, toxicity, geography, parts used, preparation, conservation.

That distinction is the most important sentence in your MTech upgrade story.

## Files

- Training notebook: `model/models.ipynb`
- Weights: `plant.h5` (also `api/plant.h5`)
- Serving: `api/app.py` → `predict_plant()`
- Knowledge: `medicinal.csv`
- Reproduction scripts (new): `training/src/train.py` with `--arch xception --freeze-backbone`
