# 🔐 env-guardian
![Health-Hub](https://img.shields.io/badge/Health--Hub-%E2%9C%94-00D1FF?style=flat-square)

**Env-Guardian** is a secure utility for managing and synchronizing `.env` files across environments without compromising security. It ensures your secrets never leak to version control while keeping your team in sync.

## 🚀 Features

-   **🔒 Secure Protection**: Encrypts your `.env` into a `.env.secure` file using AES-256 (Fernet) encryption.
-   **🔓 One-Click Restore**: Decrypts and restores your environment variables instantly when needed.
-   **🛡️ Git Integration**: Automatically manages your `.gitignore` to prevent accidental key or secret leaks.
-   **🤝 Team Sync**: Safely commit `.env.secure` to your repo; only teammates with the master `.env.key` can unlock it.

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Raphasha27/env-guardian.git
cd env-guardian

# Install dependencies
pip install typer rich cryptography
```

## ⌨️ Usage

### Protect your secrets
```bash
python guardian.py protect
```

### Restore environment
```bash
python guardian.py restore
```

## 🛡️ Security Note
Never commit your `.env.key` to any repository. Store it in a secure password manager or share it with your team through encrypted channels.

---
*Built with ❤️ by Koketso Raphasha using DevForge AI.*
