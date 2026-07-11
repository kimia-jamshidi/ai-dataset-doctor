import pandas as pd



DATETIME_THRESHOLD = 0.7

def load_dataset(uploaded_file):
    df = pd.read_csv(uploaded_file)
    object_columns = df.select_dtypes(include=["object"]).columns
    for column in object_columns:
        converted = pd.to_datetime(
            df[column],
            errors='coerce',
            
            )
        success_rate = converted.notna().mean()
        if  success_rate >= DATETIME_THRESHOLD:
            df[column] = converted
    return df