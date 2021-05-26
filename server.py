import time
import zipfile
from io import BytesIO

import yaml
from flask import Flask, request, send_file

from application.specification_diff import run_diff

UPLOAD_FOLDER = 'c:/dev/temp'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'yml', 'yaml'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/analyse-openapi3-spec/upload/', methods=['POST'])
def analyse_openapi3():
    # check if the post request has the file part
    if 'base_spec' not in request.files or 'target_spec' not in request.files:
        return 'No file part'
    base_spec_file = request.files['base_spec']
    target_spec_file = request.files['target_spec']
    # if user does not select file, browser also submit an empty part without filename
    if base_spec_file.filename == '' or target_spec_file.filename == '':
        return 'No selected file'
    if base_spec_file and allowed_file(base_spec_file.filename) and target_spec_file and allowed_file(
            target_spec_file.filename):
        base_spec = yaml.safe_load(str(base_spec_file.stream.read(), encoding='utf-8'))
        target_spec = yaml.safe_load(str(target_spec_file.stream.read(), encoding='utf-8'))
        error_report, complete_report = run_diff(base_spec, target_spec)

        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as report:
            data = zipfile.ZipInfo('error_report.md')
            data.date_time = time.localtime(time.time())[:6]
            data.compress_type = zipfile.ZIP_DEFLATED
            report.writestr(data, error_report)

            data = zipfile.ZipInfo('complete_report.md')
            data.date_time = time.localtime(time.time())[:6]
            data.compress_type = zipfile.ZIP_DEFLATED
            report.writestr(data, complete_report)
        memory_file.seek(0)
        return send_file(memory_file, download_name='diff_report.zip', as_attachment=True)
    return 'No processable files'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
