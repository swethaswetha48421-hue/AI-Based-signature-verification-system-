from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

def generate_verification_report(result_data, output_path='reports/verification_report.pdf'):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    
    content = []
    
    title = Paragraph("<b>SIGNATURE VERIFICATION REPORT</b>", styles['Heading1'])
    content.append(title)
    content.append(Spacer(1, 20))
    
    details = [
        ['Date & Time:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ['Verification Result:', result_data['result']],
        ['Confidence Score:', f"{result_data['confidence']:.2f}%"],
        ['Image Path:', result_data['image_path']],
        ['User Name:', result_data.get('user_name', 'N/A')]
    ]
    
    table = Table(details, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    content.append(table)
    content.append(Spacer(1, 30))
    
    if result_data['result'] == 'Genuine':
        remark = Paragraph("<b>✓ This signature appears to be GENUINE.</b>", styles['Normal'])
    else:
        remark = Paragraph("<b>⚠ This signature appears to be FORGED. Please verify manually.</b>", styles['Normal'])
    
    content.append(remark)
    content.append(Spacer(1, 40))
    
    footer = Paragraph("_______________________<br/>System Administrator", styles['Normal'])
    content.append(footer)
    
    doc.build(content)
    print(f"✅ Report saved to {output_path}")
    return output_path
