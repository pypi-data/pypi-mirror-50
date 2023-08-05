import numpy as np
import mahotas as mh
from laocoon import equalization as eq


class RFP_Pipeline:
    """
    A class that represent the pipeline for RFP analysis.

    Attributes
    ----------
    dapi_coords : list
        Coordinates of the cell "centers" in the DAPI channel. Used as a reference.
    checked : list
        Keeps track of which cells have already been counted in other channels.
    coords : list
        Coordinates of all the cell "centers" in the RFP channel.
    count : int
        The number of cells counted in the image.

    Methods
    -------
    analyze_rfp_hist_eps(file, dapi_coords, checked)
        Calculates the number of counted cells and their coordinates with histogram
        equalization and Gaussian filter preprocessing and epsilon quality control.
    analyze_rfp_hist(file)
        Calculates the number of counted cells and their coordinates with histogram
        equalization and Gaussian filter preprocessing.
    analyze_rfp_eps(file, dapi_coords, checked)
        Calculates the number of counted cells and their coordinates with Gaussian
        filter preprocessing and epsilon quality control.
    analyze_rfp(file)
        Calculates the number of counted cells and their coordinates with Gaussian
        filter preprocessing.
    epsilon(rfp_coords, dapi_coords, checked)
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
            self.coords, self.count, self.checked = self.analyze_rfp_hist_eps(file, dapi_coords, checked)
        if hist and not epsilon:
            self.count, self.coords = self.analyze_rfp_hist(file)
        if not hist and epsilon:
            self.coords, self.count, self.checked = self.analyze_rfp_eps(file, dapi_coords, checked)
        else:
            self.count, self.coords = self.analyze_rfp(file)


    def analyze_rfp_hist_eps(self, file, dapi_coords, checked):
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
            Coordinates of all the cell "centers" in the RFP channel.
        int
            The number of cells counted in the image.
        list
            Keeps track of which cells have already been counted in other channels.
        """

        img = mh.imread(file)
        imgg = mh.colors.rgb2grey(img)
        imgg = eq.hist_eq(img)
        imggf = mh.gaussian_filter(imgg,4.8).astype(np.uint8)
        rmax = mh.regmax(imggf)
        rfp_seeds, rfp_nuclei = mh.label(rmax)
        rfp_coords = mh.center_of_mass(imgg,labels=rfp_seeds)
        count, checked = self.epsilon(rfp_coords,dapi_coords,checked)
        return rfp_coords, count, checked


    def analyze_rfp_hist(self, file):
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
            Coordinates of all the cell "centers" in the RFP channel.
        """

        img = mh.imread(file)
        imgg = mh.colors.rgb2gray(img)
        imgg = eq.hist_eq(img)
        imggf = mh.gaussian_filter(imgg,16.5).astype(np.uint8)
        rmax = mh.regmax(imggf)
        rfp_seeds, rfp_nuclei = mh.label(rmax)
        rfp_coords = mh.center_of_mass(imgg,labels=rfp_seeds)
        return rfp_nuclei,rfp_coords


    def analyze_rfp_eps(self, file, dapi_coords, checked):
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
            Coordinates of all the cell "centers" in the RFP channel.
        int
            The number of cells counted in the image.
        list
            Keeps track of which cells have already been counted in other channels.
        """

        img = mh.imread(file)
        imgg = mh.colors.rgb2grey(img)
        imggf = mh.gaussian_filter(imgg,14).astype(np.uint8)
        rmax = mh.regmax(imggf)
        rfp_seeds, rfp_nuclei = mh.label(rmax)
        rfp_coords = mh.center_of_mass(imgg,labels=rfp_seeds)
        count, checked = self.epsilon(rfp_coords,dapi_coords,checked)
        return rfp_coords, count, checked


    def analyze_rfp(self, file):
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
            Coordinates of all the cell "centers" in the RFP channel.
        """

        img = mh.imread(file)
        imgg = mh.colors.rgb2grey(img)
        imggf = mh.gaussian_filter(imgg,14).astype(np.uint8)
        rmax = mh.regmax(imggf)
        rfp_seeds, rfp_nuclei = mh.label(rmax)
        rfp_coords = mh.center_of_mass(imgg,labels=rfp_seeds)
        return rfp_nuclei,rfp_coords


    def epsilon(self, rfp_coords, dapi_coords, checked):
        """
        Helper function for implementing epsilon quality control.

        Parameters
        ----------
        edu_coords : list
            Coordinates of all the cell "centers" in the RFP channel.
        dapi_coords : list
            Coordinates of all the cell "centers" in the DAPI channel. Used as a reference.
        checked : list
            Keeps track of which cells have already been counted in other channels.
        """

        rfp_count = 0
        for i in range(len(rfp_coords)):
            for j in range(len(dapi_coords)):
                dist = (dapi_coords[j][0]-rfp_coords[i][0])*(dapi_coords[j][0]-rfp_coords[i][0])+(dapi_coords[j][1]-rfp_coords[i][1])*(dapi_coords[j][1]-rfp_coords[i][1])
                if dist <= 265:
                    rfp_count += 1
                    checked[j] += 1
        return rfp_count,checked
