import streamlit as st
from src.data_loader import load_dataset
from src.overview import get_dataset_overview
from src.missing_values import analyze_missing_values
from src.duplicates import analyze_duplicates
from src.statistical_summary import get_statistical_summary
from src.health_check import analyze_dataset_check
from src.outlier_detection import analyze_outliers

st.title('AI Dataset Doctor')

st.caption("Diagnose your dataset before training your model.")
st.divider()

uploaded_file = st.file_uploader(
    label="Upload your CSV dataset for analysis",
    type=['csv']
)
st.divider()

if uploaded_file is not None:
    st.success('Dataset uploaded successfully! Ready for analysis.')
    st.subheader('📊 Dataset Overview')
    df = load_dataset(uploaded_file)
    # st.dataframe(df)
    overview = get_dataset_overview(df)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="Rows",
        value=overview['rows']
    )
    col2.metric(
    label="Columns",
    value=overview["columns"]
    )
    memory_mb = overview['memory_usage'] / (1024 * 1024)
    memory_txt = f"{memory_mb: .2f} MB"
    col3.metric(
        label="Memory",
        value=memory_txt
    )



    st.divider()



    st.subheader('👀 Dataset Preview')
    st.dataframe(df.head(5))





    st.divider()




    st.subheader("📂 Data Type Summary")
    col1, col2 = st.columns(2)
    col1.metric(
        label= "Numeric",
        value= overview['data_types']['numeric']['count']
    )
    col2.metric(
        label= "Categorical",
        value= overview['data_types']['categorical']['count']
    )
    with col1:
        with st.expander("📋 Numeric Columns"):
            for column in overview["data_types"]["numeric"]["columns"]:
                st.markdown(f"- {column}")
    with col2:
        with st.expander("📋 Categorical Columns"):
            for column in overview["data_types"]["categorical"]["columns"]:
                st.markdown(f"- {column}")
    
    
    col1, col2 = st.columns(2)
    col1.metric(
        label= "Boolean",
        value= overview['data_types']['boolean']['count']
    )
    col2.metric(
        label= "Datetime",
        value= overview['data_types']['datetime']['count']
    )
    with col1:
        with st.expander("📋 Boolean Columns"):
            if overview["data_types"]["boolean"]["columns"]:
                for column in overview["data_types"]["boolean"]["columns"]:
                    st.markdown(f"- {column}")
            else:
                st.caption("No boolean columns found.")
           
    with col2:
        with st.expander("📋 Datetime Columns"):
            if overview["data_types"]["datetime"]["columns"]:
                for column in overview["data_types"]["datetime"]["columns"]:
                    st.markdown(f"- {column}")
            else:
                st.caption("No datetime columns found.")
            


    
    st.divider()



    st.subheader("🧩 Missing Values")
    missing = analyze_missing_values(df)

    col1,col2,col3 = st.columns(3)
    col1.metric(
        label='Total Missing',
        value=missing['total_missing']
    )
    col2.metric(
        label='Affected Columns',
        value = missing['affected_columns']
    )

    col3.metric(
        label='Missing %',
        value=f"{missing['missing_percentage']: .2f} %"
    )

    if missing['affected_columns'] == 0 :
        st.success("✅ No missing values found. Your dataset looks clean!")
    else:
        st.markdown("#### Missing Columns")
        st.dataframe(missing['column_summary'])





    st.divider()





    st.subheader("📑 Duplicate Rows")
    duplicates = analyze_duplicates(df)

    col1, col2 = st.columns(2)
    col1.metric(
        label="Total Duplicates",
        value = duplicates['total_duplicates']
    )
    col2.metric(
        label='Duplicate %',
        value= f" {duplicates['duplicate_percentage'] : .2f} %"
    )


    if duplicates['has_duplicates'] == False :
        st.success("✅ No duplicate rows found in the dataset.")
    else:
        st.markdown("#### Sample Duplicate Rows")
        st.dataframe(duplicates['duplicate_rows'].head(100))

    st.caption(
    f"Showing the first 100 duplicate rows out of {len(duplicates['duplicate_rows']):,}."
    )


    st.divider()


    st.subheader("📈 Statistical Summary")
    summary = get_statistical_summary(df)

    if summary["statistical_summary"].empty:
        st.info("ℹ️ No numeric columns are available, so no statistical summary can be generated.")
    else:
       st.dataframe(summary["statistical_summary"].T.round(2))





    st.divider()

    st.subheader("🩺 Dataset Health Check")
    st.caption("Evaluate the statistical health of your dataset by analyzing feature distributions, variability, and category balance.")
    health = analyze_dataset_check(df)
    distribution_table = health['distribution_table']

    st.subheader("📐 Distribution Analysis")
    if health['distribution_table'] is None :
        st.info("No numerical columns found.")
    else:
        st.dataframe(health['distribution_table'])
    st.info("This table shows the distribution shape of each numerical feature.")

    st.divider()

    st.subheader("📉 Variability Analysis")
    if health["variability_table"] is None:
        st.info("No numerical columns found.")
    else:
        st.dataframe(health['variability_table'])
    st.info("The coefficient of variation (CV) measures the relative variability of each numerical feature.")

    st.divider()

    st.subheader("⚖️ Balance Analysis")
    if health["balance_table"] is None:
        st.info("No categorical columns found.")
    else:
        st.dataframe(health['balance_table'])
    st.info("This analysis evaluates the distribution of categorical features by identifying class imbalance and detecting high-cardinality columns.")



    st.divider()


    st.subheader("🚨 Outlier Detection")
    outlier = analyze_outliers(df, distribution_table)
    outlier_table = outlier['outlier_table']


    total_outliers = outlier_table["Outliers"].sum()
    columns_with_outliers = (outlier_table["Outliers"] > 0).sum()

    col1, col2 = st.columns(2)
    col1.metric(
        label="Total Outliers",
        value=total_outliers
    )
    col2.metric(
        label="Columns with Outliers",
        value=columns_with_outliers
    )

    if outlier_table.empty:
        st.info("No numerical features available for outlier detection.")
    else:
        with st.expander("📋 View Outlier Details"):
            st.dataframe(outlier_table, hide_index=True)
            st.info("This table summarizes outlier detection results for each numerical feature.")