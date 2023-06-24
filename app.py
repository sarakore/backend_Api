from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sarakore'
app.config['MYSQL_DB'] = 'sara_db'

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def get_word():
    cur = mysql.connection.cursor()
    cur.execute("SELECT word FROM words")
    result = cur.fetchone()
    cur.close()
    if result:
        return jsonify({'word': result[0]})
    else:
        return jsonify({'word': 'No word found'})

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        new_word = request.form['word']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE words SET word = %s", (new_word,))
        mysql.connection.commit()
        cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT word FROM words")
    current_word = cur.fetchone()
    cur.close()
    if current_word:
        return render_template('admin.html', current_word=current_word[0])
    else:
        return render_template('admin.html', current_word='No word found')

# Test cases
def test_get_word():
    with app.test_client() as client:
        response = client.get('/api/get_word')
        assert response.status_code == 200
        data = response.get_json()
        assert 'word' in data

def test_admin():
    with app.test_client() as client:
        response = client.get('/admin')
        assert response.status_code == 200
        assert b'Admin Portal' in response.data

if __name__ == '__main__':
    app.run(debug=True)
