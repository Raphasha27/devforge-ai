# 🛠️ git-oxide
![Health-Hub](https://img.shields.io/badge/Health--Hub-%E2%9C%94-00D1FF?style=flat-square)

**Git-Oxide** is a high-performance, smart git repository cleanup and optimization CLI. It helps developers maintain a lean, fast, and secure `.git` history by automating the pruning of stale branches and performing aggressive garbage collection.

## 🚀 Features

-   **🔍 Smart Scan**: Automatically identifies merged local branches that are no longer needed.
-   **🧹 Atomic Cleanup**: Deletes stale branches and prunes remote-tracking references in one go.
-   **⚙️ Aggressive Optimization**: Runs `git gc --aggressive` to compress repository size and improve performance.
-   **🛡️ Safety First**: Interactive confirmation for all destructive actions (can be bypassed with `--force`).

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Raphasha27/git-oxide.git
cd git-oxide

# Install dependencies
pip install typer rich
```

## ⌨️ Usage

### Scan for bloat
```bash
python oxide.py scan
```

### Perform cleanup
```bash
python oxide.py clean
```

## 🤝 Contributing
Contributions are welcome! If you have ideas for new optimization features, feel free to open an issue or a PR.

---
*Built with ❤️ by Koketso Raphasha using DevForge AI.*
