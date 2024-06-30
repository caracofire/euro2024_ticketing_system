import os

# Define the base directory
base_dir = "C:\\Users\\Leonardo\\Desktop\\euro2024_ticketing_system"

# Define the directory structure
dirs = [
    os.path.join(base_dir, "data"),
    os.path.join(base_dir, "modules")
]

# Define the files to be created
files = [
    os.path.join(base_dir, "data", "teams.json"),
    os.path.join(base_dir, "data", "stadiums.json"),
    os.path.join(base_dir, "data", "matches.json"),
    os.path.join(base_dir, "modules", "__init__.py"),
    os.path.join(base_dir, "modules", "match_management.py"),
    os.path.join(base_dir, "modules", "ticket_sales.py"),
    os.path.join(base_dir, "modules", "attendance_management.py"),
    os.path.join(base_dir, "modules", "restaurant_management.py"),
    os.path.join(base_dir, "modules", "restaurant_sales.py"),
    os.path.join(base_dir, "modules", "statistics.py"),
    os.path.join(base_dir, "main.py"),
    os.path.join(base_dir, "requirements.txt"),
    os.path.join(base_dir, "README.md")
]

# Create directories
for dir in dirs:
    os.makedirs(dir, exist_ok=True)

# Create files
for file in files:
    open(file, 'w').close()

print("Project structure created successfully.")
