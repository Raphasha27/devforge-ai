import typer
import os
import shutil
from rich.console import Console
from cryptography.fernet import Fernet

app = typer.Typer(help="Env-Guardian: Secure .env management and synchronization.")
console = Console()

def get_key():
    key_path = ".env.key"
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as f:
            f.write(key)
        console.print("[yellow]🔑 New encryption key generated in .env.key[/yellow]")
        # Add to .gitignore
        if os.path.exists(".gitignore"):
            with open(".gitignore", "a") as f:
                f.write("\n.env.key\n")
    with open(key_path, "rb") as f:
        return f.read()

@app.command()
def protect():
    """
    Encrypts the .env file and prepares it for safe storage.
    """
    if not os.path.exists(".env"):
        console.print("[red]Error: .env file not found.[/red]")
        return
        
    key = get_key()
    fernet = Fernet(key)
    
    with open(".env", "rb") as f:
        data = f.read()
        
    encrypted = fernet.encrypt(data)
    with open(".env.secure", "wb") as f:
        f.write(encrypted)
        
    console.print("[bold green]🔒 .env file encrypted to .env.secure[/bold green]")
    console.print("[dim]You can now safely commit .env.secure to your repo.[/dim]")

@app.command()
def restore():
    """
    Restores the .env file from the secure version.
    """
    if not os.path.exists(".env.secure"):
        console.print("[red]Error: .env.secure file not found.[/red]")
        return
        
    key = get_key()
    fernet = Fernet(key)
    
    with open(".env.secure", "rb") as f:
        encrypted = f.read()
        
    try:
        decrypted = fernet.decrypt(encrypted)
        with open(".env", "wb") as f:
            f.write(decrypted)
        console.print("[bold green]🔓 .env file restored successfully.[/bold green]")
    except Exception:
        console.print("[red]Error: Decryption failed. Check your .env.key file.[/red]")

if __name__ == "__main__":
    app()
