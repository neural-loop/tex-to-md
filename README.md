
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

If you get this far, you can start to check the output to find issues. If you go further the aimodels site is running on hugo and is how I render the pages to be visible
![image](https://github.com/neural-loop/tex-to-md/assets/654993/c5ab9558-19ff-4ff3-ba72-53e61f46e0d4)
![image](https://github.com/neural-loop/tex-to-md/assets/654993/f36bfd78-b5f2-47e1-bd12-23a590049fbf)
