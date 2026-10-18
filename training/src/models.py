"""Model zoo for Herbalist AI. All heads are softmax over num_classes."""
from __future__ import annotations

from tensorflow.keras import layers, models
from tensorflow.keras.applications import (
    Xception,
    EfficientNetV2B0,
    ResNet50,
    MobileNetV3Small,
    VGG16,
)


def build_model(arch: str, img_size: int, num_classes: int, freeze_backbone: bool = True, dropout: float = 0.2):
    arch = arch.lower()
    shape = (img_size, img_size, 3)
    builders = {
        "xception": lambda: Xception(weights="imagenet", include_top=False, input_shape=shape),
        "efficientnetv2b0": lambda: EfficientNetV2B0(weights="imagenet", include_top=False, input_shape=shape),
        "resnet50": lambda: ResNet50(weights="imagenet", include_top=False, input_shape=shape),
        "mobilenetv3": lambda: MobileNetV3Small(weights="imagenet", include_top=False, input_shape=shape),
        "vgg16": lambda: VGG16(weights="imagenet", include_top=False, input_shape=shape),
    }
    if arch not in builders:
        raise ValueError(f"Unknown arch {arch}. Choose {list(builders)}")
    base = builders[arch]()
    base.trainable = not freeze_backbone
    x = layers.GlobalAveragePooling2D()(base.output)
    if dropout:
        x = layers.Dropout(dropout)(x)
    out = layers.Dense(num_classes, activation="softmax")(x)
    model = models.Model(base.input, out, name=f"herbalist_{arch}")
    return model
