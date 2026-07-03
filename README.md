# Encrypted Notes

A simple, modern desktop notes app built with **PySide6**. Every note is
encrypted on disk with a password only you know — not even the app can
read your notes without it.

## Features

- 🔒 **Real encryption** — AES (via Fernet) with a key derived from your
  master password using PBKDF2-HMAC-SHA256 (480,000 rounds). Nothing is
  stored in plaintext, and the password itself is never saved anywhere.
- 🔍 **Instant search** — filter notes by title or content as you type.
- 📝 **Autosave** — notes save automatically shortly after you stop typing.
- 🎨 **Modern dark UI** — clean sidebar + editor layout, styled with QSS.
- 🔐 **Lock button** — lock the vault without quitting the app; you'll be
  asked for your password again to get back in.

## Project structure

```
encrypted_notes/
├── main.py            # Entry point — starts the app and login/relogin flow
├── login_dialog.py     # Master password dialog (create vault / unlock)
├── main_window.py       # Main window: sidebar, search, editor, autosave
├── note_list_item.py     # Custom widget for each row in the note list
├── note_storage.py        # Reads/writes the encrypted vault file on disk
├── crypto_manager.py       # Key derivation + encrypt/decrypt (Fernet)
├── models.py                # The Note data class
├── styles.py                  # Shared modern dark QSS stylesheet
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
python main.py
```

On first launch you'll be asked to create a master password. This
password encrypts your notes — **if you forget it, your notes cannot be
recovered.** There is no backdoor by design.

## Where your data lives

Your encrypted vault is stored in your home folder:

```
~/.encrypted_notes/
├── salt.bin     # random salt used for key derivation (not secret, but needed)
└── notes.enc    # all your notes, encrypted as a single blob
```

## How the encryption works

1. A random 16-byte salt is generated once when you create your vault.
2. Your password + that salt go through PBKDF2-HMAC-SHA256 (480,000
   iterations) to produce a 256-bit key.
3. That key encrypts your notes with Fernet (AES-128-CBC + HMAC), which
   authenticates the ciphertext — so a wrong password is always detected
   instead of silently producing garbage.

Typing the wrong password never corrupts your data; it's simply rejected
and you're asked to try again.
