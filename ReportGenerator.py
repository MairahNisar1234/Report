import streamlit as st
import pdfplumber
from fpdf import FPDF
from datetime import datetime

# Function to extract text from input PDF
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

# Function to create the warrant PDF based on the selected type
def create_warrant_pdf(warrant_type, officer_name, complaint_person, complaint_address, offence, witness_name, witness_description, arrest_date, issue_date, thing_specified=None, place_to_search=None):
    class WarrantPDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, f"{warrant_type} WARRANT", ln=True, align="C")
            self.ln(10)

        def body(self, officer_name, complaint_person, complaint_address, offence, witness_name, witness_description, arrest_date, issue_date, thing_specified, place_to_search):
            self.set_font("Arial", "", 12)

            # Common sections for all warrants
            self.multi_cell(0, 10, f"To {officer_name},\n")
            self.ln(2)

            if warrant_type == "Warrant to bring up a witness":
                self.multi_cell(0, 10, 
                    f"WHEREAS complaint has been made before me that {complaint_person} of {complaint_address} has (or is suspected to have) committed the offence of {offence}, "
                    f"and it appears likely that {witness_name}, {witness_description}, can give evidence concerning the said complaint; "
                    f"and whereas I have good and sufficient reason to believe that he will not attend as a witness on the hearing of the said complaint unless compelled to do so;"
                )
                self.ln(5)

                self.multi_cell(0, 10, 
                    f"This is to authorise and require you to arrest the said {witness_name} and on the {arrest_date} to bring him before this Court, "
                    "to be examined touching the offence complained of."
                )
                self.ln(5)

            elif warrant_type == "Warrant to search after information of a particular offence":
                self.multi_cell(0, 10, 
                    f"WHEREAS information has been laid (or complaint has been made) before me of the commission (or suspected commission) of the offence of {offence}, "
                    f"and it has been made to appear to me that the production of {thing_specified} is essential to the inquiry now being made (or about to be made) into the said offence or suspected offence;"
                )
                self.ln(5)

                self.multi_cell(0, 10, 
                    f"This is to authorize and require you to search for the said {thing_specified} in the {place_to_search} and, if found, to produce the same forthwith before this Court;"
                )
                self.ln(5)

                self.multi_cell(0, 10, 
                    "Returning this warrant, with an endorsement certifying what you have done under it, immediately upon its execution."
                )
                self.ln(5)

            elif warrant_type == "Warrant to search suspected Place of Deposit":
                self.multi_cell(0, 10, 
                    f"WHEREAS information has been laid before me, and on due inquiry thereupon had I have been led to believe that the {place_to_search} is used as a place for the deposit (or sale) of stolen property;"
                )
                self.ln(5)

                self.multi_cell(0, 10, 
                    "This is to authorize and require you to enter the said house (or other place) with such assistance as shall be required, and to use if necessary, reasonable force for that purpose, "
                    "and to search every part of the said house (or other place), and to seize and take possession of any property (or documents, or stamps, or seals, or coins or obscene objects, as the case may be)."
                )
                self.ln(5)

                self.multi_cell(0, 10, 
                    f"And forthwith to bring before this Court such of the said things as may be taken possession of, returning this warrant, with an endorsement certifying what you have done under it."
                )
                self.ln(5)

            self.multi_cell(0, 10, 
                f"Given under my hand and the seal of the Court, the {issue_date}, 20{datetime.now().year % 100:02d}."
            )
            self.ln(15)

            self.cell(0, 10, "(Seal)", ln=True)
            self.cell(0, 10, "(Signature)", ln=True)

    # Create PDF
    pdf = WarrantPDF()
    pdf.add_page()
    pdf.body(officer_name, complaint_person, complaint_address, offence, witness_name, witness_description, arrest_date, issue_date, thing_specified, place_to_search)
    output_filename = f"{warrant_type.replace(' ', '_').lower()}_warrant.pdf"
    pdf.output(output_filename)
    return output_filename

# Streamlit app layout
def main():
    st.title("Warrant Generator")

    # Upload PDF case file
    uploaded_pdf = st.file_uploader("Upload PDF Case File", type="pdf")
    if uploaded_pdf is not None:
        # Extract text from the PDF (for debugging purposes)
        text = extract_text_from_pdf(uploaded_pdf)
        st.text_area("Extracted Text", text, height=200)

    warrant_type = st.selectbox("Select Warrant Type", 
                                ["Warrant to bring up a witness", 
                                 "Warrant to search after information of a particular offence", 
                                 "Warrant to search suspected Place of Deposit"])

    officer_name = st.text_input("Enter the Officer's Name and Designation")
    complaint_person = st.text_input("Enter the Person Making the Complaint")
    complaint_address = st.text_input("Enter the Complaint Address")
    offence = st.text_input("Enter the Offence")
    witness_name = st.text_input("Enter the Witness Name")
    witness_description = st.text_input("Enter the Witness Description")
    arrest_date = st.text_input("Enter the Arrest Date (e.g., 10th April)")
    issue_date = st.text_input("Enter the Issue Date (e.g., 7th April)")

    if warrant_type == "Warrant to search after information of a particular offence":
        thing_specified = st.text_input("Enter the Thing to be Searched (e.g., stolen property)")
        place_to_search = st.text_input("Enter the Place to Search (e.g., specific address or location)")
    elif warrant_type == "Warrant to search suspected Place of Deposit":
        place_to_search = st.text_input("Enter the Place to Search (e.g., specific address or location)")

    if st.button("Generate Warrant"):
        if warrant_type == "Warrant to search after information of a particular offence":
            pdf_file = create_warrant_pdf(warrant_type, officer_name, complaint_person, complaint_address, offence, witness_name, witness_description, arrest_date, issue_date, thing_specified, place_to_search)
        elif warrant_type == "Warrant to search suspected Place of Deposit":
            pdf_file = create_warrant_pdf(warrant_type, officer_name, complaint_person, complaint_address, offence, witness_name, witness_description, arrest_date, issue_date, None, place_to_search)
        else:
            pdf_file = create_warrant_pdf(warrant_type, officer_name, complaint_person, complaint_address, offence, witness_name, witness_description, arrest_date, issue_date, None, None)
        
        st.success("Warrant PDF Generated!")
        st.download_button("Download Warrant PDF", pdf_file)

if __name__ == "__main__":
    main()
