import pandas as pd


def analyze_duplicates(df: pd.DataFrame):
    
    duplicates = {}

    total_duplicates = int(df.duplicated(keep='first').sum())

    has_duplicates = total_duplicates > 0
    
    duplicate_percentage = (total_duplicates / df.shape[0]) * 100
    
    duplicate_rows = df[df.duplicated(keep=False)]



    duplicates['total_duplicates'] = total_duplicates
    duplicates['duplicate_percentage'] = duplicate_percentage
    duplicates['duplicate_rows'] = duplicate_rows
    duplicates['has_duplicates'] = has_duplicates

    return duplicates