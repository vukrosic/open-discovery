"""Readable baseline for an exact grayscale image histogram."""


def histogram(image):
    counts = [0] * 256
    for value in image.get_flattened_data():
        counts[value] += 1
    return counts
