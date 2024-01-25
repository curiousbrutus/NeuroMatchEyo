import numpy as np
import numpy.testing as nt
from in3110_instapy.numpy_filters import numpy_color2gray, numpy_color2sepia


def test_color2gray(image, reference_gray):
    # run color2gray
    gray_image = numpy_color2gray(image)

    # check that the result has the right shape, type
    assert gray_image.shape == image.shape[:-1]
    assert gray_image.dtype == np.uint8

    # check that the output matches the expected values
    nt.assert_allclose(gray_image, reference_gray, atol=1)


def test_color2sepia(image, reference_sepia):
    # run color2sepia
    sepia_image = numpy_color2sepia(image)

    # check that the result has the right shape, type
    assert sepia_image.shape == image.shape
    assert sepia_image.dtype == np.uint8

    # check that the output matches the expected values
    print(sepia_image)
    nt.assert_allclose(sepia_image, reference_sepia, atol=1)