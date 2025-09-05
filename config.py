class Config:
    SECRET_KEY = "secret"
    UPLOAD_FOLDER = "static/uploads"
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SESSION_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = None

    HOST = "127.0.0.1"
    PORT = 5000