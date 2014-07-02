
# tools
from .data_generator import generate_example_data
from .basics import date_convert, group_clusters, cluster_builder
from .analyses import generation_analysis, reproduction_number, create_2x2
from .analyses import analyze_2x2, odds_ratio, relative_risk, chi2, attributable_risk
from .analyses import diagnostic_accuracy, kappa_agreement, summary
from .rolling_proportion import rolling_proportion

# plotting
from .case_tree import build_graph, case_tree_plot
from .epicurve import epicurve_plot
from .checkerboard import checkerboard_plot
from .or_plot import or_plot

def get_data(fname):
    """Returns pandas dataframe of a line listing.
    Choices are 'example_data' and 'mers_line_list'
    Example_data is fake data. Mers_line_list is of the MERS-CoV outbreak
    of 2012-2014.
    """
    import os
    import pandas as pd

    this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "data", fname+".csv")

    data = pd.read_csv(DATA_PATH)

    return data
