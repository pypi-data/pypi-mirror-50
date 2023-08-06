import logging

import pdfkit


def generate(html, pdf_output_path="out/out.pdf"):
    """
    Generate a pdf file in out/out.pdf in current folder where main script
    is executed.

    Use pdf_out_path to select final pdf generated destination.
    """
    logging.info("PDF generation...")

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
        logging.error("Something append: {}".format(e))
        raise
    else:
        logging.info("PDF generated at {}".format(pdf_output_path))
