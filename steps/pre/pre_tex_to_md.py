from pylatexenc import latexwalker, latex2text, macrospec
import os
import logging

def check_latex2text_errors(latex_content):
    lw_context_db = latexwalker.get_default_latex_context_db()
    l2t_context_db = latex2text.get_default_latex_context_db()

    try:
        lw_obj = latexwalker.LatexWalker(latex_content, latex_context=lw_context_db)
        nodelist, pos, length = lw_obj.get_latex_nodes()
        l2t_obj = latex2text.LatexNodes2Text(latex_context=l2t_context_db, math_mode='with-delimiters')
        l2t_obj.nodelist_to_text(nodelist)
        logging.info("latex2text conversion successful.")
        return 0
    except Exception as e:
        logging.error(f"latex2text conversion failed with error: {e}")
        return 1
def pre_tex_to_md(input_path):
    with open(os.path.join(input_path, 'main.tex'), 'r') as file:
        latex_content = file.read()

    # Check for latex2text errors without writing to a file
    return check_latex2text_errors(latex_content)
