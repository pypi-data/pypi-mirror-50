from haidatautils import mixed_list_to_int_list
from return_type import ReturnType
import logging
import sys

logging.disable(sys.maxsize)
logger = logging.getLogger(__name__)

def extract_returns(df, args_dict):
    int_list_to_apply_return = mixed_list_to_int_list(args_dict["COLS"], df.columns.values.tolist())
    return_type = ReturnType.from_string(args_dict.get("RETURN_TYPE", "LOG_RETURN"))
    return return_type(df, df.columns.values[int_list_to_apply_return].tolist())
