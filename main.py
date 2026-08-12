from flask import Flask

app = Flask(__name__) # utilidades

@app.route("/") # decorador, adicion funcionalidades a otra función, agrega sin modificar lo que esta envolviendo
def hello(): # no tiene que devolver cosas, sino que debe responder a una solicitud http
  return "hi oh my"

if __name__ == "__main__": # main function
  app.run(debug=true)
