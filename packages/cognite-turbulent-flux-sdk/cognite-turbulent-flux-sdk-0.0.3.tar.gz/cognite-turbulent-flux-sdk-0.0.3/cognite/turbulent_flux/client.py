from typing import *
import os
import requests
import pandas as pd
import numpy as np
import cognite.turbulent_flux.config as conf
from cognite.turbulent_flux.utils import _fill_path_variables, _tree_list_lengths


def _get_headers(api_key, **kwargs):
    # Add content-type and api key to header
    kwargs.update(**{'Content-Type': 'application/json', 'api-key': api_key})
    return kwargs


def _build_df(jsons: List[Dict], interpolate: bool = False) -> pd.DataFrame:
    static = jsons[0]['static']
    pos_vol, pos_bound = [np.array(static[key], dtype=float) for key in ('Position_Volume', 'Position_Boundary')]
    coord_dfs = {col: pd.DataFrame({col: np.array(static[col], dtype=float)}).set_index(pos_bound) for col in ('X', 'Z')}

    var_attributes = static['VariableAttributes']
    dfs = []
    # Iterate response jsons
    for json in jsons:
        for line in json['results']:
            # Complete sub-DataFrame, containing all positions
            subdf = pd.DataFrame({'pos': np.sort(np.hstack((pos_vol, pos_bound)))})\
                .set_index('pos')
            # Put data in DataFrame
            for col, data in line.items():
                # Handle multiple types of data
                if col in var_attributes.keys() and type(data) is list and len(data) > 1:
                    # Variable is spacial
                    # Make sure the variable is recognized
                    assert 'Placement' in var_attributes[col].keys(), f'Variable {col} has no attribute Placement'
                    assert var_attributes[col]['Placement'] in ('Boundary', 'Volume'),\
                        f'{col}\'s placement cannot be identified'

                    idx = pos_vol if var_attributes[col]['Placement'] == 'Volume' else pos_bound
                    if var_attributes[col]['Placement'] == 'Volume':
                        # Remove boundaries of calculated arrays
                        data = data[1:-1]

                    subdf[col] = pd.DataFrame({col: np.array(data, dtype=float)}).set_index(idx)

                elif col in ('time', 'Valve opening'):
                    # Variable is non-spacial
                    subdf[col] = np.full(subdf.shape[0], data[0] if type(data) is list else data, dtype=float)

                # Unrecognized variables
            subdf['pos'] = subdf.index
            for col, coords in coord_dfs.items():
                subdf[col] = coords
            dfs.append(subdf)
    df = pd.concat(dfs, sort=False)
    df = df.astype(dtype={'time': int})
    df.set_index(['time', 'pos'], inplace=True)
    if interpolate:
        df.interpolate(inplace=True)
        df.bfill(inplace=True)
    return df


def _as_json(jsons: List[Dict]) -> List:
    results = [time_slice for json in jsons for time_slice in json['response']]
    return results


class TFClient:
    """
    Client class for fetching data from different Turbulent Flux API endpoints.
    """
    def __init__(self, api_key: str = None, project: str = None):
        if project is None:
            assert False, 'Project name not specified. Include this as a keyword argument.'
        self.project: str = project
        if api_key is None:
            assert 'TF_API_KEY' in os.environ.keys(),\
                'API key not specified. Set the environment variable TF_API_KEY or pass api_key to TFClient()'
            self.api_key = os.environ['TF_API_KEY']
        else:
            self.api_key = api_key

    def _get_results(self, project: str, simulation_id: str) -> Dict:
        path = _fill_path_variables(conf.urls['results'], project=project, id=simulation_id)
        return self._get_data(path)

    def _get_data(self, url: str) -> Dict:
        response = requests.get(url, headers=_get_headers(self.api_key))
        if response.status_code != 200:
            print(response.text)
            raise AssertionError('Expected status code 200, something went wrong')
        return response.json()

    def get_results_df(self, simulation_id: str, interpolate: bool = True,
                       return_structured: bool = True, return_json: bool = False)\
            -> Union[Dict, Tuple[pd.DataFrame, Dict], Tuple[List, Dict], Tuple[pd.DataFrame, List, Dict]]:
        """
            Returns a tuple of results from simulation in project with simulation_id.
            The order of the tuple is (structured, json, static), with only the enabled elements present.
            The interpolation flag fills in all NaNs using linear interpolation.
            Can optionally include the original json structure of the results field

            Args:
                simulation_id (str): The id of the simulation to get data from.
                interpolate (bool): Flag for whether or not to interpolate the data in the structured DataFrame
                return_structured (bool): Return structured DataFrame
                return_json (bool): Return original json data

            Returns:
                Union[Tuple[Dict, pd.DataFrame], Tuple[Dict, List], Tuple[Dict, pd.DataFrame, List]]

        """
        r = self._get_results(self.project, simulation_id)
        jsons = [r]
        # Keep requesting until all data is fetched
        while r['next']:
            r = self._get_data(conf.config_parsed['urlbase'] + r['next'])
            jsons.append(r)

        # Collect all data
        static = jsons[0]['static']

        df = json = None
        if return_structured:
            df = _build_df(jsons, interpolate=interpolate)
        if return_json:
            json = _as_json(jsons)

        if return_json and return_structured:
            return df, json, static
        if return_json:
            return json, static
        if return_structured:
            return df, static
        return static



