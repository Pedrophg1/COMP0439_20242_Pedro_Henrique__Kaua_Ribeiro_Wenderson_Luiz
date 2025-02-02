import json
import psycopg2

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

# Atualizar os dados no banco
for issue in data:
    issue_id = issue.get("number")
    
    # Inicializar variável para armazenar a prioridade
    priority = None
    
    # Obter as labels
    labels = issue.get("labels", [])
    
    # Print para ver as labels (debug)
    print(f"Labels para issue {issue_id}: {labels}")
    
    for label in labels:
        label_name = label.get("name", "")
        
        # Verificar se a label contém a palavra "Priority"
        if "Priority" in label_name:
            # Extrair a prioridade (ex: Low, Medium, High)
            priority = label_name.split(']')[-1].strip()
            print(f"Prioridade encontrada: {priority}")  # Print para debug
            break
    
    if priority:  # Só atualiza se a prioridade for encontrada
        # Atualizar o campo 'priority' no banco de dados
        cursor.execute("""
            UPDATE issueschema.issues
            SET priority = %s
            WHERE issue_id = %s
        """, (priority, issue_id))

# Confirmar e fechar a conexão
conn.commit()
cursor.close()
conn.close()

print("Prioridades atualizadas com sucesso!")
