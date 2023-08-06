from dataclasses import dataclass
from rexart.objects import Sample, Template

samples = [
    Sample(name="tW", signature="tW", color="#1f77b4", tex="$tW$"),
    Sample(name="ttbar", signature="ttbar", color="#d62728", tex="$t\\bar{t}$"),
    Sample(name="Diboson", signature="Diboson", color="#2ca02c", tex="Diboson"),
    Sample(name="Zjets", signature="Zjets", color="#ff7f0e", tex="$Z+$jets"),
    Sample(name="MCNP", signature="MCNP", color="#9467bd", tex="MCNP"),
]

samples.reverse()


@dataclass
class RegionMeta:
    title: str = ""
    unit: str = ""
    logy: bool = False


# fmt: off
region_meta = {
    "bdt_response": RegionMeta("Classifier Response", ""),
    "cent_lep1lep2": RegionMeta("Centrality($\\ell_1\\ell_2$)", ""),
    "mT_lep2met": RegionMeta("$m_{\\mathrm{T}}(\\ell_2E_\\mathrm{T}^{\\mathrm{miss}})$", "GeV"),
    "nloosejets": RegionMeta("$N_j^{\\mathrm{soft}}$", "", True),
    "nloosebjets": RegionMeta("$N_b^{\\mathrm{soft}}$", "", True),
    "deltapT_lep1lep2_jet3": RegionMeta("$\\Delta p_{\\mathrm{T}}(\\ell_1\\ell_2, j_3)$", "GeV"),
    "deltapT_lep1_jet1": RegionMeta("$\\Delta p_{\\mathrm{T}}(\\ell_1, j_1)$", "GeV"),
    "mass_lep2jet1": RegionMeta("$m_{\\ell_2 j_1}$", "GeV"),
    "mass_lep1jet2": RegionMeta("$m_{\\ell_1 j_2}$", "GeV"),
    "mass_lep1jet1": RegionMeta("$m_{\\ell_1 j_1}$", "GeV"),
    "mass_lep1jet3": RegionMeta("$m_{\\ell_1 j_3}$", "GeV"),
    "mass_lep2jet2": RegionMeta("$m_{\\ell_2 j_2}$", "GeV"),
    "psuedoContTagBin_jet3": RegionMeta("$b$-tag bin ($j_3$)", ""),
    "psuedoContTagBin_jet2": RegionMeta("$b$-tag bin ($j_2$)", ""),
    "psuedoContTagBin_jet1": RegionMeta("$b$-tag bin ($j_1$)", ""),
    "pTsys_lep1lep2jet1": RegionMeta("$p_{\\mathrm{T}}^{\\mathrm{sys}}(\\ell_1\\ell_2 j_1)$", "GeV"),
    "pTsys_lep1lep2jet1jet2met": RegionMeta("$p_{\\mathrm{T}}^{\\mathrm{sys}}(\\ell_1\\ell_2 j_1 j_2 E_{\\mathrm{T}}^{\\mathrm{miss}})$", "GeV"),
    "pTsys_lep1lep2jet1met": RegionMeta("$p_{\\mathrm{T}}^{\\mathrm{sys}}(\\ell_1\\ell_2 j_1 E_{\\mathrm{T}}^{\\mathrm{miss}})$", "GeV"),
    "pTsys_lep1lep2": RegionMeta("$p_{\\mathrm{T}}^{\\mathrm{sys}}(\\ell_1\\ell_2)$", "GeV"),
    "pTsys_lep1lep2met": RegionMeta("$p_{\\mathrm{T}}^{\\mathrm{sys}}(\\ell_1\\ell_2 E_{\\mathrm{T}}^{\\mathrm{miss}})$", "GeV"),
    "pTsys_lep1lep2jet1jet2jet3met": RegionMeta("$p_{\\mathrm{T}}^{\\mathrm{sys}}(\\ell_1\\ell_2 j_1 j_2 j_3 E_{\\mathrm{T}}^{\\mathrm{miss}})$", "GeV"),
    "deltaR_lep2_jet1": RegionMeta("$\\Delta R(\\ell_2, j_1)$", ""),
    "deltaR_jet1_jet3": RegionMeta("$\\Delta R(j_1, j_3)$", ""),
    "deltaR_lep1_jet1": RegionMeta("$\\Delta R(\\ell_1, j_1)$", ""),
    "deltaR_lep1_lep2": RegionMeta("$\\Delta R(\\ell_1, \\ell_2)$", ""),
    "pT_lep1": RegionMeta("$p_{\\mathrm{T}}(\\ell_1)$", "GeV"),
    "pT_lep2": RegionMeta("$p_{\\mathrm{T}}(\\ell_2)$", "GeV"),
    "pT_jet1": RegionMeta("$p_{\\mathrm{T}}(j_1)$", "GeV"),
    "pT_jet2": RegionMeta("$p_{\\mathrm{T}}(j_2)$", "GeV"),
    "pT_jet3": RegionMeta("$p_{\\mathrm{T}}(j_3)$", "GeV"),
    "eta_lep1": RegionMeta("$\\eta(\\ell_1)$", ""),
    "eta_lep2": RegionMeta("$\\eta(\\ell_2)$", ""),
    "eta_jet1": RegionMeta("$\\eta(j_1)$", ""),
    "eta_jet2": RegionMeta("$\\eta(j_2)$", ""),
    "eta_jet3": RegionMeta("$\\eta(j_3)$", ""),
    "met": RegionMeta("$E_{\\mathrm{T}}^{\\mathrm{miss}}$", "GeV"),
}
# fmt: on
