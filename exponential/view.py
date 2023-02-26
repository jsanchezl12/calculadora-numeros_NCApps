
from flask import Flask
from flask import request
import os

app = Flask(__name__)


@app.route('/exponencial',methods = ['POST'])
def Suma():
    message = ""
    user_name = os.getenv("user_name")
    
    if request.method == 'POST':
        try:
            numero1, numero2 = request.json["num_1"], request.json["num_2"]
        except:
            return {"message": EscribirResultado("Indique dos numeros para ser sumados", user_name,None,None)}, 404
        
        message = f"suma de los dos numeros es: {numero1 + numero2}" 
        message = user_name + " la " + message if user_name else "La " + message  

        return {"message": EscribirResultado(message, user_name, numero1, numero2), "result": numero1 + numero2}, 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)