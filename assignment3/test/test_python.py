import numpy as np
from in3110_instapy.python_filters import python_color2gray, python_color2sepia


def test_color2gray(image):
    # run color2gray
    gray_image = python_color2gray(image)

    # check that the result has the right shape, type
    assert gray_image.shape == image.shape[:-1]
    assert gray_image.dtype == np.uint8

    # assert uniform r,g,b values
    assert np.all(gray_image[..., 0] == gray_image[..., 1])
    assert np.all(gray_image[..., 1] == gray_image[..., 2])


def test_color2sepia(image):
    # run color2sepia
    sepia_image = python_color2sepia(image)

    # check that the result has the right shape, type
    assert sepia_image.shape == image.shape
    assert sepia_image.dtype == np.uint8

    # verify some individual pixel samples according to the sepia matrix
    assert np.allclose(sepia_image[0, 0], [ 98,  89,  69])
    assert np.allclose(sepia_image[0, 1], [ 98,  89,  69])
    assert np.allclose(sepia_image[0, 2], [ 98,  89,  69])
    assert np.allclose(sepia_image[1, 0], [ 98,  89,  69])
    assert np.allclose(sepia_image[1, 1], [255, 240, 185])
    assert np.allclose(sepia_image[1, 2], [  0,   0,   0])