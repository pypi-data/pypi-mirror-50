import numpy as np
import mahotas as mh
from laocoon import equalization as eq


class EdU_Pipeline:
    """
    A class that represents the pipeline for EdU image analysis.

    Attributes
    ----------
    dapi_coords : list
        Coordinates of the cell "centers" in the DAPI channel. Used as a reference.
    checked : list
        Keeps track of which cells have already been counted in other channels.
    coords : list
        Coordinates of all the cell "centers" in the EdU channel.
    count : int
        The number of cells counted in the image.

    Methods
    -------
    analyze_edu_hist_eps(file, dapi_coords, checked)
        Calculates the number of counted cells and their coordinates with histogram
        equalization and Gaussian filter preprocessing and epsilon quality control.
    analyze_edu_hist(file)
        Calculates the number of counted cells and their coordinates with histogram
        equalization and Gaussian filter preprocessing.
    analyze_edu_eps(file, dapi_coords, checked)
        Calculates the number of counted cells and their coordinates with Gaussian
        filter preprocessing and epsilon quality control.
    analyze_edu(file)
        Calculates the number of counted cells and their coordinates with Gaussian
        filter preprocessing.
    epsilon(edu_coords, dapi_coords, checked)
        Helper function for implementing epsilon quality control.
    """


    def __init__(self, file, checked, dapi_coords, hist=True, epsilon=True):
        """
        Parameters
        ----------
        file : str
            The path to the image.
        checked : list
            Keeps track of which cells have already been counted in other channels.
        dapi_coords : list
            Coordinates of all the cell "centers" in the DAPI channel. Used as a reference.
        hist : boolean, optional
            Decides whether to perform histogram equalization preprocessing on the image
            (default is True).
        epsilon : boolean, optional
            Decides whether to perform epsilon value quality control on the image
            (default is True).
        """

        self.dapi_coords = dapi_coords
        self.checked = checked
        if hist and epsilon:
            self.coords, self.count, self.checked = self.analyze_edu_hist_eps(file, dapi_coords, checked)
        if hist and not epsilon:
            self.count, self.coords = self.analyze_edu_hist(file)
        if not hist and epsilon:
            self.coords, self.count, self.checked = self.analyze_edu_eps(file, dapi_coords, checked)
        else:
            self.count, self.coords = self.analyze_edu(file)


    def analyze_edu_hist_eps(self, file, dapi_coords, checked):
        """
        Calculates the number of counted cells and their coordinates with histogram
        equalization and Gaussian filter preprocessing and epsilon quality control.

        Parameters
        ----------
        file : str
            The path to the image.
        dapi_coords : list
            Coordinates of all the cell "centers" in the DAPI channel. Used as a reference.
        checked : list
            Keeps track of which cells have already been counted in other channels.

        Returns
        -------
        list
            Coordinates of all the cell "centers" in the EdU channel.
        int
            The number of cells counted in the image.
        list
            Keeps track of which cells have already been counted in other channels.
        """

        img = mh.imread(file)
        imgg = mh.colors.rgb2gray(img)
        imgg = eq.hist_eq(imgg)
        imggf = mh.gaussian_filter(imgg,15.3).astype(np.uint8)
        rmax = mh.regmax(imggf)
        edu_seeds, edu_nuclei = mh.label(rmax)
        edu_coords = mh.center_of_mass(imgg,labels=edu_seeds)
        count, checked = self.epsilon(edu_coords,dapi_coords,checked)
        return edu_coords, count, checked


    def analyze_edu_hist(self, file):
        """
        Calculates the number of counted cells and their coordinates with histogram
        equalization and Gaussian filter preprocessing.

        Parameters
        ----------
        file : str
            The path to the image.

        Returns
        -------
        int
            The number of cells counted in the image.
        list
            Coordinates of all the cell "centers" in the EdU channel.
        """

        img = mh.imread(file)
        imgg = mh.colors.rgb2gray(img)
        imgg = eq.hist_eq(img)
        imggf = mh.gaussian_filter(imgg,15.3).astype(np.uint8)
        rmax = mh.regmax(imggf)
        edu_seeds, edu_nuclei = mh.label(rmax)
        edu_coords = mh.center_of_mass(imgg,labels=edu_seeds)
        return edu_nuclei,edu_coords


    def analyze_edu_eps(self, file, dapi_coords, checked):
        """
        Calculates the number of counted cells and their coordinates with Gaussian
        filter preprocessing and epsilon quality control.

        Parameters
        ----------
        file : str
            The path to the image.
        dapi_coords : list
            Coordinates of all the cell "centers" in the DAPI channel. Used as a reference.
        checked : list
            Keeps track of which cells have already been counted in other channels.

        Returns
        -------
        list
            Coordinates of all the cell "centers" in the EdU channel.
        int
            The number of cells counted in the image.
        list
            Keeps track of which cells have already been counted in other channels.
        """

        img = mh.imread(file)
        imgg = mh.colors.rgb2gray(img)
        imggf = mh.gaussian_filter(imgg,11).astype(np.uint8)
        rmax = mh.regmax(imggf)
        edu_seeds, edu_nuclei = mh.label(rmax)
        edu_coords = mh.center_of_mass(imgg,labels=edu_seeds)
        count, checked = self.epsilon(edu_coords,dapi_coords,checked)
        return edu_coords, count, checked


    def analyze_edu(self, file):
        """
        Calculates the number of counted cells and their coordinates with Gaussian
        filter preprocessing.

        Parameters
        ----------
        file : str
            The path to the image.

        Returns
        -------
        int
            The number of cells counted in the image.
        list
            Coordinates of all the cell "centers" in the EdU channel.
        """

        img = mh.imread(file)
        imgg = mh.colors.rgb2gray(img)
        imggf = mh.gaussian_filter(imgg,11).astype(np.uint8)
        rmax = mh.regmax(imggf)
        edu_seeds, edu_nuclei = mh.label(rmax)
        edu_coords = mh.center_of_mass(imgg,labels=edu_seeds)
        return edu_nuclei,edu_coords


    def epsilon(self, edu_coords, dapi_coords, checked):
        """
        Helper function for implementing epsilon quality control.

        Parameters
        ----------
        edu_coords : list
            Coordinates of all the cell "centers" in the EdU channel.
        dapi_coords : list
            Coordinates of all the cell "centers" in the DAPI channel. Used as a reference.
        checked : list
            Keeps track of which cells have already been counted in other channels.
        """

        edu_count = 0
        for i in range(len(edu_coords)):
            for j in range(len(dapi_coords)):
                dist = (dapi_coords[j][0]-edu_coords[i][0])*(dapi_coords[j][0]-edu_coords[i][0])+(dapi_coords[j][1]-edu_coords[i][1])*(dapi_coords[j][1]-edu_coords[i][1])
                if dist <= 440:
                    edu_count += 1
                    checked[j] += 1
        return edu_count,checked
