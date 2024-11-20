import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse


class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_db(self):
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """)
            db.commit()

    def add_user(self, name, email):
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
            db.commit()

    def get_users(self):
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute("SELECT name, email FROM users")
            return cur.fetchall()


class RequestHandler(BaseHTTPRequestHandler):
    db = DataBase("users.db")
    db.create_db()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.display_page()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        form_data = urllib.parse.parse_qs(post_data.decode("utf-8"))

        name = form_data.get("name", [""])[0]
        email = form_data.get("email", [""])[0]

        if name and email:
            try:
                self.db.add_user(name, email)
            except sqlite3.IntegrityError:
                pass  # Игнорируем дублирующиеся записи
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def display_page(self):
        users = self.db.get_users()
        user_list = "".join(f"<li>Name: {user[0]}, Email: {user[1]}</li>" for user in users)

        response = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>User Form</title>
        </head>
        <body>
            <h1>Add User</h1>
            <form action="/" method="post">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" required><br><br>
                <label for="email">Email:</label><br>
                <input type="email" id="email" name="email" required><br><br>
                <button type="submit">Submit</button>
            </form>
            <h2>Submitted Users:</h2>
            <ul>
                {user_list if user_list else "<li>No users added yet.</li>"}
            </ul>
        </body>
        </html>
        """
        self.wfile.write(response.encode("utf-8"))


def run():
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server running on port 8080...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
