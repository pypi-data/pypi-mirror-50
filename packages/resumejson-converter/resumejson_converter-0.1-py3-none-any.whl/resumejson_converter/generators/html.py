import os.path as path
import sys
import codecs
import logging

import jinja2

import resumejson_converter.filters as filters


def generate(resume, template, out_path):
    try:
        logging.info("HTML generation...")
        templates_path = path.dirname(template)
        template_name = path.basename(template)
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_path),
            autoescape=jinja2.select_autoescape(['hmtl', 'xml']),
        )
        env.filters['dateedit'] = filters.dateedit
        env.filters['datediff'] = filters.datediff
        env.filters['birthday'] = filters.birthday
        env.filters['clean'] = filters.clean
        try:
            template = env.get_template(template_name)
        except jinja2.exceptions.TemplateNotFound:
            logging.exception("File not found: '{}'!"
                                .format(template))
            sys.exit(1)
        html = template.render(dict(resume=resume))
    except jinja2.exceptions.TemplateSyntaxError as e:
        logging.exception("Syntax error in template file '{}' line {}: {}"
                          .format(e.name, e.lineno, e.message))
        sys.exit(1)
    else:
        logging.info("HTML generation done.")
        if out_path:
            file = codecs.open(out_path, "w", "utf-8-sig")
            file.write(html)
            file.close
        return html
