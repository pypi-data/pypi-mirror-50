from rexart.objects import Sample, Histogram, Template
from rexart.utils import draw_ratio_with_line, draw_atlas_label, set_labels, shrink_pdf
from pathlib import PosixPath
import matplotlib.pyplot as plt
import numpy as np
import re
import yaml
import uproot
import logging

log = logging.getLogger(__name__)


def stackem(args, region, data, histograms, band=None, figsize=(6, 5.25)):
    """Create a stack plot

    Parameters
    ----------
    args : argparse.ArgumentParser
       command line arguments
    region : str
       region from TRExFitter
    data : rexart.objects.Sample
       data sample
    histograms : List[rexart.objects.Sample]
       list of MC samples to stack
    band : Optional[uproot_methods.classes.TGraphAsymmErrors]
       error band
    figsize : tuple(float, float)
       matplotlib figure size

    Returns
    -------
    fig : matplotlib.figure.Figure
       matplotlib fiture
    axes : tuple(matplotlib.axes.Axes, matplotlib.axes.Axes)
       matplotlib axes (main, ratio)
    """
    # fmt: off
    fig, (ax, axr) = plt.subplots(2, 1, sharex=True, figsize=figsize,
                                  gridspec_kw=dict(height_ratios=[3.25, 1], hspace=0.025))
    expected_sum = np.sum([h.content for h in histograms], axis=0)
    expected_err = np.sqrt(np.sum([h.sumw2 for h in histograms], axis=0))
    ax.hist([h.bin_centers for h in histograms], weights=[h.content for h in histograms],
            bins=histograms[0].bins, histtype="stepfilled", stacked=True,
            color=[h.sample.color for h in histograms], label=[h.sample.tex for h in histograms])
    ax.errorbar(data.bin_centers, data.content, yerr=data.error, fmt="ko", label="Data", zorder=999)
    set_labels(ax, histograms[0])
    ax.set_ylim([ax.get_ylim()[0], ax.get_ylim()[1] * 1.5])

    if band is not None:
        yerrlo = np.hstack([band.yerrorslow, band.yerrorslow[-1]])
        yerrhi = np.hstack([band.yerrorshigh, band.yerrorshigh[-1]])
        expected_sum4band = np.hstack([expected_sum, expected_sum[-1]])
        axr.fill_between(x=data.bins, y1=1 - yerrlo / expected_sum4band, y2=1 + yerrhi / expected_sum4band,
                         step="post", hatch="///", facecolor="none", edgecolor="cornflowerblue", linewidth=0.0,
                         zorder=99, label="Uncertainty")
        ax.fill_between(x=data.bins,y1=(expected_sum4band - yerrlo), y2=(expected_sum4band + yerrhi),
                        step="post", hatch="///", facecolor="none", edgecolor="cornflowerblue", linewidth=0.0,
                        zorder=99, label="Uncertainty")
    # fmt: on
    draw_ratio_with_line(axr, data, expected_sum, expected_err)
    axr.set_ylim([0.8, 1.2])
    axr.set_yticks([0.9, 1.0, 1.1])
    axr.set_xlabel(data.mpl_title, horizontalalignment="right", x=1.0)

    ax.legend(loc="upper right")
    handles, labels = ax.get_legend_handles_labels()
    handles.insert(0, handles.pop())
    labels.insert(0, labels.pop())
    ax.legend(handles, labels, loc="upper right")

    raw_region = region.split("reg")[-1].split("_")[0]
    extra_line1 = f"$\\sqrt{{s}}$ = 13 TeV, {args.lumi} fb$^{{-1}}$"
    extra_line2 = f"$pp\\rightarrow tW \\rightarrow e^{{\\pm}}\\mu^{{\\mp}}+{raw_region}$"
    extra_line3 = "Pre-fit"
    draw_atlas_label(ax, extra_lines=[extra_line1, extra_line2, extra_line3])

    fig.subplots_adjust(left=0.115, bottom=0.115, right=0.965, top=0.95)
    return fig, (ax, axr)


