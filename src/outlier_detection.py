import pandas as pd 
from numpy import number

def analyze_outliers(df: pd.DataFrame, distribution_table):
    outlier = {}

    numeric_df = df.select_dtypes(include=[number])

    outlier_table = []
    for column in numeric_df.columns:
        data = numeric_df[column]
        
        distribution = distribution_table.loc[
            distribution_table['Column'] == column,
            'Distribution'
        ].iloc[0]

        unique_classes = numeric_df[column].nunique()
        if unique_classes <=2:
            continue


        if distribution == 'Normal':
            
            method = "Z-Score"
            mean_value = data.mean()
            std_value = data.std()


            if std_value == 0:
                outlier_count = 0
                outlier_percentage = 0
            else:
                z_score = (data - mean_value) / std_value
                outlier_count = (z_score.abs() > 3).sum()
                outlier_percentage = round((outlier_count / len(data)) * 100, 2)
                

        else:
            method = "IQR"
            q1 = data.quantile(0.25)
            q3 = data.quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outlier_count = (
                (data < lower_bound) | (data> upper_bound)
            ).sum()

            outlier_percentage = round(
                (outlier_count / len(data)) * 100, 2)

        outlier_table.append({
            "Column": column,
            "Method": method,
            "Outliers": outlier_count,
            "Outlier (%)": outlier_percentage
        })



    outlier_table = pd.DataFrame(outlier_table)
    outlier['outlier_table'] = outlier_table


    return outlier