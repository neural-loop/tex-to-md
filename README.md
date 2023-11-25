
https://pylatexenc.readthedocs.io/en/latest/latex2text/ does the heavy lifting.
You can see its output by running latex2text on a tex file.

The script is adding some preprocessing to happen before latex2text (tex_to_md.py)
to prep and update content.

The most complicated of the handling scripts are 
- tex_figure_prep (converts images to png)
- tex_figures (converts tex into Hugo Shortcode )

Use: 
arxiv-search.py (downloads papers into /inputs) (I committed some papers its not needed to run this)
pipeline.py -> will process and move papers into /failed or /inputs-processed and /markdown when complete
