from app.core.llm import call_llm

def generate_mutation_code(repo_name: str, current_files: dict, mutation_plan: str):
    """
    Agent that generates mutated code for an existing repository based on an evolution plan.
    """
    mutated_files = {}
    
    # In a real scenario, we would only refactor specific files.
    # For v1, we'll ask the LLM to provide a full updated codebase or patches.
    # To keep it simple, let's just refactor the main logic files.
    
    for path, content in current_files.items():
        if path.endswith(".py") or path.endswith(".js") or path.endswith(".ts"):
            prompt = f"""
            Refactor the following file as part of a '{mutation_plan}' evolution for the repository '{repo_name}'.
            
            Current File Path: {path}
            Current Content:
            ---
            {content}
            ---
            
            Mutation Plan: {mutation_plan}
            
            Rules:
            - Maintain existing functionality but apply the mutation plan.
            - Ensure high code quality, type safety, and clean architecture.
            - Return ONLY the updated raw file content.
            """
            mutated_files[path] = call_llm(prompt)
        else:
            # Keep non-logic files as they are (or maybe update README)
            mutated_files[path] = content
            
    return mutated_files
