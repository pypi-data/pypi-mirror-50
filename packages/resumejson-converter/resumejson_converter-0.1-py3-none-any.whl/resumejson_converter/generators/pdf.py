import sys
import logging

import pdfkit


def generate(html):
    logging.info("PDF generation...")

    pdf_output_path = "out/out.pdf"

    import os
    if not os.path.exists("out"):
        os.makedirs("out", exist_ok=True)

    try:
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        options = {
            'quiet': '',
            'page-size': 'A4',
            'margin-top': '0in',
            'margin-right': '0in',
            'margin-bottom': '0in',
            'margin-left': '0in',
            'encoding': "UTF-8",
        }
        pdfkit.from_string(
                        html,
                        pdf_output_path,
                        configuration=config,
                        options=options)
    except (IOError, OSError) as e:
        logging.exception("Something append: {}".format(e))
    else:
        logging.info("PDF generated at {}".format(pdf_output_path))
