import fpdf
import datetime
import logging
from flask import make_response

def render_table_header(pdf,line_height,col_width,header_data):
    pdf.set_fill_color(117, 175, 235)
    pdf.set_text_color(255,255,255)  
    pdf.set_font(style="B")  # enabling bold text
    for col_name in header_data:
        pdf.cell(col_width, line_height, col_name, border=1,fill=True)
    pdf.ln(line_height)
    pdf.set_font(style="")  # disabling bold text
    pdf.set_text_color(0,0,0) 


def generate_pdf(file_path,file_name,logo_path,header_data,body_data):
    logging.info('ReportGeneratingServices - generate_pdf() CALLED')

    # file  initiation
    pdf = fpdf.FPDF()
    pdf.add_page()
    line_height = pdf.font_size * 2
    col_width = pdf.epw / 6  # distribute content evenly


    # file header initiation
    pdf.set_font("Times", size=8)
    pdf.image(logo_path, x = None, y = None, w = 60, h = 20, type = '', link = '')
    pdf.write(5,"EMPLOYEE ANALYTICS REPORT")
    pdf.ln()
    pdf.write(5,"GENERATED AT: " + str(datetime.datetime.now().strftime("%Y-%m-%d")))
    pdf.ln()
    # pdf.ln()
    pdf.ln()
    pdf.set_font("Times", size=9)


    render_table_header(pdf,line_height,col_width,header_data)

    for row in body_data:

        # this will check page has end or not. id ends re prints the header
        if pdf.will_page_break(line_height):
            render_table_header(pdf,line_height,col_width,header_data)

        # body data printing    
        for data in row:
            pdf.cell(col_width, line_height, str(data), border=1)
        pdf.ln(line_height)

    logging.info('ReportGeneratingServices - generate_pdf() COMPLETED')
    pdf.output(str(file_path)+str(file_name))
