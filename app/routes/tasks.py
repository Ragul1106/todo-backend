from flask import Blueprint, request, jsonify
from ..db import mysql
from datetime import datetime

task_bp = Blueprint('task_bp', __name__, url_prefix="/api")

@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute("SELECT id, task_name AS title, description, due_date, priority, is_completed FROM tasks ORDER BY due_date")
        rows = cur.fetchall()
        cur.close()
        return jsonify(rows)
    except Exception as e:
        print("🔥 GET error:", e)
        return jsonify({"error": str(e)}), 500

@task_bp.route("/tasks", methods=["POST", "OPTIONS"])
def add_task():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        due_date_str = data.get("due_date")
        priority = data.get("priority", "Medium")

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.fromisoformat(due_date_str)
            except ValueError:
                return jsonify({"error": "Invalid date format"}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO tasks (task_name, description, due_date, priority, is_completed)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, description, due_date, priority, False))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Task added"}), 201
    except Exception as e:
        print("🔥 POST error:", e)
        return jsonify({"error": str(e)}), 500

@task_bp.route("/tasks/<int:id>", methods=["PUT", "OPTIONS"])
def update_task(id):
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE tasks
            SET task_name=%s, description=%s, due_date=%s, priority=%s, is_completed=%s
            WHERE id=%s
        """, (
            data.get("title"),
            data.get("description"),
            data.get("due_date"),
            data.get("priority"),
            data.get("is_completed"),
            id
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Task updated"})
    except Exception as e:
        print("🔥 PUT error:", e)
        return jsonify({"error": str(e)}), 500

@task_bp.route("/tasks/<int:id>", methods=["DELETE", "OPTIONS"])
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
        print("🔥 DELETE error:", e)
        return jsonify({"error": str(e)}), 500
