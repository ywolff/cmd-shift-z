from os.path import relpath, dirname

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import guess_lexer_for_filename


def code_to_html(input_code, filename, html_output_file_path, css_output_file_path):
    """
    Generate highlighted code as html and css files from a code file in a string.

    Args:
        input_code (str): text input (data).
        filename (str): the name of the file to process.
        html_output_file_path (str): .html output file path. If not provided, save html with same name as input file.
        css_output_file_path (str): .css output file path. If not provided, save css with same name as input file.
    """
    html_formatter = HtmlFormatter(
        style='monokai',
        full=True,
        cssfile=relpath(css_output_file_path, dirname(html_output_file_path))
    )

    lexer = guess_lexer_for_filename(filename, input_code)

    with open(html_output_file_path, 'w+') as html_file:
        highlight(input_code, lexer, html_formatter, html_file)
