import json
from pathlib import Path
from typing import List

from crypto_manager import (
    WrongPasswordError,
    decrypt,
    derive_key,
    encrypt,
    generate_salt,
)
from models import Note

APP_DIR = Path.home() / ".encrypted_notes"
SALT_FILE = APP_DIR / "salt.bin"
DATA_FILE = APP_DIR / "notes.enc"


class NoteStorage:

    def __init__(self):
        APP_DIR.mkdir(parents=True, exist_ok=True)
        self._key = None

    def has_existing_vault(self) -> bool:
        return SALT_FILE.exists() and DATA_FILE.exists()

    def create_vault(self, password: str) -> None:
        salt = generate_salt()
        SALT_FILE.write_bytes(salt)
        self._key = derive_key(password, salt)
        self.save_notes([])

    def unlock(self, password: str) -> bool:
        salt = SALT_FILE.read_bytes()
        key = derive_key(password, salt)
        try:
            decrypt(DATA_FILE.read_bytes(), key)
        except WrongPasswordError:
            return False
        self._key = key
        return True

    def load_notes(self) -> List[Note]:
        if self._key is None:
            raise RuntimeError("Vault is locked.")
        raw = decrypt(DATA_FILE.read_bytes(), self._key)
        items = json.loads(raw.decode("utf-8"))
        return [Note.from_dict(item) for item in items]

    def save_notes(self, notes: List[Note]) -> None:
        if self._key is None:
            raise RuntimeError("Vault is locked.")
        payload = json.dumps(
            [n.to_dict() for n in notes], ensure_ascii=False
        ).encode("utf-8")
        token = encrypt(payload, self._key)
        DATA_FILE.write_bytes(token)

    def change_password(self, new_password: str, notes: List[Note]) -> None:
        salt = generate_salt()
        SALT_FILE.write_bytes(salt)
        self._key = derive_key(new_password, salt)
        self.save_notes(notes)

    def lock(self) -> None:
        self._key = None
