from rexart.objects import NuisPar
from rexart.utils import shrink_pdf
from pathlib import PosixPath
import matplotlib.pyplot as plt
import numpy as np
import yaml
import logging

log = logging.getLogger(__name__)


def get_blank_systematics(config_file):
    """Get list of NPs and categories from TRExFitte config file

    Parameters
    ----------
    config_file : str
        name of config file

    Returns
    -------
    nps : list
        list of nuisance parameters
    categories: set
        all categories that were found
    """
    trex_config = PosixPath(config_file)
    nps = []
    with trex_config.open("r") as f:
        config_blocks = f.read().split("\n\n")
        for block in config_blocks:
            if "Systematic:" in block:
                if block[0] == "%":
                    continue
                block = block.replace("\n  ", "\n")
                s = yaml.load(block, Loader=yaml.FullLoader)
                np = NuisPar(name=s["Systematic"], category=s["Category"], title=s["Title"])
                nps.append(np)
    categories = set()
    nps = {np.name: np for np in nps}
    for npn, np in nps.items():
        categories.add(np.category)
    return nps, categories


def draw_pulls(args, nps):
    """Draw pulls from command line arguments and nuisance parameters

    Parameters
    ----------
    args : argparse.ArgumentParser
       command line arguments
    nps : list
       list of nuisance parameters to draw

    Returns
    -------
    fig : matplotlib.figure.Figure
       matplotlib fiture
    ax : matplotlib.axes.Axes
       matplotlib axis
    """
    Y_OFFSET_PT = 0.00
    Y_OFFSET_TEXT = 0.095
    Y_OFFSET_TEXT_MEAN = 0.165
    X_OFFSET_TEXT = 0.035

    xval = np.array([np.mean for np in nps])
    yval = np.array([(i + 1) for i in range(len(xval))])
    xerr_lo = np.array([np.minus for np in nps])
    xerr_hi = np.array([np.plus for np in nps])
    ylabels = [np.title for np in nps]

    fig, ax = plt.subplots(figsize=(10, len(yval) * 0.5))
    ax.fill_betweenx([-50, 500], -2, 2, color="yellow")
    ax.fill_betweenx([-50, 500], -1, 1, color="limegreen")
    ax.set_yticks(yval)
    ax.set_yticklabels(ylabels)
    ax.errorbar(xval, yval, xerr=[abs(xerr_lo), xerr_hi], fmt="ko", capsize=3)
    ax.set_xlim([-2.2, 2.2])
    ax.set_ylim([0.0, len(yval) + 1])
    ax.grid(color="black", alpha=0.15)

    # fmt: off
    if not args.no_text:
        for mean, iyval, minus, plus in zip(xval, yval, xerr_lo, xerr_hi):
            ax.text(mean, iyval + Y_OFFSET_TEXT_MEAN, "${}$".format(round(mean, 3)),
                    color="black", size=10, horizontalalignment="center")
            ax.text(mean + minus - 6.5 * X_OFFSET_TEXT, iyval + Y_OFFSET_TEXT, "${}$".format(round(minus, 3)),
                    color="black", size=10, horizontalalignment="center")
            ax.text(mean + plus + X_OFFSET_TEXT, iyval + Y_OFFSET_TEXT, "${}$".format(round(plus, 3)),
                    color="black", size=10)
    # fmt: on

    fig.subplots_adjust(left=0.5)
    ax.set_xlabel(r"$\left(\hat\theta - \theta_0\right) / \Delta \theta$")
    return fig, ax


def run_pulls(args):
    """Given command line arguments generate pull plots

    Parameters
    ----------
    args : argparse.ArgumentParser

    """
    systematics, categories = get_blank_systematics(args.config)
    fit_name = PosixPath(args.workspace).stem
    fit_result = PosixPath(f"{args.workspace}/Fits/{fit_name}.txt")
    np_by_cat = {c: [] for c in categories}
    with fit_result.open("r") as f:
        lines = f.read().split("CORRELATION_MATRIX")[0].strip()
        for line in lines.split("\n")[2:-1]:
            if line.startswith("gamma"):
                continue
            elements = line.split()
            systematics[elements[0]].mean = float(elements[1])
            systematics[elements[0]].plus = float(elements[2])
            systematics[elements[0]].minus = float(elements[3])
            np_by_cat[systematics[elements[0]].category].append(systematics[elements[0]])

    outd = "."
    if args.out_dir:
        outd = args.out_dir
        if outd != ".":
            PosixPath(args.out_dir).mkdir(parents=True, exist_ok=True)

    for category, nps in np_by_cat.items():
        fig, ax = draw_pulls(args, nps)
        out_name = f"{outd}/pulls_{category}.pdf"
        fig.savefig(out_name, bbox_inches="tight")
        if args.shrink:
            shrink_pdf(out_name)
        log.info(f"Done with {category}")
