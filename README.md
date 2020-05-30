# Resumegen

Python script that converts json files to HTML or PDF (LaTeX) resumes. Supports multiple languages.

## Installation

Required apt packages are `texlive-full`, `latexmk` and `texlive-lang-european`, required python 3 packages are listed in `requirements.txt`.

## Usage 

To compile a json file to pdf:

```bash
./compile_resume.py resume.json
```