import sys
import os
import glob
import subprocess
from pathlib import Path
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.lexers import TextLexer
from pygments.formatters import LatexFormatter

tmp_directory = '/tmp/repo2pdf/'

if __name__ == '__main__':
    working_directory = os.getcwd()

    try:
        os.mkdir(tmp_directory)
    except:
        pass
    for f in os.listdir(tmp_directory):
        os.remove(os.path.join(tmp_directory, f))

    for filename in glob.iglob(os.path.abspath(sys.argv[1]) + '**/**', recursive=True):
        if not Path(filename).is_file():
            continue

        code = ''
        with open(filename, 'r') as file:
            code = file.read()

        try:
            lexer = guess_lexer(code)
        except:
            lexer = TextLexer
        formatter = LatexFormatter(full=True)

        code = "//" + os.path.basename(filename) + "\n\n" + code

        processed = highlight(code, lexer, formatter)

        output_file = tmp_directory + os.path.basename(filename) + ".tex"
        with open(output_file, "w") as tex_file:
            tex_file.write(processed)

        os.chdir(tmp_directory)
        subprocess.run(["pdflatex", output_file])

    os.chdir(working_directory)
    subprocess.call(working_directory + '/merge-pdfs.sh', shell=True)


# TODO: Consider .gitignore

