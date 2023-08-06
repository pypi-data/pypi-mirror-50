from enum import Enum
import pandas as pd
import numpy as np


class ReturnType(Enum):
    RATIO_RETURN = 0
    PERC_RETURN = 1
    DIFF_RETURN = 2
    LOG_RETURN = 3
    CUM_RATIO_RETURN = 4
    CUM_LOG_RETURN = 5
    
    @classmethod
    def from_string(cls, name):
        if name in cls.__members__.keys():
            return getattr(cls, name)
        else:
            return None
    
    def __call__(self, *args, **kwargs):
        if isinstance(args[0], pd.DataFrame):
            df = args[0]
            column_names = args[1] if isinstance(args[1], list) else [args[1]]
            for column_name in column_names:
                column_name = str(column_name)
                if self.value == ReturnType.LOG_RETURN.value:
                    df[[column_name]] = np.log(df[[column_name]]) - np.log(df[[column_name]].shift(1))
                elif self.value == ReturnType.RATIO_RETURN.value:
                    df[[column_name]] = df[[column_name]].shift(0) / df[[column_name]].shift(1)
                elif self.value == ReturnType.PERC_RETURN.value:
                    df[[column_name]] = (df[[column_name]].shift(0) - df[[column_name]].shift(1)) / df[
                        [column_name]].shift(1)
                elif self.value == ReturnType.DIFF_RETURN.value:
                    df[[column_name]] = (df[[column_name]].shift(0) - df[[column_name]].shift(1))
                elif self.value == ReturnType.CUM_RATIO_RETURN.value:
                    starting_value = df[[column_name]][0]
                    df[[column_name]] = df[[column_name]].shift(1) / starting_value
                elif self.value == ReturnType.CUM_LOG_RETURN.value:
                    starting_value = df[[column_name]][0]
                    df[[column_name]] = np.log(df[[column_name]]) / np.log(starting_value)
                else:
                    raise ValueError(f'{self.name} is not supported as a return type on DataFrame')
            return df
        else:
            return None



