import pandas as pd
import os
from google import genai

def build_analysis_summary(overview, missing, duplicates,
                    health, outlier):
    
    summary = []


    summary.append("Dataset Overview")
    summary.append("----------------")
    summary.append(f"Rows: {overview['rows']}")
    summary.append(f"Columns: {overview['columns']}")
    memory_mb = overview["memory_usage"] / (1024 * 1024)
    summary.append(f"Memory Usage: {memory_mb:.2f} MB")
    summary.append("")

    summary.append("Data Types")
    summary.append("----------------")
    for data_type in overview['data_types']:
        info = overview["data_types"][data_type]
        if info["count"] > 0:
            summary.append(f"{data_type.title()} Feature: {info['count']}")
    summary.append("")

    
    summary.append("Data Types")
    summary.append("----------------")
    if missing["total_missing"] == 0:
        summary.append(f"No missing values detected.")
    else:
        summary.append(
            f"Overall Missing Percentage: {missing['missing_percentage']}%")
        summary.append("")

        column_summary = missing['column_summary']
        filtered_missing = column_summary[
            column_summary["Missing Count"] > 0]
        
        summary.append("Columns with Missing Values:")
        for _, row in filtered_missing.iterrows():
            summary.append(f"-{row['column']} ({row['Missing %']}%)")
        summary.append("")


    summary.append("Duplicates Analysis")
    summary.append("----------------")
    if  duplicates['total_duplicates'] == 0:
        summary.append(f"No duplicate rows detected.")
    else:
        summary.append(f"Duplicate Percentage: {duplicates['duplicate_percentage']}%")
    summary.append("")


    summary.append("Distribution Analysis")
    summary.append("---------------------")
    distribution_table = health['distribution_table']
    filtered_distribution = distribution_table[distribution_table['Distribution'] != "Normal"]
    if filtered_distribution.empty:
        summary.append("All numerical features have approximately normal distributions.")
    else:
        summary.append("Non-normal features:")
        for _, row in filtered_distribution.iterrows():
            summary.append(f"- {row['Column']}: {row['Distribution']}")
    summary.append("")


    summary.append("Variability Analysis")
    summary.append("--------------------")
    variability_table = health['variability_table']
    filtered_variability = variability_table[variability_table['Variability'] != "Not Applicable"] 
    if filtered_variability.empty:
        summary.append("No applicable variability analysis available.")
    else:
        for _, row in filtered_variability.iterrows():
            summary.append(f"- {row['Column']}: {row['Variability']}")
    summary.append("")



    summary.append("Balance Analysis")
    summary.append("--------------------")
    balance_table = health['balance_table']
    filtered_balance = balance_table[balance_table["Balance"] != "Balanced"]
    if filtered_balance.empty:
        summary.append("All categorical features are balanced.")
    else:
        summary.append("Imbalanced categorical features:")
        for _, row in filtered_balance.iterrows():
            summary.append(f"- {row['Column']}: {row['Balance']}")
    summary.append("")


    summary.append("Outlier Detection")
    summary.append("--------------------")
    outlier_table = outlier['outlier_table']
    filtered_outlier = outlier_table[outlier_table['Outliers'] > 0]
    if filtered_outlier.empty:
        summary.append("No outliers detected in numerical features.")
    else:
        summary.append("Features with outliers:")
        for _, row in filtered_outlier.iterrows():
            summary.append(f"- {row['Column']}: {row['Outlier (%)']}%")
    summary.append("")



    return "\n".join(summary)







def generate_ai_prompt(summary):

    prompt = f"""
You are an AI assistant specialized in dataset quality assessment.

Analyze the following dataset summary and identify all significant data quality issues based only on the provided information.

Rules:
- Use only the provided dataset summary.
- Do not make assumptions about missing information.
- Do not invent issues that are not present.
- Do not repeat information from the dataset summary.
- Focus on insights rather than restating statistics.
- Keep your response clear and concise.

Return your response in the following format:

Warnings:
- One warning for each detected issue.

Actionable Recommendations:
- One actionable recommendation for each detected issue.

Dataset Summary:

{summary}

"""
    return prompt



def call_llm(prompt):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "Gemini API key not found. Please add GEMINI_API_KEY to your .env file."
        )

    try:

        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text

    except RuntimeError:
        raise
    
    except Exception as e:
        raise RuntimeError(
            f"Failed to generate AI insights: {e}"
        )



def parse_ai_response(response_text):
    
    result = {
        "warnings": [],
        "recommendations": []
    }

    lines = response_text.splitlines()

    current_section = None
    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line == "Warnings:":
            current_section = "warnings"
            continue

        if line == "Actionable Recommendations:":
            current_section = "recommendations"
            continue

        if line.startswith("-"):
            line = line.lstrip("- ").strip()

            if current_section == "warnings":
                result["warnings"].append(line)

            elif current_section == "recommendations":
                result['recommendations'].append(line)


    return result


def generate_ai_insights(overview, missing, duplicates,
                    health, outlier):

    summary = build_analysis_summary(overview, missing, duplicates,
                    health, outlier)

    prompt = generate_ai_prompt(summary)

    response_text = call_llm(prompt)

    result = parse_ai_response(response_text)


    return result

