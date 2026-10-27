# Kashmir Endemic Medicinal Flora Dataset (Future Work)

This directory is dedicated exclusively to the upcoming high-altitude Kashmir medicinal flora dataset.

### Folder Structure:
- `train/<species_name>/*.jpg` — Training photos collected across Kashmir alpine zones.
- `val/<species_name>/*.jpg` — Validation photos for hyperparameter tuning.
- `test/<species_name>/*.jpg` — Independent holdout test set for generalization evaluation.

### Planned Kashmir Taxa (16 Species):
1. *Crocus sativus* (Kashmir Saffron / Kong)
2. *Aconitum heterophyllum* (Atis / Patrees)
3. *Gentiana kurroo* (Nilkanth / Gulu)
4. *Picrorhiza kurroa* (Kutki / Kour)
5. *Saussurea costus* (Kuth)
6. *Podophyllum hexandrum* (Bankakri)
7. *Fritillaria roylei* (Kakoli / Sheethkhar)
8. *Rheum emodi* (Pambchalan)
9. *Taxus wallichiana* (Himalayan Yew / Posthal)
10. *Artemisia absinthium* (Tethwan)
11. *Berberis lycium* (Kawdakh)
12. *Colchicum luteum* (Virkum)
13. *Datura stramonium* (Dhatur)
14. *Hyoscyamus niger* (Bazarbhang)
15. *Jurinea dolomiaea* (Dhoop)
16. *Valeriana jatamansi* (Mushkbala)

### Training Workflow:
Once images are organized in `train/` and `val/`, execute:
```bash
python scripts/train_kashmir_model.py
```
This automatically compiles the Kashmir model and saves weights to `models/kashmir/kashmir_plant.h5`.
