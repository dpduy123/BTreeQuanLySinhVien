from flask import Flask, render_template, request, jsonify
from btree import BTree

app = Flask(__name__)

# Data storage
students_table = {}
# B-Trees (Order 3)
id_tree = BTree(order=3)
name_tree = BTree(order=3)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify({
        "table": list(students_table.values()),
        "id_tree": id_tree.to_dict(),
        "name_tree": name_tree.to_dict()
    })

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.json
    student_id = data.get("id")
    name = data.get("name")
    gender = data.get("gender")
    
    if not student_id or not name:
        return jsonify({"error": "Mã SV và Họ tên là bắt buộc"}), 400
        
    if student_id in students_table:
        return jsonify({"error": "Sinh viên đã tồn tại"}), 400
        
    student = {
        "id": student_id,
        "name": name,
        "gender": gender
    }
    
    # Thêm vào bảng gốc
    students_table[student_id] = student
    
    # Thêm vào chỉ mục
    id_tree.insert(student_id, student_id)
    name_tree.insert(name, student_id)
    
    return jsonify({"success": True}), 201

@app.route("/api/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    if student_id not in students_table:
        return jsonify({"error": "Không tìm thấy sinh viên"}), 404
        
    student = students_table[student_id]
    
    # Xóa khỏi chỉ mục
    id_tree.delete(student_id, student_id)
    name_tree.delete(student["name"], student_id)
    
    # Xóa khỏi bảng gốc
    del students_table[student_id]
    
    return jsonify({"success": True})

@app.route("/api/search", methods=["GET"])
def search_student():
    term = request.args.get("q", "")
    type_ = request.args.get("type", "id") # 'id' or 'name'
    
    results = []
    
    if type_ == "id":
        search_res = id_tree.search(term)
        if search_res:
            results = [students_table[s_id] for s_id in search_res if s_id in students_table]
    else:
        search_res = name_tree.search(term)
        if search_res:
            results = [students_table[s_id] for s_id in search_res if s_id in students_table]
            
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=8888)
