import nbformat
from nbconvert import PDFExporter
from traitlets.config import Config
import os


# File data specific to the assignment
assignment_name = "Exercise_1"

files = ["1_the_audio_file.ipynb", 
         "2_processing_audio.ipynb", 
         "3_sinusoids.ipynb", 
         "4_audio_analysis.ipynb", 
         "5_audio_filtering.ipynb", 
         "6_exercise_review.ipynb"]

title = "Exercise 1: An introduction to Digital Signal Processing using Python"

intro_text = """
In this exercise, the focus is on audio signals. The exercise problems cover topics from sampling 
and audio file formatting, to spectral analysis of digital audio and simple filtering of audio signals.  
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
            nb.cells.pop(0) # Remove header
            nb.cells.pop(-1) # Remove footer
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
