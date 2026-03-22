from flask import Flask, request, Response
import requests, os

app = Flask(__name__)

PROXY_TOKEN  = "ls-binance-proxy-2026"
BINANCE_BASE = "https://api.binance.com"

@app.route("/<path:path>", methods=["GET","POST","PUT","DELETE"])
def proxy(path):
    if request.headers.get("X-Proxy-Token") != PROXY_TOKEN:
        return Response("Unauthorized", status=401)
    url     = f"{BINANCE_BASE}/{path}"
    headers = {k: v for k, v in request.headers if k not in ("Host","X-Proxy-Token")}
    resp    = requests.request(
        method  = request.method,
        url     = url,
        headers = headers,
        params  = request.args,
        data    = request.get_data(),
        timeout = 10
    )
    return Response(resp.content, status=resp.status_code)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
