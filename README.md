
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

Workflow: 
    1: Read directory of papers 'inputs' and copy to 'inputs-processed'
    2: Run various scripts to process the tex files
    3: Run tex_to_md.py on the tex
    4: Run postprocessing on the md
    5: Move the md to output 'markdown' directory
If you get this far, you can start to check the output to find issues. If you go further the aimodels site is running on hugo and is how I render the pages to be visible
![image](https://github.com/neural-loop/tex-to-md/assets/654993/c5ab9558-19ff-4ff3-ba72-53e61f46e0d4)
![image](https://github.com/neural-loop/tex-to-md/assets/654993/f36bfd78-b5f2-47e1-bd12-23a590049fbf)
