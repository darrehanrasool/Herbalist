"""Directory data loaders matching the BTech ImageDataGenerator pipeline."""
from __future__ import annotations

from tensorflow.keras.preprocessing.image import ImageDataGenerator


def make_generators(train_dir, val_dir, img_size=180, batch_size=16, augment=False):
    train_kwargs = {"rescale": 1.0 / 255}
    if augment:
        train_kwargs.update(
            rotation_range=25,
            width_shift_range=0.1,
            height_shift_range=0.1,
            zoom_range=0.15,
            horizontal_flip=True,
            fill_mode="nearest",
        )
    train_gen = ImageDataGenerator(**train_kwargs)
    val_gen = ImageDataGenerator(rescale=1.0 / 255)
    train = train_gen.flow_from_directory(
        train_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode="categorical",
        shuffle=True,
    )
    val = val_gen.flow_from_directory(
        val_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode="categorical",
        shuffle=False,
    )
    return train, val
