import json
import psycopg2
from datetime import datetime

# Caminho do arquivo JSON
json_file = "listade_issues.json"

# Conectar ao PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="database",
    user="user",
    password="password"
)
cursor = conn.cursor()

# Abrir o arquivo JSON
with open(json_file, encoding="latin-1") as f:
    raw_data = f.read()

# Decodificar os dados para UTF-8
data = json.loads(raw_data.encode("utf-8", errors="replace").decode("utf-8"))

# Função para calcular o tempo de resolução em intervalo (dias)
def calcular_resolucao(created_at, closed_at):
    if created_at and closed_at:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        closed = datetime.fromisoformat(closed_at.replace("Z", "+00:00"))
        return closed - created  # Retorna um intervalo entre as datas
    return None

# Inserir os dados no banco
for issue in data:
    issue_id = issue.get("number")
    title = issue.get("title", "")
    body = issue.get("body", "")
    created_at = issue.get("createdAt")
    closed_at = issue.get("closedAt")
    resolution_time = calcular_resolucao(created_at, closed_at)
    priority = None  # Substitua com lógica, se necessário
    milestone = issue.get("milestone")
    author = issue.get("author", {}).get("login", "")
    assignee = ", ".join([a.get("login", "") for a in issue.get("assignees", [])])
    tema_relacionado = None  # Adicione lógica de classificação se necessário

    # Inserir no banco
    cursor.execute("""
        INSERT INTO issueschema.issues (
            issue_id, title, body, created_at, closed_at, resolution_time, 
            priority, milestone, author, assignee, tema_relacionado
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        issue_id, title, body, created_at, closed_at, resolution_time, 
        priority, milestone, author, assignee, tema_relacionado
    ))

# Confirmar e fechar a conexão
conn.commit()
cursor.close()
conn.close()

print("Dados inseridos com sucesso!")
