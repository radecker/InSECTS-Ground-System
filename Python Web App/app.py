from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/password.html')
def password():
    return render_template('password.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/thermal-history.html')
def historicData():
    return render_template('thermal-history.html')

@app.route('/thermal-database.html')
def thermalDatabase():
    return render_template('thermal-database.html')

@app.route('/ground-segment-log.html')
def groundSegmentLog():
    return render_template('ground-segment-log.html')

@app.route('/ground-segment-status.html')
def groundSegmentStatus():
    return render_template('ground-segment-status.html')

@app.route('/commands-fan-on.html')
def commandsFanOn():
    return render_template('commands-fan-on.html')

@app.route('/commands-fan-off.html')
def commandsFanOff():
    return render_template('commands-fan-off.html')

@app.route('/autonomy-mode-commands.html')
def autoCommands():
    return render_template('autonomy-mode-commands.html')

@app.route('/about-insects.html')
def aboutInsects():
    return render_template('about-insects.html')

@app.route('/about-the-team.html')
def abouttheteam():
    return render_template('about-the-team.html')

@app.errorhandler(401)
def error401():
    return render_template('401.html')

@app.errorhandler(404)
def error404():
    return render_template('404.html')

@app.errorhandler(500)
def error500():
    return render_template('500.html')

if __name__=="__main__":
    app.run(debug=True)

