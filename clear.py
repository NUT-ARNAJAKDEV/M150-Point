import sqlite3


def clear_data():
    conn = sqlite3.connect('points.db')
    c = conn.cursor()
    c.execute("DELETE FROM transactions")
    print("ล้างข้อมูลทั้งหมดในตาราง transactions แล้ว")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    clear_data()
