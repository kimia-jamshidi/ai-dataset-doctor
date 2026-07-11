import streamlit as st
from src.data_loader import load_dataset
from src.overview import get_dataset_overview
from src.missing_values import analyze_missing_values

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
    