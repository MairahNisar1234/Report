import streamlit as st
from fpdf import FPDF
import os

# Function to create a simple TXT report
def generate_txt_report(content, txt_path):
    with open(txt_path, "w") as file:
        file.write(content)

# Function to convert TXT to PDF
def txt_to_pdf(txt_path, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    with open(txt_path, "r") as file:
        for line in file:
            pdf.multi_cell(0, 10, txt=line)

    pdf.output(pdf_path)

# Streamlit UI
st.title("Report Generator")

user_input = st.text_area("Enter the report content:", height=200)

if st.button("Generate Report"):
    if user_input.strip() == "":
        st.warning("Please enter some content.")
    else:
        os.makedirs("output", exist_ok=True)
        txt_path = "output/report.txt"
        pdf_path = "output/report.pdf"

        generate_txt_report(user_input, txt_path)
        txt_to_pdf(txt_path, pdf_path)

        st.success("Report generated successfully!")

        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF Report", f, file_name="report.pdf", mime="application/pdf")
