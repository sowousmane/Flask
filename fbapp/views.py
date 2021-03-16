from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscription')    
def inscription():
    return render_template('inscription.html')

@app.route('/connexion')    
def connexion():
    return render_template('connection.html')

@app.route('/don')    
def don():
    return render_template('don.html')


