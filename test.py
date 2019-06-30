from fpdf import FPDF
 
pdf = FPDF(orientation='P', unit='in', format='A4')
pdf.add_page()
pdf.set_margins(1, 1, 1)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Welcome to Python!", ln=1, align="C")
pdf.output("simple_demo.pdf")