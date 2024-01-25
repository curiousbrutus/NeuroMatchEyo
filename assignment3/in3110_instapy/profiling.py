"""
Profiling (IN4110 only)
"""
from __future__ import annotations

import cProfile
import pstats

import in3110_instapy
import line_profiler

from . import io


def profile_with_cprofile(filter, image, ncalls=3):
    """Profile filter(image) with cProfile

    Statistics will be printed to stdout.

    Args:

        filter (callable): filter function
        image (ndarray): image to filter
        ncalls (int): number of repetitions to measure
    """
    profiler = cProfile.Profile()
    # run `filter(image)` in the profiler
    for _ in range(ncalls):
        profiler.runcall(filter, image)
    stats = pstats.Stats(profiler)
    # print the top 10 results, sorted by cumulative time
    stats.sort_stats("cumulative")
    stats.print_stats(10)


def profile_with_line_profiler(filter, image, ncalls=3):
    """Profile filter(image) with line_profiler

    Statistics will be printed to stdout.

    Args:

        filter (callable): filter function
        image (ndarray): image to filter
        ncalls (int): number of repetitions to measure
    """
    # create the LineProfiler
    profiler = line_profiler.LineProfiler()
    # tell it to measure the function we are given
    profiler.add_function(filter)
    # Measure filter(image)
    profiler.runctx(f"{filter.__name__}(image)", globals(), locals())
    # print statistics
    profiler.print_stats()


def run_profiles(profiler: str = "cprofile"):
    """Run profiles of every implementation

    Args:

        profiler (str): either 'line_profiler' or 'cprofile'
    """
    # Select which profile function to use
    if profiler == "line_profiler":
        profile_func = profile_with_line_profiler
    elif profiler.lower() == "cprofile":
        profile_func = profile_with_cprofile
    else:
        raise ValueError(f"{profiler=} must be 'line_profiler' or 'cprofile'")

    # construct a random 640x480 image
    image = io.read_image("input.jpg")

    filter_names = ["color2gray", "color2sepia"]
    implementations = ["python", "numpy", "numba", "cython"]
    for filter_name in filter_names:
        for implementation in implementations:
            print(f"Profiling {implementation} {filter_name} with {profiler}:")
            filter = in3110_instapy.get_filter(filter_name, implementation)
            # call it once
            filter(image)
            profile_func(filter, image)


if __name__ == "__main__":
    print("Begin cProfile")
    run_profiles("cprofile")
    print("End cProfile")
    print("Begin line_profiler")
    run_profiles("line_profiler")
    print("End line_profiler")