# BASE_DIR = Path(__file__).resolve().parent
# DB_PATH = BASE_DIR / "students.db"
# def get_connection():
#     conn = sqlite3.connect(str(DB_PATH))
#     conn.row_factory = sqlite3.Row
#     conn.execute("PRAGMA foreign_keys = ON;")
#     return conn