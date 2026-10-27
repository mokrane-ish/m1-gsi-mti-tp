import csv

def csv_to_nested_dict(csv_file):
    """Reads modules.csv into a nested dictionary structure (semester -> unit -> list of modules)."""
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

def modules_to_html(data):
    """Converts the nested dictionary data into an HTML document with tables."""
    html = [
        '<!DOCTYPE html>',
        '<html><head><meta charset="utf-8"><title>M1 GSI Canvas</title>',
        '<style>',
        'body { font-family: Arial, sans-serif; margin: 20px; }',
        'table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }',
        'th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }',
        'th { background-color: #4CAF50; color: white; }',
        'tr:nth-child(even){ background-color: #f2f2f2; }',
        '</style>',
        '</head><body>'
    ]
    
    for semester, unites in data.items():
        html.append(f"<h2>Semester {semester}</h2>")
        for unite, modules in unites.items():
            html.append(f"<h3>Unit: {unite}</h3>")
            html.append("<table>")
            html.append("<tr><th>Module Code</th><th>Title</th><th>Coef</th><th>Credit</th>"
                        "<th>TP %</th><th>TD %</th><th>Exam %</th></tr>")
            
            for info in modules:
                html.append("<tr>")
                html.append(f"<td>{info['module_name']}</td>")
                html.append(f"<td>{info['module_title']}</td>")
                html.append(f"<td>{info['coef']}</td>")
                html.append(f"<td>{info['credit']}</td>")
                html.append(f"<td>{info['percent_tp']:.0f}%</td>")
                html.append(f"<td>{info['percent_td']:.0f}%</td>")
                html.append(f"<td>{info['percent_exam']:.0f}%</td>")
                html.append("</tr>")
            
            html.append("</table>")
            html.append("<hr>")
            
    html.append("</body></html>")
    return "\n".join(html)

if __name__ == "__main__":
    filename = "modules.csv"
    
    # 1. Load data
    result = csv_to_nested_dict(filename)
    
    # 2. Generate HTML text
    html_content = modules_to_html(result)
    
    # 3. Save to file
    with open("modules.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("HTML file successfully generated: modules.html")