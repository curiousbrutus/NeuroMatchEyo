# InstaPy

InstaPy is a Python package for applying color filters to images.

## Installation

You can install InstaPy using pip:

```
pip install instapy
```

## Usage

You can use InstaPy from the command line by running the `instapy` script:

```
instapy <file> [-o <out_file>] [-i <implementation>] [-f <filter>] [-s <scale>]
```

The `file` argument is the input image file. The `out_file` argument is the output image file (optional). The `implementation` argument is the filter implementation to use (`python`, `numpy`, `numba`, or `cython`). The `filter` argument is the filter to apply (`color2gray` or `color2sepia`). The `scale` argument is the scale factor to resize the image (optional).

For example, to apply the `color2gray` filter to an image using the `numpy` implementation and save the output to a file, you can run:

```
instapy input.jpg -o output.jpg -i numpy -f color2gray
```

You can also use InstaPy as a Python package by importing the `in3110_instapy` module and calling the `run_filter` function:

```python
import in3110_instapy

in3110_instapy.run_filter(
    file="input.jpg",
    out_file="output.jpg",
    implementation="numpy",
    filter="color2gray",
    scale=1,
)
```

This will apply the `color2gray` filter to the input image using the `numpy` implementation and save the output to a file.