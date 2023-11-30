from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
app.app_context().push()

class ExcelData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        df = pd.read_excel(file)
        json_data = df.to_json(orient='records')

        # Store data in the database
        new_data = ExcelData(data=json_data)
        db.session.add(new_data)
        db.session.commit()

        return jsonify({'data': json_data})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
