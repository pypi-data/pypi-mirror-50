from __future__ import annotations
import uproot
import numpy as np
from dataclasses import dataclass, field
from typing import List


@dataclass
class Sample:
    """Defines a physics sample

    Attributes
    ----------

    name : str
       name of the sample
    signature : str
       name of the sample on disk
    color : str
       matplotlib color
    tex : str
       LaTeX label
    """
    name: str = "none"
    signature: str = "none"
    color: str = "black"
    tex: str = "none"


@dataclass
class NuisPar:
    """Defines a nuisance parameter from TRExFitter

    Attributes
    ----------

    name : str
       name on disk
    mean : float
       mean value
    minus : float
       minus part of the error bar
    plus : float
       plus part of the error bar
    category : str
       systematic category
    title : str
       a title for the plots
    """
    name: str = "none"
    mean: float = 0
    minus: float = 0
    plus: float = 0
    category: str = "none"
    title: str = "none"


@dataclass
class Template:
    """Defines a template for generation by WtStat

    Attributes
    ----------
    var : str
       variable (branch) from the tree
    region : List[str]
       list of regions where the template was calculated
    xmin : float
       axis range minimum
    xmax: float
       axis range maximum
    nbins : int
       number of bins
    use_region_binning : bool
       for wt-stat usage
    axis_title : str
       axis title for TRExFitter
    mpl_title : str
       axis title for matplotlib
    is_aux : bool
       for wt-stat usagse
    unit : str
       unit as a string (e.g. GeV)
    """
    var: str = ""
    regions: List[str] = field(default_factory=list)
    xmin: float = 0
    xmax: float = 0
    nbins: int = 0
    use_region_binning: bool = False
    axis_title: str = ""
    mpl_title: str = ""
    is_aux: bool = False
    unit: str = ""


@dataclass
class Histogram:
    """ defines a histogram from a TRExFitter file """
    hfile: str
    region: str
    sample: Sample
    unit: str = ""
    mpl_title: str = ""
    signature: str = ""
    postfit: bool = False

    def __post_init__(self):
        pfp = "" if not self.postfit else "h_"
        pfs = "" if not self.postfit else "_postFit"
        regionsig = f"{self.region}_" if not self.postfit else ""
        self.signature = f"{pfp}{regionsig}{self.sample.signature}{pfs}"
        try:
            self.uproothist = uproot.open(self.hfile).get(self.signature)
            self.content = self.uproothist.values
            self.content[self.content < 0] = 1.0e-6
        except KeyError:
            self.uproothist = None
            self.content = None

    def __bool__(self):
        return self.uproothist is not None

    def __call__(self):
        return self.uproothist

    @property
    def sumw2(self):
        return self.uproothist.variances

    @property
    def error(self):
        return np.sqrt(self.sumw2)

    @property
    def bins(self):
        return self.uproothist.edges

    @property
    def bin_centers(self):
        return (self.bins[1:] + self.bins[:-1]) * 0.5

    @property
    def bin_width(self):
        return round(self.bins[-1] - self.bins[-2], 2)

    def has_uniform_bins(self):
        diffs = np.ediff1d(self.bins)
        return np.allclose(diffs, diffs[0])
