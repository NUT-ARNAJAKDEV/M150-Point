from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# ฟังก์ชันสร้างฐานข้อมูล


def init_db():
    conn = sqlite3.connect('points.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  code TEXT,
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()

# ฟังก์ชันนับจำนวนแต้ม


def get_points_count():
    conn = sqlite3.connect('points.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM transactions")
    count = c.fetchone()[0]
    conn.close()
    return count


@app.route('/')
def home():
    init_db()  # ตรวจสอบว่ามีตารางหรือยัง
    return render_template('index.html')

# เพิ่ม endpoint สำหรับ AJAX


@app.route('/get_points')
def get_points():
    count = get_points_count()
    return jsonify({
        'count': count,
        'formatted_count': f"{count:,}"  # เพิ่มรูปแบบตัวเลขด้วย comma
    })


if __name__ == '__main__':
    app.run(debug=True)
