from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": [
    "https://todo-list-managing.netlify.app",  
    "http://localhost:5173"  
]}})

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ragul@116'
app.config['MYSQL_DB'] = 'todo_list'

mysql = MySQL(app)

@app.route('/')
def home():
    return "✅ Flask API is running!"

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, task_name, is_completed FROM tasks")
        rows = cur.fetchall()
        cur.close()
        return jsonify([
            {"id": row[0], "title": row[1], "completed": bool(row[2])} for row in rows
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks', methods=['POST', 'OPTIONS'])
def add_task():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        title = data.get("title")
        if not title:
            return jsonify({"error": "Title required"}), 400
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (task_name, is_completed) VALUES (%s, %s)", (title, False))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Task added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        return jsonify({"message": "Task updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete_task(id):
    if request.method == 'OPTIONS':
        return '', 200
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Task deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
