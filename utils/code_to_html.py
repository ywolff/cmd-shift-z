from os.path import splitext, relpath, dirname

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import guess_lexer_for_filename


def code_to_html(input_file_path, html_output_file_path=None, css_output_file_path=None):
    """
    Generate highlighted code as html and css files from a code file.

    Args:
        input_file_path (str): text input file path
        html_output_file_path (str): .html output file path. If not provided, save html with same name as input file.
        css_output_file_path (str): .css output file path. If not provided, save css with same name as input file.
    """
    input_file_path_without_ext, _ = splitext(input_file_path)
    html_output_file_path = html_output_file_path or f'{input_file_path_without_ext}.html'
    css_output_file_path = css_output_file_path or f'{input_file_path_without_ext}.css'

    with open(input_file_path, 'r') as input_file:
        input_code = input_file.read()

    html_formatter = HtmlFormatter(
        style='monokai',
        full=True,
        cssfile=relpath(css_output_file_path, dirname(html_output_file_path))
    )
    lexer = guess_lexer_for_filename(input_file_path, input_code)

    with open(html_output_file_path, 'w+') as html_file:
        highlight(input_code, lexer, html_formatter, html_file)
