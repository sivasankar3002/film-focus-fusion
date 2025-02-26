import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from fpdf import FPDF

# Title of the app
st.title("AI-Powered Data Analytics Tool")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    # Display raw data
    st.subheader("Raw Data")
    st.write(df)

    # Data Cleaning
    st.subheader("Data Cleaning")
    df = df.dropna()  # Drop missing values
    df = df.drop_duplicates()  # Remove duplicates
    st.write("Missing values and duplicates removed.")

    # Summary Statistics
    st.subheader("Summary Statistics")
    st.write(df.describe())

    # Data Visualization
    st.subheader("Data Visualization")
    fig, ax = plt.subplots()
    sns.histplot(df.iloc[:, 0], kde=True, ax=ax)  # Histogram of the first column
    st.pyplot(fig)

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    corr_matrix = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # Feature Engineering
    st.subheader("Feature Engineering")
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df.select_dtypes(include=[np.number]))
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(scaled_data)
    st.write("PCA-transformed data:")
    st.write(reduced_data)

    # Generate PDF Report
    def generate_pdf_report():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Data Analytics Report", ln=True, align="C")
        pdf.cell(200, 10, txt="Summary Statistics", ln=True)
        pdf.multi_cell(0, 10, txt=str(df.describe()))
        pdf.output("report.pdf")

    # Download Report
    st.subheader("Download Report")
    if st.button("Generate PDF Report"):
        generate_pdf_report()
        with open("report.pdf", "rb") as f:
            st.download_button("Download PDF", f, file_name="report.pdf")
