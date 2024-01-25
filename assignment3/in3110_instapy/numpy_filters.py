"""numpy implementation of image filters"""
from __future__ import annotations

import numpy as np


def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    gray_image = np.empty_like(image)

    # Hint: use numpy slicing in order to have fast vectorized code
    r = image[:, :, 0]
    g = image[:, :, 1]
    b = image[:, :, 2]

    gray_image = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
    # Return image (make sure it's the right type!)
    return gray_image


def numpy_color2sepia(image: np.array, k: float = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
        you may ignore it)

    Returns:
        np.array: sepia_image
    """

    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError(f"k must be between [0-1], got {k=}")

    sepia_image = np.dot(image, sepia_matrix.T)

    # define sepia matrix (optional: with stepless sepia changes)
    sepia_matrix =  sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])

    # HINT: For version without adaptive sepia filter, use the same matrix as in the pure python implementation
    # use Einstein sum to apply pixel transform matrix
    # Apply the matrix filter
    sepia_image = np.where(sepia_image > 255, 255, sepia_image).astype(np.uint8)

    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255
    sepia_image[sepia_image > 255] = 255

    # Return image (make sure it's the right type!)
    return sepia_image