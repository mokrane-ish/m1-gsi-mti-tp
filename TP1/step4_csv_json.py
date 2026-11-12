import csv
import json

def csv_to_nested_dict(csv_file):
    """Reads CSV and returns a 2-level nested dict (semester -> unit -> list of modules)."""
    data = {"S1": {}, "S2": {}}
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            semester = row['semestre'].strip()
            unite = row['unite'].strip()
            
            module = {
                "module_name": row['module_name'].strip(),
                "module_title": row['module_title'].strip(),
                "coef": int(row['coef']),
                "credit": int(row['credit']),
                "percent_tp": float(row['percent_tp']),
                "percent_td": float(row['percent_td']),
                "percent_exam": float(row['percent_exam'])
            }
            
            if unite not in data[semester]:
                data[semester][unite] = []
            data[semester][unite].append(module)
            
    return data

def csv_to_3level_dict(csv_file):
    """Modifies the dictionary structure to use 3 key levels (semester -> unit -> module_name)."""
    data = {}
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            semester = row['semestre'].strip()
            unite = row['unite'].strip()
            mod_name = row['module_name'].strip()

            if semester not in data:
                data[semester] = {}
            if unite not in data[semester]:
                data[semester][unite] = {}

            data[semester][unite][mod_name] = {
                "module_title": row['module_title'].strip(),
                "coef": int(row['coef']),
                "credit": int(row['credit']),
                "percent_tp": float(row['percent_tp']),
                "percent_td": float(row['percent_td']),
                "percent_exam": float(row['percent_exam'])
            }
    return data

if __name__ == "__main__":
    filename = "modules.csv"
    
    # 2-level dictionary
    dict_2level = csv_to_nested_dict(filename)
    
    # 3-level dictionary (semester -> unit -> module)
    dict_3level = csv_to_3level_dict(filename)
    
    # Display result as formatted JSON
    print("--- Data Formatted as JSON (3 Levels) ---")
    json_output = json.dumps(dict_3level, indent=4, ensure_ascii=False)
    print(json_output)