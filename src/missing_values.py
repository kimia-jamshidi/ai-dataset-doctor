import pandas as pd


def analyze_missing_values(df: pd.DataFrame):

    missing = {}

    total_missing = int(df.isna().sum().sum())
    
    total_rows = df.shape[0]
    total_columns = df.shape[1]
    total_cells = total_rows * total_columns
    
    missing_percentage = (total_missing / total_cells) * 100
    
    affected_columns = int((df.isna().sum() > 0).sum())


    column_summary = df.isna().sum().to_frame(name="Missing Count")
    column_summary = column_summary.reset_index()
    column_summary = column_summary.rename(
        columns = {"index" : "column"}
    )

    column_summary['Missing %'] = (column_summary["Missing Count"] / df.shape[0]) * 100
    column_summary['Missing %'] = column_summary['Missing %'].round(2)

    column_summary = column_summary.sort_values(
        by="Missing Count",
        ascending=False
    )
    column_summary = column_summary[
        column_summary['Missing Count'] > 0
    ].reset_index(drop=True)



    missing["total_missing"] = total_missing
    missing["missing_percentage"] = missing_percentage
    missing["affected_columns"] = affected_columns
    missing['column_summary'] = column_summary


    return missing