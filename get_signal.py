import numpy
numpy.NaN = numpy.nan  # Patch before pandas_ta tries to use it
import pandas_ta as ta
import pandas as pd
from talipp.indicators import EMA,McGinleyDynamic
import toml
import datetime as dt
import os
def get_sig(data):
    data['main_s'] = numpy.where(((data['pcr'] > data['pcr_sma_10'])), "Y", "N")
    conditions = [
        ((data['main_s'] == "Y") & (data['main_s'].shift(+1) == "N")),
        ((data['main_s'] == "N") & (data['main_s'].shift(+1) == "Y"))
    ]
    choices = ["BUY", "SELL"]
    data['pcr_sig'] = numpy.select(conditions, choices, "NA")
    return data