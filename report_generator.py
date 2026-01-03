from fpdf import FPDF
import io
import datetime
import os

class MalariaPDF(FPDF):
    def header(self):
        # Logo - Look for a file named 'logo.png' in your folder
        if os.path.exists("logo.png"):
            self.image("logo.png", 10, 8, 25)
        
        self.set_font("helvetica", "B", 20)
        self.set_text_color(0, 102, 204) # Professional Blue
        self.cell(0, 10, "Malaria Surveillance Intelligence", ln=True, align="R")
        self.set_font("helvetica", "I", 10)
        self.set_text_color(100)
        self.cell(0, 10, f"Official Report | {datetime.date.today()}", ln=True, align="R")
        self.ln(10)

def generate_malaria_pdf(df, kpis, charts):
    pdf = MalariaPDF()
    pdf.add_page()
    
    # 1. Executive Summary Table
    pdf.set_font("helvetica", "B", 16)
    pdf.set_fill_color(230, 240, 255)
    pdf.cell(0, 12, "  1. Executive Summary", ln=True, fill=True)
    pdf.ln(5)

    pdf.set_font("helvetica", "", 12)
    for label, val in kpis:
        # Highlight 'Risk Level' in Red if it's High
        if label == "Regional Risk Status" and val == "High":
            pdf.set_text_color(200, 0, 0) # Red
        else:
            pdf.set_text_color(0) # Black
            
        pdf.cell(60, 10, f"{label}:", border="B")
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, f" {val}", ln=True, border="B")
        pdf.set_font("helvetica", "", 12)
    
    pdf.ln(10)

    # 2. Charts Section
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 12, "  2. Visual Analytics", ln=True, fill=True)
    pdf.ln(5)

    for title, fig in charts.items():
        pdf.set_font("helvetica", "B", 11)
        pdf.set_text_color(50)
        pdf.cell(0, 10, f">> {title}", ln=True)
        
        try:
            # Convert Plotly to Image bytes
            img_bytes = fig.to_image(format="png", width=800, height=450, scale=2)
            img_stream = io.BytesIO(img_bytes)
            pdf.image(img_stream, w=180) 
            pdf.ln(5)
        except Exception as e:
            pdf.set_font("helvetica", "I", 8)
            pdf.cell(0, 10, f"Note: Chart {title} could not be rendered in PDF.", ln=True)

    # CRITICAL FIX: Explicitly convert bytearray to bytes
    pdf_output = pdf.output()
    return bytes(pdf_output)