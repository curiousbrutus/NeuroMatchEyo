"""pure Python implementation of image filters"""
from __future__ import annotations

import numpy as np


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    # iterate through the pixels, and apply the grayscale transform
    height, width, channels = image.shape
    print(height, width, channels)

    gray_image = np.zeros((height, width,channels), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            r, g, b = image[y, x]

            gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)

            gray_image[y, x, 0] = gray_value
            gray_image[y, x, 1] = gray_value
            gray_image[y, x, 2] = gray_value
    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    # Iterate through the pixels
    # applying the sepia matrix

    ...

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image
