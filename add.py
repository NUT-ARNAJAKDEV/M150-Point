import sqlite3
from datetime import datetime


def add_sample_data():
    # ข้อมูลตัวอย่าง 3 รายการ
    sample_data = [
        ("12345678901", "2023-01-15 10:30:00"),
        ("98765432109", "2023-01-16 14:45:00"),
        ("45678912345", "2023-01-17 09:15:00")
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
