import os

# Directory containing the .sql files
sql_folder = "."
# Output Python file
output_file = "eval_schemas.py"

def sanitize_variable_name(name):
    # Replace invalid characters with underscores and ensure it’s a valid Python identifier
    return ''.join(c if c.isalnum() or c == '_' else '_' for c in name).lstrip('0123456789')

sql_files = [f for f in os.listdir(sql_folder) if f.endswith(".sql")]

with open(output_file, "w", encoding="utf-8") as py_file:
    py_file.write("# Auto-generated SQL queries\n\n")
    for filename in sql_files:
        var_name = sanitize_variable_name(os.path.splitext(filename)[0])
        file_path = os.path.join(sql_folder, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        py_file.write(f"{var_name} = '''{content}'''\n\n")

print(f"Generated {output_file} with {len(sql_files)} SQL variables.")
