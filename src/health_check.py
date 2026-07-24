import pandas as pd
from pandas.api.types import is_numeric_dtype
from numpy import number

HIGH_CARDINALITY_THRESHOLD = 20

def analyze_dataset_check(df: pd.DataFrame):

    health = {}

    numeric_df = df.select_dtypes(include=[number])
    skew_values = numeric_df.skew()

    distribution_table = []
    for column, value in skew_values.items():

        if -0.5 <= value <= 0.5 :
            distribution = 'Normal'
        elif 0.5 < value <=1:
            distribution = "Moderately Right Skewed"
        elif value > 1:
            distribution = "Highly Right Skewed"
        elif  -1 <= value < -0.5:
            distribution = "Moderately Left Skewed"
        elif value < -1 :
            distribution = "Highly Left Skewed"

        distribution_table.append({
        "Column": column,
        "Skew": round(value, 2),
        "Distribution": distribution
        })

    distribution_table = pd.DataFrame(distribution_table)



    variability_table = []
    for column in numeric_df.columns:

        mean_value = numeric_df[column].mean()
        std_value = numeric_df[column].std()

        if mean_value == 0 :
            cv = None
            variability = "Not Applicable" 
        else:
            cv = round(std_value / mean_value, 2)
            
            if cv < 0.15 :
                variability = "Low"
            elif 0.15 <= cv <= 0.30 :
                variability = "Moderate"
            elif cv > 0.30 :
                variability = "High"

        variability_table.append({
            "Column" : column,
            "CV" : cv,
            "Variability" : variability
        })

    variability_table = pd.DataFrame(variability_table)


    categorical_df = df.select_dtypes(include=['object', 'string', 'category'])
    
    balance_table = []
    for column in categorical_df.columns:

        unique_classes = categorical_df[column].nunique()
        if unique_classes > HIGH_CARDINALITY_THRESHOLD:
            largest_class_name = "N/A"
            largest_class = "N/A"
            balance = "High Cardinality"
            
        else:
            largest_class = (
                categorical_df[column].value_counts(normalize=True).max()
            ) * 100
            largest_class = round(largest_class, 2)

            
            counts = categorical_df[column].value_counts()
            largest_class_name = counts.idxmax()

            if largest_class <= 60:
                balance = "Balanced"

            elif 60 < largest_class <= 80:
                balance = "Moderately Imbalanced"

            else:
                balance = "Highly Imbalanced"

   
        balance_table.append({
            'Column' : column,
            'Unique Classes' :unique_classes,
            'Largest Class' : largest_class_name,
            'Largest Class (%)' : largest_class,
            'Balance' : balance
            })

    balance_table = pd.DataFrame(balance_table)




    health["distribution_table"] = distribution_table
    health['variability_table'] = variability_table
    health['balance_table'] = balance_table

    return health
