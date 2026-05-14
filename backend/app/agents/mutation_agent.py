from app.core.llm import call_llm

def generate_mutation_code(repo_content: dict, mutation_plan: str):
    """
    Agent that performs the actual code mutation based on an evolution plan.
    """
    mutated_files = {}
    
    for path, content in repo_content.items():
        if path.endswith(".py"):
            prompt = f"""
            You are a senior evolution engineer at DevForge AI.
            Apply the following mutation plan to this file:
            Plan: {mutation_plan}
            
            File: {path}
            Content:
            {content}
            
            Rules:
            - Do not break existing functionality.
            - Follow the plan strictly.
            - Return ONLY the updated code.
            """
            mutated_files[path] = call_llm(prompt)
        else:
            mutated_files[path] = content
            
    return mutated_files
