import hashlib
import re
import unicodedata
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src/starter'))
from core import INTENTS,classification_score,fingerprint

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def key(text):
    return re.sub(r'\s+',' ',unicodedata.normalize('NFC',str(text))).strip().casefold()

def duplicate_key(text):
    """Ignore punctuation for duplicate checks, while preserving original wording."""
    return ' '.join(''.join(c for c in key(text) if not unicodedata.category(c).startswith('P')).split())
