from pathlib import Path
import json

folder_path = Path("./Data/")

json_files = [{"file": file.name} for file in folder_path.glob("*.json")]

# Write the list to a JSON file
output_file = Path("file_array.json")

with output_file.open("w", encoding="utf-8") as f:
    json.dump(json_files, f, indent=4)

print("Written to file_array.json")