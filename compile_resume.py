#!/usr/bin/env python3
import os
import re
import sys
import subprocess
import json
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))

html_jinja_env = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)

latex_jinja_env = Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = FileSystemLoader(os.path.join(PATH, 'templates'))
)

def load_json(json_file):
    with open(json_file) as json_file:
        data = json.load(json_file)
        output_format = data["output_format"]

        file_contents = json_file.read()
        converted_text = transform_text(file_contents, output_format)
        data = json.loads(converted_text)
    return data

def transform_text(text, output_format):
    # Transform json values where necessary w.r.t. output format
    if output_format == "tex":
        text = re.sub(r'\*\*([^\*]*)\*\*', r'\\\\textbf{\1}', text)
    elif output_format == "html":
        text = re.sub(r'\*\*([^\*]*)\*\*', r'<b>\1</b>', text)
    else:
        pass
    return text

def render_from_template(template, **kwargs):
    if template.endswith(".tex"):
        env = latex_jinja_env
    elif template.endswith(".html"):
        env = html_jinja_env
    else:
        print("Invalid output format")
        exit(1)
    template = env.get_template(template)
    return template.render(**kwargs)

def tex_to_pdf(file):
    cmd = ["latexmk", 
            "-synctex=1",
            "-interaction=nonstopmode",
            "-file-line-error",
            "-pdf",
            os.path.join(PATH, file)]

    subprocess.run(cmd)

    # Remove all temporary build files
    source = os.listdir(PATH)
    for output_file in source:
        if output_file.split(".")[-1] in ["gz", "out", "log", "fls", "fdb_latexmk", "aux"]:
            os.unlink(os.path.join(PATH, output_file))

def render_resume(json_file):
    with open(json_file) as f:
        output_formats = json.load(f)["output_formats"]
        f.seek(0)
        content = f.read()

    for output_format in output_formats:
        print(output_format)
        filename = "resume." + output_format
        converted_text = transform_text(content, output_format)
        data = json.loads(converted_text)

        render = render_from_template(filename, language=data["language"],
                                                information=data["information"],
                                                other=data["other"],
                                                education_items=data["education"], 
                                                experience_items=data["experience"],
                                                skill_items=data["skills"])

        with open(os.path.join(PATH, filename), 'w', encoding="utf-8") as f:
            f.write(render)
        
        if output_format == "tex":
            tex_to_pdf(filename)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please provide a json file to compile")
        exit(1)

    render_resume(sys.argv[1])