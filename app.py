import os
from typing import Tuple

from flask import Flask
from flask import request, render_template, send_file
from pdf2docx.main import parse


UPLOADER_FOLDER = ''
app = Flask(__name__)
app.config['UPLOADER_FOLDER'] = UPLOADER_FOLDER


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        def convert_pdf2docx(input_file1: str, output_file1: str, pages: Tuple = None):
            if pages:
                pages = [int(i) for i in list(pages) if i.isnumeric()]

            result = parse(pdf_file=input_file1, docx_with_path=output_file1, pages=pages)
            summary = {
                "File": input_file1, "Pages": str(pages), "Output File": output_file1
            }

            print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
            return result

        file = request.files['filename']
        if file.filename != '':
            file.save(os.path.join(app.config['UPLOADER_FOLDER'], file.filename))
            input_file = file.filename
            output_file = r"hello.docx"
            convert_pdf2docx(input_file, output_file)
            doc = input_file.split(".")[0] + ".docx"
            print(doc)
            lis = doc.replace(" ", "=")
            return render_template("docx.html", variable=lis)
    return render_template("index.html")


@app.route('/docx', methods=['GET', 'POST'])
def docx():
    if request.method == "POST":
        lis = request.form.get('filename', None)
        lis = lis.replace("=", " ")
        return send_file(lis, as_attachment=True)
    return render_template("index.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
