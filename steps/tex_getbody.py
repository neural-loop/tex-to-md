import os


def extract_document_content(input_path):
    # Construct the full path to main.tex
    main_tex_path = os.path.join(input_path, 'main.tex')

    # Check if the file exists
    if not os.path.exists(main_tex_path):
        print(f"Error: {main_tex_path} does not exist.")
        return

    # Read the content of main.tex
    with open(main_tex_path, 'r') as file:
        content = file.read()

    # Find the indices of \begin{document} and \end{document}
    begin_index = content.find('\\begin{document}')
    end_index = content.find('\\end{document}')

    # Check if both markers are found
    if begin_index == -1 or end_index == -1:
        print("Error: \\begin{document} or \\end{document} not found in main.tex.")
        return

    # Extract the content between \begin{document} and \end{document}
    new_content = content[begin_index:end_index + len('\\end{document}')]

    # Update main.tex with the new content
    with open(main_tex_path, 'w') as file:
        file.write(new_content)

    print(f"Successfully updated {main_tex_path}.")
