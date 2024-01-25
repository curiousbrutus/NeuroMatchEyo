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
    sepia_matrix = [
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ]
    # Pure python implementation
    sepia_image = np.empty_like(image)
    # Iterate through the pixels
    height, width, channels = image.shape

    for y in range(height):
        for x in range(width):
            r, g, b = image[y, x]

            sepia_r = int(r * sepia_matrix[0][0] + g * sepia_matrix[0][1] + b * sepia_matrix[0][2])
            sepia_g = int(r * sepia_matrix[1][0] + g * sepia_matrix[1][1] + b * sepia_matrix[1][2])
            sepia_b = int(r * sepia_matrix[2][0] + g * sepia_matrix[2][1] + b * sepia_matrix[2][2])

            sepia_image[y, x] = [min(255, sepia_r), min(255, sepia_g), min(255, sepia_b)]

    return sepia_image