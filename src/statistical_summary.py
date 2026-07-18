import pandas as pd
from numpy import number

def get_statistical_summary(df : pd.DataFrame):

    summary = {}

    numeric_df = df.select_dtypes(include=[number])

    summary['statistical_summary'] = numeric_df.describe()


    return summary