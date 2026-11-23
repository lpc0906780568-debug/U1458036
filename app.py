from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <title>每日笑話小站</title>
</head>
<body style="font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 0 16px;">
  <h1>每日笑話小站</h1>
  <p><strong>問題：</strong>{{ setup }}</p>
  <p><strong>答案：</strong>{{ punchline }}</p>
  <button onclick="location.reload()">換一則笑話</button>
</body>
</html>
"""


@app.route("/")
def home():
  try:
    res = requests.get(
        "https://official-joke-api.appspot.com/random_joke", timeout=8
    )
    res.raise_for_status()
    data = res.json()
    setup = data.get("setup", "找不到笑話問題")
    punchline = data.get("punchline", "找不到笑話答案")
  except Exception:
    setup = "目前無法取得外部笑話"
    punchline = "請稍後再按一次「換一則笑話」。"
  return render_template_string(HTML, setup=setup, punchline=punchline)


@app.route("/api/joke")
def api_joke():
  try:
    res = requests.get(
        "https://official-joke-api.appspot.com/random_joke", timeout=8
    )
    res.raise_for_status()
    return jsonify(res.json())
  except Exception as e:
    return jsonify({"error": str(e)}), 502


@app.route("/api/health")
def health():
  return jsonify({"status": "ok"})
