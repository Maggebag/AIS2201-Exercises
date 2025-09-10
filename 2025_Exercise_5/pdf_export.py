import nbformat
from nbconvert import PDFExporter
from traitlets.config import Config
import os


# File data specific to the assignment
assignment_name = "Exercise_5"



files = ["1_spectral_leakage.ipynb", 
         "2_zero_padding.ipynb", 
         "3_window_functions.ipynb", 
         "4_spectrograms.ipynb",
         "5_exercise_review.ipynb"]

title = "Exercise 5: Spectral leakage, window functions and spectrograms"

intro_text = """
The focus of this exercise is to explore the limitations of Discrete Fourier Transformation as a tool in frequency analysis, and different approaches to managing these limitations. Finally, we will  take a closer look at the spectrogram as an analysis tool, and how the various parameters for spectrogram calculation affect the quality of our output.
"""


def write_to_PDF(student_name: str):
    """
    Function to compile 1 PDF document from a list of '.ipynb' in consecutive order.

    Parameters
    ----------
    assignment_name : str
        Name of output file (file format '.pdf' will be appended)
        Default value for document title
    files : list[str]
        List of Jupyter Notebook files (.ipynb) to compile into output pdf.
    student_name : str
        Sets the author in the output file's title section
    title : str, optional
        The output PDF's title. Defaults to 'assignment_name' if not specified.
    intro_text : str, optional
        Text for initial paragraph preceding content of the first Jupyter Notebook
        file in the 'files' argument.

    Output
    -------
    output file : <assignment_name>.pdf
        Document to be uploaded to learning management system (Blackboard, Canvas, 
        Inspera etc..).
    """

    # c = Config()
    # c.TemplateExporter.extra_template_basedirs = ["./assignment_template"]
    # c.TemplateExporter.template_name = 'latex'
    
    merged = nbformat.v4.new_notebook()
    merged.metadata["title"] = title if title != "" else assignment_name
    merged.metadata["authors"] = [{"name": student_name}]
    merged_cells = []
    if intro_text != "":
        merged_cells.append(nbformat.v4.new_markdown_cell(source=intro_text))

    for file in files:
        with open(file, 'r', encoding='utf-8') as fh:
            nb = nbformat.read(fh, as_version=4)
            #nb.cells.pop(0) # Remove header
            #nb.cells.pop(-1) # Remove footer
            merged_cells.extend(nb.cells)
            
    merged.cells = merged_cells

    exporter = PDFExporter()

    # Export to PDF bytes
    pdf_data, _resources = exporter.from_notebook_node(
        merged,
        resources={"metadata": {"path": os.getcwd()}},
    )

    # Write the PDF
    with open(assignment_name + ".pdf", "wb") as f:
        f.write(pdf_data)

def pdf_convert_debug():
    student_name = "Ola Normann"
    merged = nbformat.v4.new_notebook()
    merged.metadata["title"] = title if title != "" else assignment_name
    merged.metadata["authors"] = [{"name": student_name}]


    for file in files:
        print(f"Processing {file}")
        with open(file, 'r', encoding='utf-8') as fh:
            nb = nbformat.read(fh, as_version=4)
            for cell in nb.cells:
                merged.cells = [cell]
                exporter = PDFExporter()
                try:
                    # Export to PDF bytes
                    pdf_data, _resources = exporter.from_notebook_node(
                        merged,
                        resources={"metadata": {"path": os.getcwd()}},
                    )
                except:
                    raise Exception(f"problem encountered converting '{file}' \n cell contents: \n {cell.source}")
