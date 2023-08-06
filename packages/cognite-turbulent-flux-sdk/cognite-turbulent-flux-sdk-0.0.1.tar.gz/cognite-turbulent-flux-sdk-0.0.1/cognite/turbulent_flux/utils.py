import re
import pandas as pd
import scipy.interpolate as spi
import numpy as np
from typing import *

# Matches variable names preceded by ':'
match_path_vars = r':(\w+)(?=(/|$))'


def _fill_path_variables(path: str, **kwargs) -> str:
    for var in map(lambda x: x[0], re.findall(match_path_vars, path)):
        assert var in kwargs.keys(), 'Variable {var} not found in kwargs: {kwargs}'
    return re.sub(match_path_vars, lambda x: kwargs[x[0][1:]], path)


def _tree_list_lengths(tree):
    if type(tree) is dict:
        lentree = {}
        for key, val in tree.items():
            lentree[key] = _tree_list_lengths(val)
        return lentree
    if type(tree) is list:
        return len(tree)
    return 'not a list'


def interpolate_to_positions(df: pd.DataFrame, time_idx: int, positions: np.array):
    """Returns an array of interpolated values for the selected time index and positions.

    Args:
        df (pd.DataFrame): The full DataFrame of data from a TFClient.
        time_idx (int): The time index at which to interpolate the positions.
        positions (np.array): An array of positions to interpolate to.

    Returns:
        pd.DataFrame
    """
    xs = df.loc[time_idx].index.get_level_values('pos').to_numpy()
    ys = df.loc[time_idx].to_numpy().T
    interpolated_data = spi.interp1d(xs, ys)(positions)
    return pd.DataFrame(data=interpolated_data.T, index=pd.Index(positions, name='pos'), columns=df.columns)
