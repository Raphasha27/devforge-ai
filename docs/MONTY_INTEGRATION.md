# Ironclad Sandbox Integration - Docker-Free Code Execution

## Overview

This project now supports **Ironclad Sandbox** (powered by Pydantic Monty) as a secure, 
zero-container alternative to Docker for AI agent code execution.

### Why Ironclad?

| Feature | Docker | Ironclad Sandbox |
|---------|--------|------------------|
| Startup | ~200ms | 0.06ms |
| Memory | ~50MB | <1MB |
| Containers | Required | None |
| Cost | Variable | Free |

### How It Works

Ironclad Sandbox uses Pydantic's Monty -- a minimal Python interpreter written in 
**Rust** -- to run LLM-generated code directly in your process. It blocks unauthorized 
file system, network, and environment variable access at the interpreter level.

### Quick Start

```bash
pip install monty-python pydantic-ai
```

```python
from monty import Monty

sandbox = Monty()
result = sandbox.run("output = sorted([5, 3, 8, 1])")
print(result)  # [1, 3, 5, 8]
```

### Resources

- [Ironclad Sandbox](https://github.com/Raphasha27/ironclad-sandbox) - Our implementation
- [Pydantic Monty](https://github.com/pydantic/monty) - Underlying Rust interpreter
- [Pydantic AI](https://ai.pydantic.dev) - Agent framework
