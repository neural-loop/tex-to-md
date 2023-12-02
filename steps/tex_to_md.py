from pylatexenc import latexwalker, latex2text, macrospec
import os
import logging

def add_macros_to_context(macro_db, textmacro_db, macro_replacements):
    macro_specs = [macrospec.MacroSpec(macro_name, "{") for macro_name in macro_replacements.keys()]
    macro_text_specs = [latex2text.MacroTextSpec(macro_name, simplify_repl=repl_func) for macro_name, repl_func in
                        macro_replacements.items()]

    macro_db.add_context_category('my-macros', prepend=True, macros=macro_specs)
    textmacro_db.add_context_category('my-macros', prepend=True, macros=macro_text_specs)


lw_context_db = latexwalker.get_default_latex_context_db()
l2t_context_db = latex2text.get_default_latex_context_db()

macro_replacements = {
    'section': lambda node, l2tobj: '## ' + l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]]) + '\n\n',
    'subsection': lambda node, l2tobj: '### ' + l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]])+ '\n\n',
    'spara': lambda node, l2tobj: '#### ' + l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]])+ "\n\n",
    'subsubsection': lambda node, l2tobj: '#### ' + l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]])+ '\n\n',
    'textbf': lambda node, l2tobj: '**' + l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]]) + '**',
    'textit': lambda node, l2tobj: '_' + l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]]) + '_',
    'texttt': lambda node, l2tobj: '_' + l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]]) + '_',
    # 'cite': lambda node, l2tobj: '',
    'emph': lambda node, l2tobj: '*' + l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]]) + '*',
    'underline': lambda node, l2tobj: '_' + l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]]) + '_',
    'bibliographystyle': lambda node, l2tobj: '',
    'newgeometry': lambda node, l2tobj: '',
}
add_macros_to_context(lw_context_db, l2t_context_db, macro_replacements)

# Add custom handler for 'abstract' environment
l2t_context_db.add_context_category(
    'my-environments',
    prepend=False,
    environments=[
        latex2text.EnvironmentTextSpec(
            'abstract',
            simplify_repl=lambda node, l2tobj: '> ' + l2tobj.nodelist_to_text(node.nodelist).strip()
        ),
    ],
)


def custom_latex_to_text(input_latex):
    lw_obj = latexwalker.LatexWalker(input_latex, latex_context=lw_context_db)
    nodelist, pos, length = lw_obj.get_latex_nodes()
    l2t_obj = latex2text.LatexNodes2Text(latex_context=l2t_context_db, math_mode='remove')
    # l2t_obj = latex2text.LatexNodes2Text(latex_context=l2t_context_db, math_mode='with-delimiters')
    return l2t_obj.nodelist_to_text(nodelist)


def tex_to_md(input_path, output_path):
    with open(input_path + '/main.tex', 'r') as file:
        latex_content = file.read()

    # Write the converted text to the output file
    # create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    with open(output_path + '/index.md', 'w') as output_file:
        output_file.write(custom_latex_to_text(latex_content))

    logging.info(f"Conversion complete. Output written to {output_path}")