import os
from flask import Flask, request, jsonify
import requests
import traceback

@app.route("/avatar-steam", methods=["POST"])
def avatar_steam():
    try:
        import urllib.parse
        import json

        raw_data = request.get_data(as_text=True)

        print("RAW:", raw_data)

        decoded = urllib.parse.unquote(raw_data)

        print("DECODED:", decoded)

        data = json.loads(decoded)

        steam_id = data["steam_id"]

        url = (
            "https://api.steampowered.com/"
            "ISteamUser/GetPlayerSummaries/v2/"
            f"?key={STEAM_KEY}&steamids={steam_id}"
        )

        steam_response = requests.get(url, timeout=15)

        print("STEAM STATUS:", steam_response.status_code)
        print("STEAM RESPONSE:", steam_response.text)

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
