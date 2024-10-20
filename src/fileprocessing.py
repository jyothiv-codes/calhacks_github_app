from fpdf import FPDF
import re


class FileProcessing:

    def __init__(self, input_file):
        self.input_file=f'{input_file}.txt'
        self.inter_file=f'{input_file}_cleaned.txt'
        self.pdf_file =f'{input_file}.pdf'
        self.pdf = FPDF()

    def clean_conversation_file(self):

        with open(self.input_file, 'r') as file:
            content = file.read()  # Read the entire content of the file

        cleaned_content = re.sub(r"'data':\s*'[^']*'", '', content)
        cleaned_content = re.sub(r",\s*}", '}', cleaned_content)

        with open(self.inter_file, 'w') as file:
            file.write(cleaned_content)  # Write the modified content to a new file
        print(f"Cleaned content saved to {self.inter_file}")

        # with open(self.input_file, 'w') as file:
        #     pass

    def txt_to_pdf(self):
        
        self.pdf.add_page()

        # Set the same font for the main content
        # self.pdf.set_font("ArialUnicode", "", 12)
        self.pdf.set_font("Arial", size = 12)

        # Read the .txt file and add its content to the PDF
        with open(self.inter_file, 'r', encoding='utf-8') as file:
            for line in file:
                self.pdf.multi_cell(0, 10, line)

        # Save the PDF
        self.pdf.output(self.pdf_file)
        print(f"PDF saved at: {self.pdf_file}")

        # with open(self.inter_file, 'w') as file:
        #     pass


    def processFile(self):
        self.clean_conversation_file()
        self.txt_to_pdf()

        return self.pdf_file

# fp = FileProcessing('logs/emotion_logs')
# fp.processFile()