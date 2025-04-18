from pathlib import Path
from datetime import timedelta
import re

CHAR_FIELD_MAX_LENGTH = 255
MOVIE_POSTER_UPLOAD_PATH = Path("movie/posters/")
MOVIE_VIDEO_UPLOAD_PATH = Path("movie/videos/")

USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 30

# String consists only of letters (uppercase and lowercase), numbers, hyphens, and underscores.
USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")

PASSWORD_MIN_LENGTH = 6
PASSWORD_MAX_LENGTH = 128

# Passwords contains at least one: lowercase letter, uppercase letter and digit
PASSWORD_PATTERN = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$")


ACCESS_TOKEN_LIFETIME = 15 * 60             # 15 minutes
REFRESH_TOKEN_LIFETIME = 15 * 24 * 3600     # 15 days
JWT_ALGORITHM = "HS256"
ACCESS_DECODE_OPTIONS = {"verify_signature": True, "require": ["sub", "email", "iat", "exp"]}
REFRESH_DECODE_OPTIONS = {"verify_signature": True, "require": ["sub", "iat", "exp", "type"]}
