"""numba-optimized filters"""
from __future__ import annotations

import numpy as np
import numba 
from numba import jit


@numba.jit(nopython=True)
def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    height, width, channels = image.shape

    gray_image = np.empty((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            r, g, b = image[y, x]

            gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)

            gray_image[y, x] = gray_value

    return gray_image

@jit(nopython=True)
def numba_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])


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