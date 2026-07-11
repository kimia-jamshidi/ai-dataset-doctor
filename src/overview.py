import pandas as pd

def get_dataset_overview(df: pd.DataFrame):
    overview = {}

    overview['rows'] = df.shape[0]
    overview['columns'] = df.shape[1]
    overview['memory_usage'] = int(df.memory_usage(deep=True).sum())
    
    numeric_df = df.select_dtypes(include=['number'])
    categorical_df = df.select_dtypes(include=["object", "string", "category"])
    boolean_df = df.select_dtypes(include=['bool', 'boolean'])
    datetime_df = df.select_dtypes(include=['datetime', 'datetimetz'])
    overview['data_types'] = {
        'numeric': {
            'count' : len(numeric_df.columns),
            'columns' : list(numeric_df.columns)
        },
        'categorical': {
            "count": len(categorical_df.columns),
            "columns": list(categorical_df.columns)
        },
        'boolean' : {
            "count": len(boolean_df.columns),
            "columns": list(boolean_df.columns)
        },
        'datetime' : {
            "count": len(datetime_df.columns),
            "columns": list(datetime_df.columns)
        }
    }





    return overview