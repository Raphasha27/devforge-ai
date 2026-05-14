import json
from app.core.llm import call_llm

def build_architecture(idea: dict):
    """
    Agent that designs the folder structure and tech stack for a repo.
    """
    prompt = f"""
    Design a production-ready architecture for the following project:
    Name: {idea['name']}
    Description: {idea['description']}
    
    Return ONLY a JSON object with:
    {{
        "stack": "Main programming language and key libraries",
        "structure": ["list/of/folders/", "list/of/files.py"],
        "entrypoint": "main file to run",
        "commands": {{ "install": "command", "run": "command", "test": "command" }}
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {
            "stack": "Python + Typer",
            "structure": ["src/main.py", "tests/test_main.py", "README.md", "requirements.txt"],
            "entrypoint": "src/main.py",
            "commands": { "install": "pip install -r requirements.txt", "run": "python src/main.py", "test": "pytest" }
        }

def generate_codebase(architecture: dict, idea: dict):
    """
    Agent that generates the actual code for all files in the architecture.
    """
    files = {}
    for file_path in architecture.get("structure", []):
        if file_path.endswith("/"): continue
        
        prompt = f"""
        Generate production-ready, clean code for the file: {file_path}
        Project: {idea['name']}
        Architecture: {architecture['stack']}
        
        Rules:
        - Include logging, error handling, and type hints.
        - If it's a test file, include useful test cases.
        - If it's a README, make it SEO optimized and professional.
        
        Return ONLY the raw file content.
        """
        files[file_path] = call_llm(prompt)
        
    return files
