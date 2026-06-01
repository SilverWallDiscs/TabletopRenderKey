import os
from flask import Flask, request, jsonify
import requests
import traceback

app = Flask(__name__)

STEAM_KEY = os.environ.get("MI_API_KEY")

@app.route("/avatar-steam", methods=["POST"])
def avatar_steam():
    try:
        print("=== NUEVA PETICION ===")
        print("CONTENT TYPE:", request.content_type)

        raw_data = request.get_data(as_text=True)

        print("RAW DATA:")
        print(repr(raw_data))

        return jsonify({
            "debug": raw_data
        })

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/", methods=["GET"])
def home():
    return "Steam Avatar API Online"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
