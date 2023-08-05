import numpy as np
import mahotas as mh
from laocoon import equalization as eq


class DAPI_Pipeline:
    """
    A class that represents the pipeline for DAPI image analysis.

    Attributes
    ----------
    coords : list
        Coordinates for all the detected cell "centers."
    count : int
        Number of counted cells.

    Methods
    -------
    analyze_dapi_hist(file)
        Calculates the number of counted cells and their coordinates with
        histogram equalization and Gaussian filter preprocessing.
    """


    def __init__(self, file):
        """
        Parameters
        ----------
        file : str
            The path to the image.
        """

        self.coords, self.count = self.analyze_dapi_hist(file)


    def analyze_dapi_hist(self, file):
        """
        Calculates the number of counted cells and their coordinates with histogram
        equalization and Gaussian filter preprocessing.

        Parameters
        ----------
        file : str
            The path to the image.

        Returns
        -------
        list
            The coordinates of all the cell "centers."
        int
            The number of cells counted in the image.
        """

        img = mh.imread(file)
        imgg = mh.colors.rgb2gray(img)
        imgg = eq.hist_eq(imgg)
        imggf = mh.gaussian_filter(imgg,7.5).astype(np.uint8)
        rmax = mh.regmax(imggf)
        dapi_seeds, dapi_nuclei = mh.label(rmax)
        dapi_coords = mh.center_of_mass(imgg,labels=dapi_seeds)
        return dapi_coords, dapi_nuclei
