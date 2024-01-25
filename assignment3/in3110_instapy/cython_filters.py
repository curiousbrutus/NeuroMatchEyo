"""Cython implementation of filter functions"""
#from __future__ import annotations

import cython as C
import numpy as np
#cimport numpy as np
#cimport cython

if not C.compiled:
    raise ImportError(
        "Cython module not compiled! Check setup.py and make sure this package has been installed, not just imported in-place."
    )

# we may need a 'const uint8_t' type to make sure we accept 'read-only' arrays
const_uint8_t = C.typedef("const uint8_t")
float64_t = C.typedef(C.double)

@cython.boundscheck(False)
@cython.wraparound(False)

if not C.compiled:
    raise ImportError(
        "Cython module not compiled! Check setup.py and make sure this package has been installed, not just imported in-place."
    )

@cython.boundscheck(False)
@cython.wraparound(False)
def cython_color2gray(image):
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    cdef int height = image.shape[0]
    cdef int width = image.shape[1]
    cdef np.ndarray[np.uint8_t, ndim=2] gray_image = np.zeros((height, width), dtype=np.uint8)

    cdef int r, g, b, gray_value
    for y in range(height):
        for x in range(width):
            r = image[y, x, 0]
            g = image[y, x, 1]
            b = image[y, x, 2]

            gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)

            gray_image[y, x] = gray_value

    return gray_image


@cython.boundscheck(False)
@cython.wraparound(False)
def cython_color2sepia(image):
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    cdef const float64_t[:, :] sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])

    cdef int height = image.shape[0]
    cdef int width = image.shape[1]
    cdef np.ndarray[np.uint8_t, ndim=3] sepia_image = np.zeros((height, width, 3), dtype=np.uint8)

    cdef int r, g, b, sepia_r, sepia_g, sepia_b
    for y in range(height):
        for x in range(width):
            r = image[y, x, 0]
            g = image[y, x, 1]
            b = image[y, x, 2]

            sepia_r = int(r * sepia_matrix[0, 0] + g * sepia_matrix[0, 1] + b * sepia_matrix[0, 2])
            sepia_g = int(r * sepia_matrix[1, 0] + g * sepia_matrix[1, 1] + b * sepia_matrix[1, 2])
            sepia_b = int(r * sepia_matrix[2, 0] + g * sepia_matrix[2, 1] + b * sepia_matrix[2, 2])

            sepia_image[y, x] = [min(255, sepia_r), min(255, sepia_g), min(255, sepia_b)]

    return sepia_image
    for y in range(height):
        for x in range(width):
            r = image[y, x, 0]
            g = image[y, x, 1]
            b = image[y, x, 2]

            sepia_r = int(r * sepia_matrix[0][0] + g * sepia_matrix[0][1] + b * sepia_matrix[0][2])
            sepia_g = int(r * sepia_matrix[1][0] + g * sepia_matrix[1][1] + b * sepia_matrix[1][2])
            sepia_b = int(r * sepia_matrix[2][0] + g * sepia_matrix[2][1] + b * sepia_matrix[2][2])

            sepia_image[y, x] = [min(255, sepia_r), min(255, sepia_g), min(255, sepia_b)]

    return sepia_image

