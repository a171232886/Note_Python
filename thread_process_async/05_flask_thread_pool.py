import json
import flask
import time
from concurrent.futures import ThreadPoolExecutor

app = flask.Flask(__name__)
pool = ThreadPoolExecutor()

def read_file():
    time.sleep(0.1)
    return 'file'

def read_db():
    time.sleep(0.2)
    return 'db'

def read_api():
    time.sleep(0.3)
    return 'api'


@app.route('/api')
def index():
    result_file = pool.submit(read_file)
    result_db = pool.submit(read_db)
    result_api = pool.submit(read_api)

    return json.dumps({
        'file': result_file.result(),
        'db': result_db.result(),
        'api': result_api.result()
    })

if __name__ == '__main__':
    app.run()
