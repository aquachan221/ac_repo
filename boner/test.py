import requests
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    target = f"http://192.168.1.107:5000/{path}"
    resp = requests.request(
        method=request.method,
        url=target,
        headers={key: value for key, value in request.headers},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded_headers]
    return Response(resp.content, resp.status_code, headers)

app.run(host='0.0.0.0', port=80)