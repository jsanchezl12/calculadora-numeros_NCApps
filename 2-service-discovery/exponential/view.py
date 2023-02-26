from flask import Flask
from flask import request
import os
import requests

app = Flask(__name__)

@app.route('/exponencial',methods = ['POST'])
def Exponencial():
    multiplicacion_url = os.getenv("MULTIPLICACION_MS")
    
    if request.method == 'POST':
        try:
            numero , potencia = request.json["numero"], request.json["potencia"]
        except:
            return {"message": ""}

        resultado = numero
        for _ in range(potencia-1):
            obj = {'num_1': resultado, 'num_2': numero}
            req = requests.post(multiplicacion_url + '/multiplicar', json = obj)
            if req.status_code != 200:
                raise Exception(req.text)
            resultado = req.json()["result"]

        return {"message": f"Elevando {numero} a la {potencia} se obtiene {resultado}" , "result": resultado}, 200
            

@app.route('/health',methods = ['GET'])
def Health():
    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)