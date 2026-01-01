"""Image cropping utilities for export.

This module provides functions for auto-cropping images to content
with consistent margins, including support for animation frames.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PIL import Image as PILImage

__all__ = [
    "auto_crop",
    "auto_crop_frames",
    "get_content_bbox",
]


def get_content_bbox(
    img: PILImage.Image,
    background_color: str,
) -> tuple[int, int, int, int] | None:
    """Get bounding box of non-background content in image.

    Args:
        img: PIL Image to analyze.
        background_color: Background color to detect (hex string).

    Returns:
        Bounding box tuple (x1, y1, x2, y2) or None if image is entirely background.
    """
    from PIL import Image, ImageChops

    bg = Image.new("RGB", img.size, background_color)
    diff = ImageChops.difference(img.convert("RGB"), bg)
    return diff.getbbox()


def auto_crop(
    img: PILImage.Image,
    background_color: str,
    margin: int = 20,
) -> PILImage.Image:
    """Auto-crop image to content with margin.

    Finds the bounding box of non-background pixels and crops with a margin.

    Note: This function is for static images only. For animations, use
    auto_crop_frames to crop all frames to a common bounding box.

    Args:
        img: PIL Image to crop.
        background_color: Background color to detect (hex string).
        margin: Margin in pixels around content. Defaults to 20.

    Returns:
        Cropped PIL Image.
    """
    bbox = get_content_bbox(img, background_color)

    if bbox is None:
        return img

    x1, y1, x2, y2 = bbox
    x1 = max(0, x1 - margin)
    y1 = max(0, y1 - margin)
    x2 = min(img.width, x2 + margin)
    y2 = min(img.height, y2 + margin)

    return img.crop((x1, y1, x2, y2))


def auto_crop_frames(
    frames: list[PILImage.Image],
    background_color: str,
    margin: int = 20,
) -> list[PILImage.Image]:
    """Auto-crop multiple frames to a common bounding box.

    Calculates the union of all content bounding boxes across frames,
    then crops all frames to that same area. This prevents "jumping"
    in animations.

    Args:
        frames: List of PIL Images to crop.
        background_color: Background color to detect (hex string).
        margin: Margin in pixels around content. Defaults to 20.

    Returns:
        List of cropped PIL Images, all with identical dimensions.
    """
    if not frames:
        return frames

    # Calculate union of all bounding boxes
    union_bbox: tuple[int, int, int, int] | None = None

    for frame in frames:
        bbox = get_content_bbox(frame, background_color)
        if bbox is None:
            continue

        if union_bbox is None:
            union_bbox = bbox
        else:
            # Expand union to include this bbox
            union_bbox = (
                min(union_bbox[0], bbox[0]),
                min(union_bbox[1], bbox[1]),
                max(union_bbox[2], bbox[2]),
                max(union_bbox[3], bbox[3]),
            )

    if union_bbox is None:
        # All frames are entirely background
        return frames

    # Apply margin to union bbox
    x1, y1, x2, y2 = union_bbox
    x1 = max(0, x1 - margin)
    y1 = max(0, y1 - margin)
    x2 = min(frames[0].width, x2 + margin)
    y2 = min(frames[0].height, y2 + margin)

    # Crop all frames to the same bbox
    return [frame.crop((x1, y1, x2, y2)) for frame in frames]
