import sqlite3
from datetime import datetime


def add_sample_data():
    # ข้อมูลตัวอย่าง 3 รายการ
    sample_data = [
        ("123456789012", "2023-01-15 10:30:00"),
        ("987654321098", "2023-01-16 14:45:00"),
        ("456789123456", "2023-01-17 09:15:00")
    ]

    conn = sqlite3.connect('points.db')
    c = conn.cursor()

    # เพิ่มข้อมูลลงตาราง
    c.executemany(
        "INSERT INTO transactions (code, timestamp) VALUES (?, ?)", sample_data)

    print(f"เพิ่มข้อมูลตัวอย่างสำเร็จ {len(sample_data)} รายการ")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    add_sample_data()
