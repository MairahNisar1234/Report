import streamlit as st
import pdfplumber
from fpdf import FPDF
from datetime import datetime
import tempfile
import os

# Function to extract text from input PDF
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

# Function to create the warrant PDF based on the selected type
def create_warrant_pdf(warrant_type, officer_name, complaint_person, complaint_address, offence,
                       witness_name, witness_description, arrest_date, issue_date, thing_specified=None, place_to_search=None):

    class WarrantPDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, f"{warrant_type} WARRANT", ln=True, align="C")
            self.ln(10)

        def body(self):
            self.set_font("Arial", "", 12)
            self.multi_cell(0, 10, f"To {officer_name},\n")
            self.ln(2)

            if warrant_type == "Warrant to bring up a witness":
                self.multi_cell(0, 10,
                    f"WHEREAS complaint has been made before me that {complaint_person} of {complaint_address} has (or is suspected to have) committed the offence of {offence}, "
                    f"and it appears likely that {witness_name}, {witness_description}, can give evidence concerning the said complaint; "
                    f"and whereas I have good and sufficient reason to believe that he will not attend as a witness on the hearing of the said complaint unless compelled to do so;")
                self.ln(5)
                self.multi_cell(0, 10,
                    f"This is to authorise and require you to arrest the said {witness_name} and on the {arrest_date} to bring him before this Court, "
                    "to be examined touching the offence complained of.")
                self.ln(5)

            elif warrant_type == "Warrant to search after information of a particular offence":
                self.multi_cell(0, 10,
                    f"WHEREAS information has been laid before me of the commission of the offence of {offence}, "
                    f"and it has been made to appear to me that the production of {thing_specified} is essential to the inquiry into the said offence.")
                self.ln(5)
                self.multi_cell(0, 10,
                    f"This is to authorize and require you to search for the said {thing_specified} in the {place_to_search} and, if found, to produce the same forthwith before this Court;")
                self.ln(5)
                self.multi_cell(0, 10,
                    "Returning this warrant, with an endorsement certifying what you have done under it, immediately upon its execution.")
                self.ln(5)

            elif warrant_type == "Warrant to search suspected Place of Deposit":
                self.multi_cell(0, 10,
                    f"WHEREAS information has been laid before me, and I believe that the {place_to_search} is used for the deposit (or sale) of stolen property;")
                self.ln(5)
                self.multi_cell(0, 10,
                    "This is to authorize and require you to enter the said house or place, use reasonable force if needed, and search every part of it. "
                    "Seize and bring any relevant property or documents before the Court.")
                self.ln(5)
                self.multi_cell(0, 10,
                    "Return this warrant with an endorsement certifying what was done under it.")
                self.ln(5)

            self.multi_cell(0, 10,
                f"Given under my hand and the seal of the Court, the {issue_date}, 20{datetime.now().year % 100:02d}.")
            self.ln(15)
            self.cell(0, 10, "(Seal)", ln=True)
            self.cell(0, 10, "(Signature)", ln=True)

    # Generate PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf = WarrantPDF()
        pdf.add_page()
        pdf.body()
        pdf.output(tmp.name)
        return tmp.name

# Streamlit app layout
def main():
    st.title("Petition Generator")

    uploaded_pdf = st.file_uploader("Upload PDF Case File", type="pdf")
    if uploaded_pdf is not None:
        text = extract_text_from_pdf(uploaded_pdf)
        st.text_area("Extracted Text", text, height=200)

    warrant_type = st.selectbox("Select Warrant Type", [
        "Warrant to bring up a witness",
        "Warrant to search after information of a particular offence",
        "Warrant to search suspected Place of Deposit"
    ])

    officer_name = st.text_input("Officer's Name and Designation")
    complaint_person = st.text_input("Person Making the Complaint")
    complaint_address = st.text_input("Complaint Address")
    offence = st.text_input("Offence")
    witness_name = st.text_input("Witness Name")
    witness_description = st.text_input("Witness Description")
    arrest_date = st.text_input("Arrest Date (e.g., 10th April)")
    issue_date = st.text_input("Issue Date (e.g., 7th April)")

    thing_specified = place_to_search = None
    if warrant_type == "Warrant to search after information of a particular offence":
        thing_specified = st.text_input("Thing to be Searched")
        place_to_search = st.text_input("Place to Search")
    elif warrant_type == "Warrant to search suspected Place of Deposit":
        place_to_search = st.text_input("Place to Search")

    if st.button("Generate Warrant"):
        pdf_path = create_warrant_pdf(
            warrant_type, officer_name, complaint_person, complaint_address, offence,
            witness_name, witness_description, arrest_date, issue_date,
            thing_specified, place_to_search
        )
        with open(pdf_path, "rb") as file:
            st.success("Petiton Generated!")
            st.download_button("Download Petition PDF", file.read(), file_name="warrant.pdf", mime="application/pdf")
        os.remove(pdf_path)  # clean up

if __name__ == "__main__":
    main()
