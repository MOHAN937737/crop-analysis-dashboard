import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

# ======================================
# Page Configuration
# ======================================
st.set_page_config(
    page_title="Agriculture Analytics Dashboard",
    page_icon="🌾",
    layout="wide"
)

# ======================================
# Load Dataset
# ======================================
df = pd.read_csv("crop_production.csv")

# ======================================
# Header
# ======================================
st.title("🌾 Agriculture Analytics Dashboard")
st.markdown("### Smart Crop Production Analysis")

# ======================================
# KPI Metrics
# ======================================
col1, col2, col3 = st.columns(3)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", int(df.isnull().sum().sum()))

# ======================================
# Tabs
# ======================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 Dataset",
    "📊 Visualizations",
    "📈 Statistics",
    "🌾 Crop Analysis",
    "🔍 Data Quality",
    "📌 Insights"
])

# ======================================
# DATASET TAB
# ======================================
with tab1:

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Shape")
    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")

    st.subheader("Dataset Information")

    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    st.subheader("Missing Values Before Cleaning")
    st.dataframe(df.isnull().sum().to_frame("Null Count"))

    rows_before = len(df)

    # Data Cleaning
    df_clean = df.copy()

    for col in df_clean.select_dtypes(include="object"):
        df_clean[col] = df_clean[col].fillna(
            df_clean[col].mode()[0]
        )

    for col in df_clean.select_dtypes(include="number"):
        df_clean[col] = df_clean[col].fillna(
            df_clean[col].median()
        )

    rows_after = len(df_clean)

    st.subheader("Cleaning Summary")

    st.write(f"Rows Before Cleaning: {rows_before}")
    st.write(f"Rows After Cleaning: {rows_after}")
    st.write(f"Rows Removed: {rows_before - rows_after}")

    remaining_nulls = df_clean.isnull().sum()
    remaining_nulls = remaining_nulls[remaining_nulls > 0]

    if len(remaining_nulls) > 0:
        st.subheader("Remaining Null Values")
        st.dataframe(remaining_nulls.to_frame("Null Count"))
    else:
        st.success("✅ No Null Values Found")

# ======================================
# VISUALIZATION TAB
# ======================================
with tab2:

    st.subheader("Histogram")

    numeric_cols = df.select_dtypes(include="number").columns

    hist_col = st.selectbox(
        "Select Column for Histogram",
        numeric_cols,
        key="histogram"
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    sns.histplot(
        df[hist_col],
        kde=True,
        color="green",
        ax=ax
    )

    ax.set_title(f"{hist_col} Distribution")

    st.pyplot(fig)

    st.subheader("🔥 Correlation Heatmap")

    numeric_df = df.select_dtypes(include="number")

    fig2, ax2 = plt.subplots(figsize=(10, 6))

    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="coolwarm",
        ax=ax2
    )

    st.pyplot(fig2)

# ======================================
# STATISTICS TAB
# ======================================
with tab3:

    st.header("📈 Statistical Analysis")

    numeric_df = df.select_dtypes(include="number")

    # Boxplot
    box_col = st.selectbox(
        "Select Column for Boxplot",
        numeric_df.columns,
        key="boxplot"
    )

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    sns.boxplot(y=df[box_col], ax=ax3)

    st.pyplot(fig3)

    # Scatter Plot
    x_col = st.selectbox(
        "Select X Axis",
        numeric_df.columns,
        key="x_axis"
    )

    y_col = st.selectbox(
        "Select Y Axis",
        numeric_df.columns,
        key="y_axis"
    )

    fig4, ax4 = plt.subplots(figsize=(8, 5))

    sns.scatterplot(
        x=df[x_col],
        y=df[y_col],
        ax=ax4
    )

    st.pyplot(fig4)

    st.subheader("Descriptive Statistics")
    st.dataframe(df.describe())

# ======================================
# CROP ANALYSIS TAB
# ======================================
with tab4:

    st.header("🌾 Crop Analysis")

    categorical_cols = df.select_dtypes(
        include="object"
    ).columns

    if len(categorical_cols) > 0:

        crop_col = st.selectbox(
            "Select Category Column",
            categorical_cols,
            key="crop_analysis"
        )

        st.subheader("Category Distribution")

        st.bar_chart(
            df[crop_col].value_counts()
        )

# ======================================
# DATA QUALITY TAB
# ======================================
with tab5:

    st.header("🔍 Data Quality Report")

    quality_df = pd.DataFrame({
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum(),
        "Unique Values": df.nunique()
    })

    st.dataframe(quality_df)

    st.metric(
        "Duplicate Rows",
        int(df.duplicated().sum())
    )

# ======================================
# INSIGHTS TAB
# ======================================
with tab6:

    st.header("📌 Business Insights")

    st.info("""
    • Rice is one of the dominant crops.

    • Production varies significantly across seasons.

    • Area has a positive impact on production.

    • Some districts contribute more to total production.

    • Data-driven planning improves productivity.
    """)

    st.subheader("Recommendations")

    st.success("""
    ✅ Focus on high-yield crops.

    ✅ Monitor seasonal trends.

    ✅ Optimize land utilization.

    ✅ Improve resource allocation.

    ✅ Use predictive analytics for crop planning.
    """)

    st.subheader("Project Conclusion")

    st.write("""
    Agricultural production varies across crops,
    districts and seasons. This dashboard helps
    identify trends, correlations and opportunities
    for improving agricultural productivity.
    """)
    