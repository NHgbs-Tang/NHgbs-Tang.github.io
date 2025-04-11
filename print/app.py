from flask import Flask, request, jsonify, send_from_directory, abort
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 上传文件
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return jsonify({'message': '文件上传成功'}), 200


# 获取文件列表
@app.route('/files', methods=['GET'])
def get_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify([{'filename': file} for file in files])


# 下载文件
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


# 删除文件
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': '文件删除成功'}), 200
    else:
        return jsonify({'error': '文件不存在'}), 404


if __name__ == '__main__':
    app.run(debug=True)
    