from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": [
    "https://todo-list-managing.netlify.app", 
    "http://localhost:5173"  
]}})

app.config['MYSQL_HOST'] = 'turntable.proxy.rlwy.net'
app.config['MYSQL_PORT'] = 38656
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yvADtitJOieTGVMXmaEidbbOgMRegfTq'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


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
            {"id": row['id'], "title": row['task_name'], "completed": bool(row['is_completed'])}
            for row in rows
        ])
    except Exception as e:
        print("❌ GET /api/tasks Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks', methods=['POST', 'OPTIONS'])
def add_task():
    if request.method == 'OPTIONS':
        return '', 200  
    try:
        data = request.get_json()
        title = data.get("title")
        if not title:
            return jsonify({"error": "Title is required"}), 400
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (task_name, is_completed) VALUES (%s, %s)", (title, False))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Task added"}), 201
    except Exception as e:
        print("❌ POST /api/tasks Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<int:id>', methods=['PUT', 'OPTIONS'])
def update_task(id):
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        completed = data.get("completed")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tasks SET is_completed = %s WHERE id = %s", (completed, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Task updated"})
    except Exception as e:
        print("❌ PUT /api/tasks Error:", e)
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
        print("❌ DELETE /api/tasks Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
