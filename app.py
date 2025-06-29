from flask import Flask, render_template, jsonify, request
import sqlite3
import easyocr
import os
import re
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])


def init_db():
    conn = sqlite3.connect('points.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  code TEXT,
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()


def get_points_count():
    conn = sqlite3.connect('points.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM transactions")
    count = c.fetchone()[0]
    conn.close()
    return count


def validate_code(code):
    """Validate that code is exactly 11 digits"""
    return bool(re.fullmatch(r'^\d{11}$', code))


def extract_code_from_image(image_path):
    try:
        results = reader.readtext(image_path)
        all_text = ' '.join([res[1] for res in results])

        # Find all sequences of 11+ digits
        digit_sequences = re.findall(r'\d{11,}', all_text)

        # Check for invalid codes (more than 11 digits)
        for seq in digit_sequences:
            if len(seq) > 11:
                return {'valid': False, 'error': 'รหัสไม่ถูกต้อง! พบตัวเลขมากกว่า 11 หลัก'}

        # Find exact 11-digit codes
        matches = re.findall(r'\b\d{11}\b', all_text)

        if matches:
            return {'valid': True, 'code': matches[0]}

        return {'valid': False, 'error': 'ไม่พบรหัส 11 หลักในภาพ'}
    except Exception as e:
        print(f"Error processing image: {e}")
        return {'valid': False, 'error': 'เกิดข้อผิดพลาดในการประมวลผลภาพ'}


@app.route('/')
def home():
    init_db()
    return render_template('index.html')


@app.route('/get_points')
def get_points():
    count = get_points_count()
    return jsonify({
        'count': count,
        'formatted_count': f"{count:,}"
    })


@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'valid': False, 'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'valid': False, 'error': 'No selected file'}), 400

    # Save temporary file
    filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Process image
    result = extract_code_from_image(filepath)

    # Clean up
    try:
        os.remove(filepath)
    except:
        pass

    return jsonify(result)


@app.route('/submit_codes', methods=['POST'])
def submit_codes():
    data = request.get_json()
    codes = data.get('codes', [])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    saved = []
    duplicates = []

    conn = sqlite3.connect('points.db')
    c = conn.cursor()

    for code in codes:
        c.execute("SELECT 1 FROM transactions WHERE code = ?", (code,))
        if c.fetchone():
            duplicates.append(code)
        else:
            c.execute(
                "INSERT INTO transactions (code, timestamp) VALUES (?, ?)", (code, timestamp))
            saved.append(code)

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'saved': saved,
        'duplicates': duplicates
    })


if __name__ == '__main__':
    app.run(debug=True)
