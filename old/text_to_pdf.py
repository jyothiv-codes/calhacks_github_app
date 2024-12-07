from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # Add Arial Unicode font during initialization
        self.add_font("ArialUnicode", "", "/Library/Fonts/Arial Unicode.ttf")

    def header(self):
        # Set the font for the header after it's added
        self.set_font("ArialUnicode", "", 12)
        self.cell(0, 10, "Text to PDF Conversion", 0, 1, "C")

def txt_to_pdf(txt_file, pdf_file):
    pdf = PDF()
    pdf.add_page()

    # Set the same font for the main content
    pdf.set_font("ArialUnicode", "", 12)

    # Read the .txt file and add its content to the PDF
    with open(txt_file, 'r', encoding='utf-8') as file:
        for line in file:
            pdf.multi_cell(0, 10, line)

    # Save the PDF
    pdf.output(pdf_file)
    print(f"PDF saved at: {pdf_file}")


txt_file = "audio_responses_cleaned.txt"  # Replace with your .txt file path
pdf_file = "audio_responses_cleaned.pdf"  # Desired .pdf file path
txt_to_pdf(txt_file, pdf_file)
