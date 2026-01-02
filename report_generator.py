from fpdf import FPDF
import io
import datetime

def generate_malaria_pdf(df, kpis, charts):
    pdf = FPDF()
    pdf.add_page()
    
    # 1. Header
    pdf.set_font("helvetica", "B", 24)
    pdf.cell(0, 20, "Malaria Surveillance Report", ln=True, align="C")
    
    pdf.set_font("helvetica", "I", 10)
    pdf.cell(0, 10, f"Generated on: {datetime.date.today().strftime('%B %d, %Y')}", ln=True, align="C")
    pdf.ln(10)

    # 2. Executive Summary (KPIs)
    pdf.set_font("helvetica", "B", 16)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 12, "  Executive Summary", ln=True, fill=True)
    pdf.ln(5)

    pdf.set_font("helvetica", "", 12)
    for label, val in kpis:
        pdf.cell(50, 10, f"{label}:", border=0)
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, f"{val}", ln=True)
        pdf.set_font("helvetica", "", 12)
    
    pdf.ln(10)

    # 3. Visuals (Charts to Images)
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 12, "  Surveillance Insights", ln=True, fill=True)
    pdf.ln(5)

    # Process each chart provided
    for title, fig in charts.items():
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, f"Analysis: {title}", ln=True)
        
        # Convert Plotly fig to image bytes
        img_bytes = fig.to_image(format="png", width=800, height=450, scale=2)
        img_stream = io.BytesIO(img_bytes)
        
        # Add to PDF
        pdf.image(img_stream, w=170) 
        pdf.ln(10)

    # Return the PDF as bytes
    return pdf.output()