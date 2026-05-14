from app.core.llm import call_llm
import json

def scan_repo_intelligence(repo_name: str, files: dict):
    """
    Agent that scans repository contents to extract technical intelligence.
    Identifies hidden dependencies, tech stack nuances, and shared patterns.
    """
    intelligence = {
        "repo": repo_name,
        "tech_stack": [],
        "inferred_dependencies": [],
        "shared_patterns": [],
        "refactor_suggestions": []
    }
    
    # Concatenate snippets of logic files for scanning
    snippets = ""
    for path, content in list(files.items())[:5]: # Limit to first 5 files
        if path.endswith((".py", ".js", ".ts", ".go")):
            snippets += f"\nFile: {path}\n---\n{content[:500]}\n---"
            
    prompt = f"""
    Analyze the technical structure of the repository '{repo_name}' based on these file snippets:
    {snippets}
    
    Extract:
    1. Primary technology stack (languages, frameworks).
    2. Deep dependencies (beyond what's in requirements/package.json).
    3. Potential shared patterns that could be extracted into a common library.
    4. Urgent refactor areas.
    
    Return ONLY a JSON object:
    {{
        "stack": ["list"],
        "dependencies": ["list"],
        "patterns": ["list"],
        "refactors": ["list"]
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        data = json.loads(response)
        intelligence["tech_stack"] = data.get("stack", [])
        intelligence["inferred_dependencies"] = data.get("dependencies", [])
        intelligence["shared_patterns"] = data.get("patterns", [])
        intelligence["refactor_suggestions"] = data.get("refactors", [])
    except:
        pass
        
    return intelligence
