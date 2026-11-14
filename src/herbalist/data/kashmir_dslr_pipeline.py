"""
kashmir_dslr_pipeline.py
-------------------------
Production-grade automated ingestion, EXIF telemetry extraction, quality-auditing,
and stratified train/val/test dataset splitting pipeline for Kashmir Himalayan
high-altitude DSLR and smartphone botanical field photography.

Capabilities:
  1. Multi-Format Image Ingestion:
     - Standard: .JPG, .JPEG, .PNG, .TIFF, .BMP
     - Camera RAW: .CR2, .CR3 (Canon), .NEF (Nikon), .ARW (Sony), .DNG (Adobe)
  2. Quality Auditing:
     - Laplacian Variance blur detection (threshold: sigma^2 < 100.0)
     - Exposure validation (highlight blowout > 250, underexposure < 15)
  3. EXIF & Altitude Extraction:
     - GPS Decimal Coordinates & Elevation (m.a.s.l.)
     - Kashmir altitudinal zone classification (Montane, Temperate, Sub-Alpine, Alpine Scree)
     - Camera hardware metadata (Make, Model, Lens, Focal Length, Aperture, ISO)
  4. Standardized Image Normalization:
     - Aspect-ratio preserving center crop
     - Standard model dimension resizing (180x180, 224x224, 512x512)
  5. Automated Stratified Splitting:
     - Per-species partition into Train (70%), Validation (15%), Test (15%)
     - Preserves balanced representation across rare high-altitude endemics
  6. Manifest & Audit Logging:
     - Writes `data/manifests/kashmir_dslr_split_manifest.json`
     - Updates `data/csv/kashmir_dslr_splits.csv`

Authors:
  - Dar Rehan Rasool (Project Lead & Author, M.Tech AI, CAI, IUST)
Faculty Supervisor & HOD:
  - Dr. Javad Ahmad & Dr. Riyaz (Faculty Supervisors, CAI, IUST)
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import random
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import ExifTags, Image, ImageOps

from src.herbalist.core.constants import ROOT_DIR

# Supported image file extensions
STANDARD_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
CAMERA_RAW_EXTENSIONS = {".cr2", ".cr3", ".nef", ".arw", ".dng", ".raf", ".orf", ".rw2"}
ALL_IMAGE_EXTENSIONS = STANDARD_EXTENSIONS.union(CAMERA_RAW_EXTENSIONS)


@dataclass
class ImageQualityAudit:
    is_valid: bool
    blur_score: float
    is_blurry: bool
    mean_luminance: float
    exposure_status: str
    width: int
    height: int
    rejection_reason: Optional[str] = None


@dataclass
class ExifTelemetry:
    camera_make: str = "Unknown"
    camera_model: str = "Unknown"
    date_captured: str = ""
    focal_length_mm: Optional[float] = None
    aperture_f_stop: Optional[float] = None
    iso_speed: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude_m: Optional[float] = None
    ecological_zone: str = "Colline / Montane"


@dataclass
class ProcessedImageRecord:
    image_id: str
    species_name: str
    original_path: str
    target_split: str
    processed_path: str
    file_format: str
    blur_score: float
    altitude_m: Optional[float]
    ecological_zone: str
    date_processed: str
    sha256_hash: str


class KashmirDSLRDatasetPipeline:
    """Automated preprocessor and stratified dataset builder for Kashmir field captures."""

    def __init__(
        self,
        raw_dir: Optional[Path] = None,
        processed_dir: Optional[Path] = None,
        manifest_dir: Optional[Path] = None,
        csv_dir: Optional[Path] = None,
        target_size: Tuple[int, int] = (180, 180),
        blur_threshold: float = 80.0,
        split_ratios: Tuple[float, float, float] = (0.70, 0.15, 0.15),
        seed: int = 42,
    ):
        self.raw_dir = raw_dir or (ROOT_DIR / "data" / "raw" / "kashmir")
        self.processed_dir = processed_dir or (ROOT_DIR / "data" / "processed")
        self.manifest_dir = manifest_dir or (ROOT_DIR / "data" / "manifests")
        self.csv_dir = csv_dir or (ROOT_DIR / "data" / "csv")
        self.target_size = target_size
        self.blur_threshold = blur_threshold
        self.split_ratios = split_ratios
        self.seed = seed

        # Ensure directory structures exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_dir.mkdir(parents=True, exist_ok=True)
        self.csv_dir.mkdir(parents=True, exist_ok=True)

        for split in ("train", "val", "test"):
            (self.processed_dir / split).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def detect_hardware_accelerator() -> Dict[str, str]:
        """Detect available hardware accelerator for parallel tensor processing."""
        hw = {"device": "CPU", "framework": "PyTorch / TensorFlow", "cores": str(os.cpu_count() or 4)}
        try:
            import torch  # type: ignore
            if torch.cuda.is_available():
                hw["device"] = f"NVIDIA CUDA ({torch.cuda.get_device_name(0)})"
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                hw["device"] = "Apple Silicon Metal (MPS)"
        except ImportError:
            try:
                import tensorflow as tf  # type: ignore
                gpus = tf.config.list_physical_devices("GPU")
                if gpus:
                    hw["device"] = f"GPU ({len(gpus)} device(s))"
            except ImportError:
                pass
        return hw

    def audit_quality(self, img: Image.Image) -> ImageQualityAudit:
        """Inspect image for optical sharpness (Laplacian variance) and exposure levels."""
        w, h = img.size
        if w < 50 or h < 50:
            return ImageQualityAudit(
                is_valid=False, blur_score=0.0, is_blurry=True,
                mean_luminance=0.0, exposure_status="Invalid Dimensions",
                width=w, height=h, rejection_reason="Dimensions too small (<50px)"
            )

        # Convert to grayscale numpy array for variance of Laplacian
        gray = np.array(img.convert("L"), dtype=np.float32)

        # Discrete 2D Laplacian convolution kernel
        kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
        # Fast 2D edge response using slices
        laplacian = (
            gray[:-2, 1:-1] + gray[2:, 1:-1] + gray[1:-1, :-2] + gray[1:-1, 2:] - 4.0 * gray[1:-1, 1:-1]
        )
        blur_score = float(np.var(laplacian))
        is_blurry = blur_score < self.blur_threshold

        # Luminance
        mean_lum = float(np.mean(gray))
        if mean_lum > 248.0:
            exp_status = "Overexposed (Highlights Blown)"
        elif mean_lum < 15.0:
            exp_status = "Underexposed (Deep Shadows)"
        else:
            exp_status = "Optimal Exposure"

        return ImageQualityAudit(
            is_valid=True,
            blur_score=round(blur_score, 2),
            is_blurry=is_blurry,
            mean_luminance=round(mean_lum, 2),
            exposure_status=exp_status,
            width=w,
            height=h,
        )

    @staticmethod
    def extract_exif(img: Image.Image) -> ExifTelemetry:
        """Extract camera hardware metadata and GPS coordinates from EXIF tags."""
        telemetry = ExifTelemetry()
        raw_exif = getattr(img, "_getexif", lambda: None)()
        if not raw_exif:
            return telemetry

        tag_map = {ExifTags.TAGS.get(k, k): v for k, v in raw_exif.items()}

        telemetry.camera_make = str(tag_map.get("Make", "Unknown")).strip()
        telemetry.camera_model = str(tag_map.get("Model", "Unknown")).strip()
        telemetry.date_captured = str(tag_map.get("DateTimeOriginal", tag_map.get("DateTime", "")))

        # Focal length and aperture
        focal = tag_map.get("FocalLength")
        if focal:
            try:
                telemetry.focal_length_mm = float(focal)
            except (ValueError, TypeError):
                pass

        f_num = tag_map.get("FNumber")
        if f_num:
            try:
                telemetry.aperture_f_stop = float(f_num)
            except (ValueError, TypeError):
                pass

        iso = tag_map.get("ISOSpeedRatings")
        if iso:
            try:
                telemetry.iso_speed = int(iso) if isinstance(iso, (int, float)) else int(iso[0])
            except (ValueError, TypeError, IndexError):
                pass

        # GPS Info
        gps_info = tag_map.get("GPSInfo")
        if gps_info:
            gps_tags = {ExifTags.GPSTAGS.get(k, k): v for k, v in gps_info.items()}
            lat = gps_tags.get("GPSLatitude")
            lat_ref = gps_tags.get("GPSLatitudeRef", "N")
            lon = gps_tags.get("GPSLongitude")
            lon_ref = gps_tags.get("GPSLongitudeRef", "E")
            alt = gps_tags.get("GPSAltitude")

            if lat and len(lat) == 3:
                try:
                    dec_lat = float(lat[0]) + float(lat[1]) / 60.0 + float(lat[2]) / 3600.0
                    if lat_ref == "S":
                        dec_lat = -dec_lat
                    telemetry.latitude = round(dec_lat, 6)
                except (ValueError, TypeError):
                    pass

            if lon and len(lon) == 3:
                try:
                    dec_lon = float(lon[0]) + float(lon[1]) / 60.0 + float(lon[2]) / 3600.0
                    if lon_ref == "W":
                        dec_lon = -dec_lon
                    telemetry.longitude = round(dec_lon, 6)
                except (ValueError, TypeError):
                    pass

            if alt:
                try:
                    telemetry.altitude_m = round(float(alt), 1)
                except (ValueError, TypeError):
                    pass

        # Classify altitudinal zone
        alt_m = telemetry.altitude_m or 2200.0
        if alt_m >= 3600.0:
            telemetry.ecological_zone = "Alpine Scree & Moraine (3600m - 4400m)"
        elif alt_m >= 2800.0:
            telemetry.ecological_zone = "Sub-Alpine Betula Ravines (2800m - 3600m)"
        elif alt_m >= 1800.0:
            telemetry.ecological_zone = "Temperate Mixed Coniferous (1800m - 2800m)"
        else:
            telemetry.ecological_zone = "Colline / Montane Valley Scrub (1400m - 1800m)"

        return telemetry

    def load_image(self, file_path: Path) -> Tuple[Optional[Image.Image], str]:
        """Safely load DSLR image, handling both standard formats and camera RAW."""
        ext = file_path.suffix.lower()

        # Handle Camera RAW (.CR2, .CR3, .NEF, .ARW, etc.)
        if ext in CAMERA_RAW_EXTENSIONS:
            try:
                import rawpy  # type: ignore
                with rawpy.imread(str(file_path)) as raw:
                    rgb = raw.postprocess(use_camera_wb=True, half_size=False)
                    img = Image.fromarray(rgb)
                    return img, "Camera RAW (Decoded)"
            except ImportError:
                # Fallback to PIL if rawpy not installed
                try:
                    img = Image.open(file_path)
                    return img.convert("RGB"), "RAW (PIL Native)"
                except Exception as e:
                    return None, f"Camera RAW decode requires 'rawpy' package: {e}"
            except Exception as e:
                return None, f"RAW decode error: {e}"

        # Handle Standard formats
        try:
            img = Image.open(file_path)
            # Correct orientation from EXIF orientation tag
            img = ImageOps.exif_transpose(img)
            return img.convert("RGB"), "Standard RGB"
        except Exception as e:
            return None, f"Image open failed: {e}"

    def preprocess_and_crop(self, img: Image.Image) -> Image.Image:
        """Center-crop image to 1:1 square ratio and resize to target dimension with anti-aliasing."""
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim

        cropped = img.crop((left, top, right, bottom))
        rescaled = cropped.resize(self.target_size, Image.Resampling.LANCZOS)
        return rescaled

    def run_pipeline(
        self,
        source_dir: Optional[Path] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Execute full ingestion, audit, normalization, and stratified splitting.

        Folder structure expected:
          data/raw/kashmir/<Species_Name>/image_001.JPG
        Or flat directory with auto-detected species tags.
        """
        src = source_dir or self.raw_dir
        random.seed(self.seed)

        print("\n" + "=" * 75)
        print("KASHMIR HIMALAYAN DSLR FIELD DATASET INGESTION & SPLITTING PIPELINE")
        print("Centre for Artificial Intelligence, IUST Kashmir")
        print("=" * 75)

        hw = self.detect_hardware_accelerator()
        print(f"  Accelerated Compute: {hw['device']} (Cores: {hw['cores']})")
        print(f"  Source Directory:    {src}")
        print(f"  Target Resolution:   {self.target_size[0]}×{self.target_size[1]} RGB")
        print(f"  Split Ratios:        Train {int(self.split_ratios[0]*100)}% / Val {int(self.split_ratios[1]*100)}% / Test {int(self.split_ratios[2]*100)}%")
        print("=" * 75)

        # Discover species folders or files
        species_dirs = [d for d in src.iterdir() if d.is_dir() and not d.name.startswith(".")]

        # If flat directory with no subdirectories, use default Kashmir endemic category
        if not species_dirs:
            species_dirs = [src]

        records: List[ProcessedImageRecord] = []
        species_summary: Dict[str, Dict[str, int]] = {}
        total_discovered = 0
        total_processed = 0
        total_blurry = 0
        total_rejected = 0

        for s_dir in species_dirs:
            species_name = s_dir.name.replace("_", " ") if s_dir != src else "Kashmir Alpine Taxa"
            species_summary[species_name] = {"train": 0, "val": 0, "test": 0, "rejected": 0}

            # Gather all image files
            img_files = [
                f for f in s_dir.glob("*")
                if f.is_file() and f.suffix.lower() in ALL_IMAGE_EXTENSIONS
            ]
            total_discovered += len(img_files)

            if not img_files:
                continue

            # Randomize order for stratified assignment
            random.shuffle(img_files)
            n_total = len(img_files)
            n_train = int(n_total * self.split_ratios[0])
            n_val = int(n_total * self.split_ratios[1])

            for idx, img_path in enumerate(img_files):
                img, load_status = self.load_image(img_path)
                if img is None:
                    total_rejected += 1
                    species_summary[species_name]["rejected"] += 1
                    print(f"  ⚠ Skipped {img_path.name}: {load_status}")
                    continue

                # Quality Audit
                audit = self.audit_quality(img)
                if not audit.is_valid:
                    total_rejected += 1
                    species_summary[species_name]["rejected"] += 1
                    continue

                if audit.is_blurry:
                    total_blurry += 1

                # EXIF extraction
                telemetry = self.extract_exif(img)

                # Assign split
                if idx < n_train:
                    split_name = "train"
                elif idx < n_train + n_val:
                    split_name = "val"
                else:
                    split_name = "test"

                # Preprocess & Save
                species_slug = species_name.replace(" ", "_")
                dest_dir = self.processed_dir / split_name / species_slug
                dest_dir.mkdir(parents=True, exist_ok=True)

                # Stable content hash for unique image ID
                hasher = hashlib.sha256()
                with open(img_path, "rb") as bf:
                    hasher.update(bf.read(65536))
                content_hash = hasher.hexdigest()[:12]
                out_filename = f"{species_slug}_{split_name}_{content_hash}.jpg"
                out_path = dest_dir / out_filename

                if not dry_run:
                    processed_img = self.preprocess_and_crop(img)
                    processed_img.save(out_path, "JPEG", quality=95)

                species_summary[species_name][split_name] += 1
                total_processed += 1

                records.append(
                    ProcessedImageRecord(
                        image_id=f"KASH-{content_hash.upper()}",
                        species_name=species_name,
                        original_path=str(img_path),
                        target_split=split_name,
                        processed_path=str(out_path),
                        file_format=img_path.suffix.upper(),
                        blur_score=audit.blur_score,
                        altitude_m=telemetry.altitude_m,
                        ecological_zone=telemetry.ecological_zone,
                        date_processed=datetime.utcnow().isoformat() + "Z",
                        sha256_hash=content_hash,
                    )
                )

        # Save Split Manifest JSON
        manifest_payload = {
            "pipeline_version": "2.0.0",
            "executed_at": datetime.utcnow().isoformat() + "Z",
            "institution": "Centre for Artificial Intelligence, IUST Kashmir",
            "hardware_platform": hw,
            "target_resolution": f"{self.target_size[0]}x{self.target_size[1]}",
            "statistics": {
                "total_discovered": total_discovered,
                "total_processed": total_processed,
                "total_blurry_flagged": total_blurry,
                "total_rejected": total_rejected,
            },
            "species_splits": species_summary,
        }

        manifest_file = self.manifest_dir / "kashmir_dslr_split_manifest.json"
        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest_payload, f, indent=2)

        # Save Splits CSV in data/csv/
        csv_file = self.csv_dir / "kashmir_dslr_splits.csv"
        if records:
            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(asdict(records[0]).keys()))
                writer.writeheader()
                for r in records:
                    writer.writerow(asdict(r))

        print(f"\n✓ Pipeline complete:")
        print(f"  • Images Discovered:  {total_discovered}")
        print(f"  • Images Processed:   {total_processed}")
        print(f"  • Blurry Images:      {total_blurry} (Logged, threshold={self.blur_threshold})")
        print(f"  • Rejected Images:    {total_rejected}")
        print(f"  • Manifest Saved:     {manifest_file}")
        print(f"  • Splits CSV Saved:   {csv_file}")
        print("=" * 75 + "\n")

        return manifest_payload


def run_kashmir_pipeline():
    pipeline = KashmirDSLRDatasetPipeline()
    return pipeline.run_pipeline()


if __name__ == "__main__":
    run_kashmir_pipeline()
