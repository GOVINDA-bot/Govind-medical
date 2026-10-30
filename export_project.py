import os
import shutil
import zipfile

def export_mediverse():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(root_dir, "MediVerse_Export.zip")
    
    if os.path.exists(zip_path):
        os.remove(zip_path)

    print(f"Preparing MediVerse export bundle into: {zip_path}")
    
    # Files to include
    include_root_files = [
        "README.md",
        "PROJECT_DOCUMENTATION.md",
        "requirements.txt",
        ".gitignore",
        "start_server.bat",
        "start_server.sh"
    ]
    
    # Directories to include (and exclusions)
    ignore_patterns = {
        "node_modules",
        "__pycache__",
        ".git",
        ".DS_Store",
        "Thumbs.db",
        "MediVerse_Export.zip",
        "export_project.py"
    }

    count = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add root files
        for fname in include_root_files:
            fpath = os.path.join(root_dir, fname)
            if os.path.exists(fpath):
                zipf.write(fpath, arcname=fname)
                count += 1
                print(f"  + Added: {fname}")

        # Add backend
        backend_dir = os.path.join(root_dir, "backend")
        for root, dirs, files in os.walk(backend_dir):
            dirs[:] = [d for d in dirs if d not in ignore_patterns]
            for file in files:
                if file not in ignore_patterns and not file.endswith(".pyc"):
                    full_p = os.path.join(root, file)
                    rel_p = os.path.relpath(full_p, root_dir)
                    zipf.write(full_p, arcname=rel_p)
                    count += 1

        # Add frontend
        frontend_dir = os.path.join(root_dir, "frontend")
        for root, dirs, files in os.walk(frontend_dir):
            dirs[:] = [d for d in dirs if d not in ignore_patterns]
            for file in files:
                if file not in ignore_patterns:
                    full_p = os.path.join(root, file)
                    rel_p = os.path.relpath(full_p, root_dir)
                    zipf.write(full_p, arcname=rel_p)
                    count += 1

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"\n[SUCCESS] Successfully packaged {count} files into MediVerse_Export.zip ({size_mb:.2f} MB)")

if __name__ == "__main__":
    export_mediverse()