def prefit_histograms(args, fit_name, region, samples):
    """Prepare prefit histogram objects

    Parameters
    ---------
    args : argparse.ArgumentParser
       command line arguments
    fit_name : str
       TRExFitter fit name
    region : str
       TRExFitter region
    samples : List[rexart.objects.Sample]
       list of MC samples

    Returns
    -------
    data : rexart.objects.Histogram
       data histogram
    histograms : List[rexart.objects.Histogram]
       MC histograms
    band : uproot_methods.classes.TGraphAsymmErrors
       uncertainty band
    """
    hfile = f"{args.workspace}/Histograms/{fit_name}_{region}_histos.root"
    bfile = f"{args.workspace}/Histograms/{fit_name}_{region}_preFit.root"
    band = uproot.open(bfile).get("g_totErr")
    histograms = [Histogram(hfile, region, sample) for sample in samples]
    data = Histogram(hfile, region, Sample("Data", "Data", "", "Data"))
    return data, histograms, band


def postfit_histograms(args, fit_name, region, samples):
    """Prepare postfit histogram objects

    Parameters
    ---------
    args : argparse.ArgumentParser
       command line arguments
    fit_name : str
       TRExFitter fit name
    region : str
       TRExFitter region
    samples : List[rexart.objects.Sample]
       list of MC samples

    Returns
    -------
    data : rexart.objects.Histogram
       data histogram
    histograms : List[rexart.objects.Histogram]
       MC histograms
    band : uproot_methods.classes.TGraphAsymmErrors
       uncertainty band

    """
    hfile = f"{args.workspace}/Histograms/{region}_postFit.root"
    bfile = f"{args.workspace}/Histograms/{region}_postFit.root"
    band = uproot.open(bfile).get("g_totErr_postFit")
    histograms = [Histogram(hfile, region, sample, postfit=True) for sample in samples]
    return histograms, band


def split_region_str(region):
    splits = region.split("_")
    if len(splits) == 1:
        return (region, "bdt_response")
    else:
        return (splits[0], "_".join(splits[1:]))


def run_stacks(args):
    """Given command line arguments generate stack plots

    Parameters
    ----------
    args : argparse.ArgumentParser

    """
    with open(args.config, "r") as f:
        yaml_config = yaml.load(f, Loader=yaml.FullLoader)
    samples = [Sample(**d) for d in yaml_config["samples"]]
    samples.reverse()
    templates = {t["var"]: Template(**t) for t in yaml_config["templates"]}
    outd = "."
    if args.out_dir:
        outd = args.out_dir
        if outd != ".":
            PosixPath(args.out_dir).mkdir(parents=True, exist_ok=True)

    fit_name = PosixPath(args.workspace).stem
    hfiledir = PosixPath(f"{fit_name}/Histograms")
    regions = []
    if args.skip_regions is not None:
        skipregex = re.compile(args.skip_regions)
    else:
        skipregex = None
    for hfile in hfiledir.iterdir():
        if "_histos.root" in hfile.name:
            region = hfile.name.split("_histos.root")[0].split(f"{fit_name}_")[-1]
            if skipregex:
                if re.search(skipregex, region):
                    continue
            regions.append(region)

    for region in regions:
        raw_region, template_variable = split_region_str(region)
        data, histograms, band = prefit_histograms(args, fit_name, region, samples)
        data.unit = templates[template_variable].unit
        data.mpl_title = templates[template_variable].mpl_title
        fig, (ax, axr) = stackem(args, region, data, histograms, band=band)
        out_name = f"{outd}/preFit_{region}.pdf"
        fig.savefig(out_name)
        plt.close(fig)
        if args.shrink:
            shrink_pdf(out_name)
        log.info(f"Done with {region} prefit")

        if args.do_postfit:
            histograms, band = postfit_histograms(args, fit_name, region, samples)
            fig, (ax, axr) = stackem(args, region, data, histograms, band=band)
            axr.set_ylim([0.9, 1.1])
            axr.set_yticks([0.95, 1.0, 1.05])
            out_name = f"{outd}/postFit_{region}.pdf"
            fig.savefig(out_name)
            plt.close(fig)
            if args.shrink:
                shrink_pdf(out_name)
            log.info(f"Done with {region} postfit")
