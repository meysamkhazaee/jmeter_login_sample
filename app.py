import os
import http.server
import socketserver
import sqlite3
import urllib.parse

# Specify the current directory to serve
LOCAL_FOLDER = os.getcwd()  # This will serve the current working directory

# Set the host and port
HOST = '0.0.0.0'  # Use '0.0.0.0' for access from other devices
PORT = 8080

# Initialize SQLite database connection
DB_FILE = 'user_database.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DB_FILE)

def create_table():
    """Create the users table if it doesn't exist."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Create the users table if it doesn't exist (run this once manually or at server startup)
create_table()

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Handles GET requests."""
        if self.path == "/login.html" or self.path == "/":
            self.serve_html("login.html")
        elif self.path == "/welcome.html":
            self.serve_html("welcome.html")
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        """Handles POST requests."""
        if self.path == "/login.html":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            username = post_data.get('username', [None])[0]
            password = post_data.get('password', [None])[0]

            if self.authenticate_user(username, password):
                self.redirect_to_welcome(username)
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><body><h2>Invalid credentials. Please try again.</h2></body></html>")

    def authenticate_user(self, username, password):
        """Authenticate user against the SQLite database."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def serve_html(self, filename):
        """Serves an HTML file from the current directory."""
        try:
            with open(os.path.join(LOCAL_FOLDER, filename), 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, "File Not Found")

    def redirect_to_welcome(self, username):
        """Redirects to the welcome page with a personalized message."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response_html = f"<html><body><h2>Welcome, {username}!</h2></body></html>"
        self.wfile.write(response_html.encode('utf-8'))

def start_server():
    with socketserver.TCPServer((HOST, PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serving files from {LOCAL_FOLDER} at http://{HOST}:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
