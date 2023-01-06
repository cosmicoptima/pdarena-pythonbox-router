from base64 import b64encode
from flask import Flask, request
from flask_cors import CORS
from os import chmod
import requests
from tarfile import TarFile
from tempfile import TemporaryDirectory, NamedTemporaryFile

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def index():
    files = request.get_json()
    with TemporaryDirectory() as tmpdir:
        with TarFile.open(name=tmpdir + '/a.tar', mode='w') as tar:
            for name, contents in files.items():
                with open(tmpdir + '/' + name, 'w') as f:
                    f.write(contents)
                chmod(tmpdir + '/' + name, 0o755)
                tar.add(tmpdir + '/' + name, arcname=name)

        with open(tmpdir + '/a.tar', 'rb') as f:
            encoded = b64encode(f.read()).decode('utf-8')

    result = requests.post('http://localhost:8075/run_code', json={'base_64_tar_gz': encoded, 'max_time_s': 1})
    return result.text

if __name__ == '__main__':
    app.run(port=8099)
