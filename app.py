from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import config

app = Flask(__name__)

from flask_cors import CORS

CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:5173",
    "https://chipper-malasada-65cf89.netlify.app/",
]}})




app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, task_name, is_completed FROM tasks")
        tasks = [{'id': row[0], 'title': row[1], 'completed': bool(row[2])} for row in cur.fetchall()]
        cur.close()
        return jsonify(tasks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST', 'OPTIONS'])
def add_task():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        task_name = data.get('title')
        if not task_name:
            return jsonify({'error': 'Title is required'}), 400

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (task_name, is_completed) VALUES (%s, %s)", (task_name, False))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Task added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:id>', methods=['PUT', 'OPTIONS'])
def update_task(id):
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tasks SET is_completed = %s WHERE id = %s", (data['completed'], id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Task updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete_task(id):
    if request.method == 'OPTIONS':
        return '', 200
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Task deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/')
def index():
    return 'Flask To-Do API Running '

if __name__ == "__main__":
    app.run(debug=True)
