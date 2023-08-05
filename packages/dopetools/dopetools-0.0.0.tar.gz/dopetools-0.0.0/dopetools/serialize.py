from functools import singledispatch
import json
import pandas as pd

@singledispatch
def msg_serialization(val):
    """Used by default."""
    return json.JSONEncoder(val)


@msg_serialization.register(pd.DataFrame)
def df_serialization(val):
    """Used if *val* is an instance of pd.DataFrame()."""
    return val.to_json(orient='split', index=False)


def obj_hook(dict_in):
    dict_in['data_df'] = pd.read_json(dict_in['data_df'], orient='split')
    return dict_in


def jsonify(val):
    return json.dumps(val, default=msg_serialization)


def dejsonify(val):
    return json.loads(val, object_hook=obj_hook)

