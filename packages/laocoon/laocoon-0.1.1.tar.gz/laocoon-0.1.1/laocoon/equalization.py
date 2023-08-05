import numpy as np


def get_histogram(image,bins):
    """
    Returns the histogram representation of the pixels in the image.

    Attributes
    ----------
    image : list
        Flattened list of pixels that make up the image.
    bins : int
        Number of bins the histogram should have.

    Returns
    -------
    list
        Histogram representation of the image.
    """

    histogram = np.zeros(bins)
    for pixel in image:
        histogram[int(pixel)] += 1
    return histogram


def cumsum(a):
    """
    Returns the cumulative sum of an array.

    Attributes
    ----------
    a : list
        A list of numbers.

    Returns
    -------
    nparray
        Cumulative sum of all the numbers in a.
    """

    a = iter(a)
    b =[next(a)]
    for i in a:
        b.append(b[-1]+i)
    return np.array(b)


def hist_eq(imgg):
    """
    Performs histogram equalization on an image.

    Attributes
    ----------
    imgg : nparray
        The nparray representation of a greyscale image.

    Returns
    -------
    The new "equalized" image.
    """

    img_arr = np.asarray(imgg)
    flat = img_arr.flatten()

    hist = get_histogram(flat,256)
    cs = cumsum(hist)

    nj = (cs-cs.min())*255
    N = cs.max()-cs.min()
    cs = nj/N
    cs = cs.astype('uint8')

    img_new = cs[flat.astype(int)]
    return np.reshape(img_new,imgg.shape)
