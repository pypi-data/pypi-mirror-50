import os.path as path
import codecs
import logging

import jinja2
from jinja2.exceptions import TemplateSyntaxError

import resumejson_converter.filters as filters


def generate(resume, template, out_path=None):
    """
    Return html version of a JSON resume based on a template.

    `resume` is a JsonObject from resumejson_converter.utils.json.
    `template` is the path of the template to use.
    `out_path` is the output path of html generate. By default the html is
    not writen in a file.
    """
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
            logging.error("File not found: '{}'!"
                          .format(template))
            raise
        html = template.render(dict(resume=resume))
    except TemplateSyntaxError as e:
        logging.error("Syntax error in template file '{}' line {}: {}"
                      .format(e.name, e.lineno, e.message))
        raise
    else:
        logging.info("HTML generation done.")
        if out_path:
            try:
                file = codecs.open(out_path, "w", "utf-8-sig")
                file.write(html)
                file.close
            except IOError:
                logging.error("Permission error when writing html file!")
                raise
        return html
