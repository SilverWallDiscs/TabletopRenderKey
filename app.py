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
        print("STEAM_KEY EXISTE:", STEAM_KEY is not None)

        data = request.get_json(force=True)
        print("DATA:", data)

        steam_id = data["steam_id"]
        print("STEAM_ID:", steam_id)

        url = (
            "https://api.steampowered.com/"
            "ISteamUser/GetPlayerSummaries/v2/"
            f"?key={STEAM_KEY}&steamids={steam_id}"
        )

        steam_response = requests.get(url, timeout=15)

        print("STATUS:", steam_response.status_code)
        print("RESPUESTA:", steam_response.text)

        steam_data = steam_response.json()

        players = steam_data.get("response", {}).get("players", [])

        if not players:
            return jsonify({
                "error": "Jugador no encontrado"
            }), 404

        return jsonify({
            "avatarUrl": players[0]["avatarfull"]
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
