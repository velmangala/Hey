from app import app

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/')
def working():
    return "hello world!"

