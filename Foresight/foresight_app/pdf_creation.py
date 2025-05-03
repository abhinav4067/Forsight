from fpdf import FPDF

class ApplicationFormPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "FIHM - APPLICATION FORM", ln=True, align="C")
        self.ln(10)

    def body(self):
        self.set_font("Arial", "", 12)
        lines = [
            "---------------------------------------------------------",
            "Full Name: ____________________________________________",
            "",
            "Email Address: ________________________________________",
            "",
            "Phone Number: _________________________________________",
            "",
            "Educational Qualification: _____________________________",
            "",
            "Course Applying For: [ ] Hotel Management",
            "",
            "Permanent Address:",
            "_______________________________________________________",
            "_______________________________________________________",
            "",
            "Signature: _____________________      Date: _____________",
            "---------------------------------------------------------",
            "Instructions:",
            "- Please fill this form clearly with a blue or black pen.",
            "- Attach required documents (Copy of +2 mark sheet, ID proof).",
            "- Submit at FIHM office or send to our official address.",
        ]
        
        for line in lines:
            self.cell(0, 10, line, ln=True)

pdf = ApplicationFormPDF()
pdf.add_page()
pdf.body()
pdf.output("D:/Forsight/Foresight/foresight_app/static/forms/FIHM_Application_Form.pdf")
