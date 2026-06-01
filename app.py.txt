import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Recuperamos la clave secreta guardada de forma segura en Render
API_KEY = os.environ.get('MI_API_KEY')

@app.route('/procesar', methods=['POST'])
def procesar():
    datos_juego = request.json
    
    # 1. Aquí tu mini web usa la clave en secreto para hablar con el servicio real
    # (Cambia esta URL por la del servicio que estés usando)
    url_servicio = "https://ejemplo.com" 
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    respuesta = requests.post(url_servicio, json=datos_juego, headers=headers)
    
    # 2. Le devolvemos a Tabletop Simulator el resultado SIN la clave
    return jsonify(respuesta.json()), respuesta.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))