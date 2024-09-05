from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa


def generate_pdf_from_html(context,template_name):
    template = get_template(template_name)
    html_string = template.render(context)
    # Create a BytesIO buffer to receive the PDF data
    result = BytesIO()
    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html_string, dest=result)
    # Get the PDF data from the buffer
    pdf = result.getvalue()
    result.close()

    return pdf