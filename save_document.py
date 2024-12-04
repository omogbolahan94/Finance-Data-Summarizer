from fpdf import FPDF
import streamlit as st


def save_summary(summary):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add the content to the PDF
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    # Ensure proper handling of Unicode
    for line in summary.split("\n"):
        pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))

    pdf_file = "summary.pdf"
    pdf.output(pdf_file)

    with open(pdf_file, "rb") as file:
        st.download_button("Download PDF", file, file_name="financial_summary.pdf", mime="application/pdf")



