import logging
import sys
import numpy as np
from distutils.util import strtobool
import pandas as pd

# from haidata.haidatautils import mixed_list_to_int_list
from haidatautils import mixed_list_to_int_list, stringify_dict_value

logging.disable(sys.maxsize)
logger = logging.getLogger(__name__)


def set_excess_stdev(input_df, args_dict):
    
    args_dict["COLS"] = stringify_dict_value(args_dict, "COLS")
    if "BY" in args_dict.keys():
        args_dict["BY"] = stringify_dict_value(args_dict, "BY")
    if "VALUE" in args_dict.keys():
        args_dict["VALUE"] = stringify_dict_value(args_dict, "VALUE")

        
    int_list_to_check = mixed_list_to_int_list(args_dict["COLS"], input_df.columns.values.tolist())
    
    # args_dict = dict({'NUM_STD': "3,6,5"})
    std_multipliers = [float(x) for x in str(args_dict["NUM_STD"]).split(",")] if \
        "NUM_STD" in args_dict.keys() else [10.0] * len(int_list_to_check)

    if len(int_list_to_check) > 1 and len(std_multipliers) == 1:
        std_multipliers = [std_multipliers[0]] * len(int_list_to_check)

    if len(std_multipliers) != len(int_list_to_check):
        raise ValueError(
            "Length of Std dev multipliers ({0}) does not match length of column identifiers ({1})".format(
                len(std_multipliers), len(int_list_to_check)))

    by_names = None if "BY" not in args_dict.keys() else \
        [int(x) for x in mixed_list_to_int_list(args_dict["BY"], input_df.columns.values.tolist())]
    if by_names is not None:
        if len(by_names) == 1 and len(int_list_to_check) > 1:
            # nonlocal by_names
            by_names = [by_names[0]] * len(int_list_to_check)
    
    by_values = None if "VALUE" not in args_dict.keys() else \
        [int(x) for x in mixed_list_to_int_list(args_dict["VALUE"], input_df.columns.values.tolist())]
    if by_values is not None:
        if len(by_values) == 1 and len(int_list_to_check) > 1:
            # nonlocal by_names
            by_values = [by_values[0]] * len(int_list_to_check)
    else:
        by_values = [np.nan]*len(int_list_to_check)

    if by_names is None:
        for column_name, std_multiplier, new_value in zip( input_df.columns[int_list_to_check].values.tolist(),
                                                           std_multipliers,
                                                           by_values):
            input_px = input_df.iloc[:, input_df.columns.get_loc(column_name)]
            mean_diff = input_px.mean()
            std_diff = input_px.std()
            test_series = np.abs((input_px - mean_diff) / std_diff)

            to_replace_idxs, = np.where(test_series < std_multiplier)
            input_df.iloc[to_replace_idxs,input_df.columns.get_loc(column_name)] = new_value
            
        return input_df
        
    else:

        new_dfs = []

        for column_name, std_multiplier, by_name, new_value in zip(input_df.columns[int_list_to_check].values.tolist(),
                                                                   std_multipliers, by_names, by_values):
            by_column_name = input_df.columns.values[by_name]
            by_values_subset = input_df[by_column_name].unique()

            for by_value in by_values_subset:  # by_value = by_values[0]
                input_df_subset = input_df[input_df[by_column_name] == by_value]
                
                input_px = input_df_subset[column_name]
                mean_diff = input_px.mean()
                std_diff = input_px.std()
                test_series = np.abs((input_px - mean_diff) / std_diff)

                idxs = np.where(test_series.values <= std_multiplier, True, False).flatten()
                input_df_subset = input_df_subset.iloc[idxs]

                new_dfs.append(input_df_subset)
                # print(by_value)

            input_df = pd.concat(new_dfs)
            
        input_df.sort_index(inplace=True)
        return input_df

#
