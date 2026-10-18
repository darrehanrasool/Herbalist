"""Train from scratch (MTech)

BTech reproduction (frozen Xception, 180px, 6 epochs):

    python training/src/train.py --arch xception --freeze-backbone --epochs 6 --batch-size 16

Need VNPlant-200 class folders in data/splits/train and data/splits/validation.

Other algorithms (same data API):

    python training/src/train.py --arch efficientnetv2b0 --epochs 12 --augment
    python training/src/train.py --arch resnet50 --epochs 12 --augment
    python training/src/train.py --arch mobilenetv3 --epochs 12 --augment
    python training/src/train.py --arch vgg16 --freeze-backbone --epochs 8

Evaluate:

    python training/src/evaluate.py --model artifacts/checkpoints/<file>.h5 --data-dir data/splits/test

Graphs for the website:

    python training/scripts/generate_lab_graphs.py
"""
