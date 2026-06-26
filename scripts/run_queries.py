import os
import duckdb
import re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

DB_PATH       = "data/ecommerce.duckdb"
QUERIES_DIR   = "queries"
TEMPLATE_DIR  = "scripts"
TEMPLATE_FILE = "template.html"
OUTPUT_PATH   = "reports/index.html"

SECTIONS = [
    {"title": "Beginner",     "folder": "01_beginner"},
    {"title": "Intermediate", "folder": "02_intermediate"},
    {"title": "Advanced",     "folder": "03_advanced"},
]

def parse_comment_block(sql):
    """
    Extracts business_question and concept from the comment block
    at the top of each .sql file.
    """
    business_question = "N/A"
    concept           = "N/A"

    bq_match = re.search(r'--\s*Business question\s*:\s*(.+)', sql)
    cn_match  = re.search(r'--\s*Concept\s*:\s*(.+)', sql)

    if bq_match:
        business_question = bq_match.group(1).strip()
    if cn_match:
        concept = cn_match.group(1).strip()

    return business_question, concept

def run_query(con, sql):
    """
    Executes a SQL query and returns columns and rows.
    Skips the EXPLAIN prefix result and returns plan as rows.
    """
    try:
        result  = con.execute(sql).fetchdf()
        columns = list(result.columns)
        rows    = result.head(20).values.tolist()
        return columns, rows, None
    except Exception as e:
        return [], [], str(e)

def main():
    con = duckdb.connect(DB_PATH)

    sections_data = []

    for section in SECTIONS:
        folder_path = os.path.join(QUERIES_DIR, section["folder"])
        sql_files   = sorted(f for f in os.listdir(folder_path) if f.endswith(".sql"))

        queries_data = []
        for filename in sql_files:
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding = "utf-8") as f:
                sql = f.read()

            business_question, concept = parse_comment_block(sql)
            columns, rows, error       = run_query(con, sql)

            queries_data.append({
                "filename":          filename,
                "sql":               sql.strip(),
                "business_question": business_question,
                "concept":           concept,
                "columns":           columns,
                "rows":              rows,
                "error":             error,
            })

        sections_data.append({
            "title":   section["title"],
            "queries": queries_data,
        })

    con.close()

    env      = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(TEMPLATE_FILE)
    html     = template.render(
        sections=sections_data,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    os.makedirs("reports", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report generated at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()