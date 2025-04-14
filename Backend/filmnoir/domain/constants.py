from pathlib import Path
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

