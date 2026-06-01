import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

STEAM_KEY = os.environ.get("MI_API_KEY")

@app.route("/avatar-steam", methods=["POST"])
def avatar_steam():
    try:
        data = request.get_json()

        steam_id = data.get("steam_id")
        if not steam_id:
            return jsonify({"error": "steam_id requerido"}), 400

        url = (
            "https://api.steampowered.com/"
            "ISteamUser/GetPlayerSummaries/v2/"
            f"?key={STEAM_KEY}&steamids={steam_id}"
        )

        steam_response = requests.get(url, timeout=15)
        steam_data = steam_response.json()

        players = steam_data.get("response", {}).get("players", [])

        if not players:
            return jsonify({"error": "Jugador no encontrado"}), 404

        avatar_url = players[0]["avatarfull"]

        return jsonify({
            "avatarUrl": avatar_url
        })

    except Exception as e:
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
