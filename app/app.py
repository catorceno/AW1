from flask import Flask, render_template

app = Flask(__name__) # utilidades

@app.route("/") # decorador, adicion funcionalidades a otra función, agrega sin modificar lo que esta envolviendo
def index(): # no tiene que devolver cosas, sino que debe responder a una solicitud http
  return render_template("index.html", name="oh my")

if __name__ == "__main__": # main function
  app.run(host="0.0.0.0", debug=True)
