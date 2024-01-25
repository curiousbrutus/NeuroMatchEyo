"""Command-line (script) interface to instapy"""
from __future__ import annotations

import argparse
import os
import sys

from in3110_instapy import io
from in3110_instapy.python_filters import python_color2gray, python_color2sepia
from in3110_instapy.numpy_filters import numpy_color2gray, numpy_color2sepia
from in3110_instapy.numba_filters import numba_color2gray, numba_color2sepia
from in3110_instapy.cython_filters import cython_color2gray, cython_color2sepia


def parse_args(args):
    parser = argparse.ArgumentParser(description='Apply a color filter to an image.')
    parser.add_argument('file', help='The filename to apply filter to')
    parser.add_argument('-o', '--out', help='The output filename')
    parser.add_argument('-g', '--gray', action='store_true', help='Select gray filter')
    parser.add_argument('-se', '--sepia', action='store_true', help='Select sepia filter')
    parser.add_argument('-sc', '--scale', type=float, help='Scale factor to resize image')
    parser.add_argument('-i', '--implementation', choices=['python', 'numpy', 'numba', 'cython'], default='python', help='The implementation')
    return parser.parse_args(args)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    args = parse_args(args)

    # read input image
    image = io.read_image(args.file)

    # apply scale factor if specified
    if args.scale:
        image = io.resize_image(image, args.scale)

    # apply filter based on implementation
    if args.implementation == 'python':
        if args.gray:
            filtered_image = python_color2gray(image)
        elif args.sepia:
            filtered_image = python_color2sepia(image)
    elif args.implementation == 'numpy':
        if args.gray:
            filtered_image = numpy_color2gray(image)
        elif args.sepia:
            filtered_image = numpy_color2sepia(image)
    elif args.implementation == 'numba':
        if args.gray:
            filtered_image = numba_color2gray(image)
        elif args.sepia:
            filtered_image = numba_color2sepia(image)
    elif args.implementation == 'cython':
        if args.gray:
            filtered_image = cython_color2gray(image)
        elif args.sepia:
            filtered_image = cython_color2sepia(image)

    # write output image
    if args.out:
        io.write_image(args.out, filtered_image)
    else:
        root, ext = os.path.splitext(args.file)
        io.write_image(f'{root}_filtered{ext}', filtered_image)


if __name__ == '__main__':
    main()

    import timeit

    def run_filter(
        file: str,
        out_file: str = None,
        implementation: str = "python",
        filter: str = "color2gray",
        scale: int = 1,
        runtime: bool = False,
    ) -> None:
        """Run the selected filter"""
        # load the image from a file
        image = io.read_image(file)
        if scale != 1:
            # Resize image, if needed
            image = io.resize_image(image, scale)

        # Apply the filter
        if implementation == "python":
            if filter == "color2gray":
                func = in3110_instapy.python_filters.python_color2gray
            elif filter == "color2sepia":
                func = in3110_instapy.python_filters.python_color2sepia
        elif implementation == "numpy":
            if filter == "color2gray":
                func = in3110_instapy.numpy_filters.numpy_color2gray
            elif filter == "color2sepia":
                func = in3110_instapy.numpy_filters.numpy_color2sepia
        elif implementation == "numba":
            if filter == "color2gray":
                func = in3110_instapy.numba_filters.numba_color2gray
            elif filter == "color2sepia":
                func = in3110_instapy.numba_filters.numba_color2sepia
        elif implementation == "cython":
            if filter == "color2gray":
                func = in3110_instapy.cython_filters.cython_color2gray
            elif filter == "color2sepia":
                func = in3110_instapy.cython_filters.cython_color2sepia

        if runtime:
            # track the average runtime over 3 runs
            runtime = timeit.timeit(lambda: func(image), number=3) / 3
            print(f"Average time over 3 runs: {runtime}s")

        filtered = func(image)

        if out_file:
            # save the file
            io.write_image(out_file, filtered)
        else:
            # not asked to save, display it instead
            io.display(filtered)