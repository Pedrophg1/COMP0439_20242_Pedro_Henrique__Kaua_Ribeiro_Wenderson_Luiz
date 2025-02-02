import json
import psycopg2

# Caminho do arquivo JSON
json_file = "listade_issues.json"

# Conectar ao PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="Issues_db",
    user="postgres",
    password="@dmin159"
)
cursor = conn.cursor()

# Abrir o arquivo JSON
with open(json_file, encoding="latin-1") as f:
    raw_data = f.read()

# Decodificar os dados para UTF-8
data = json.loads(raw_data.encode("utf-8", errors="replace").decode("utf-8"))

# Atualizar os dados no banco
for issue in data:
    issue_id = issue.get("number")
    
    # Extrair as descrições dos labels
    labels = issue.get("labels", [])
    descriptions = [label.get("description", "") for label in labels]
    description_text = " | ".join(descriptions)  # Concatenar as descrições
    
    # Atualizar o campo 'body' com as descrições no banco
    cursor.execute("""
        UPDATE issueschema.issues
        SET body = %s
        WHERE issue_id = %s
    """, (description_text, issue_id))

# Confirmar e fechar a conexão
conn.commit()
cursor.close()
conn.close()

print("Dados atualizados com sucesso!")
