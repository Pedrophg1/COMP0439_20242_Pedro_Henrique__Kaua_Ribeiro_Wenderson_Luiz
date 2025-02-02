import json
import psycopg2
import unicodedata

# Caminho do arquivo JSON
json_file = "150-299.json"

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

def remover_acentos(texto):
    if texto:
        return ''.join(
            c for c in unicodedata.normalize('NFKD', texto)
            if unicodedata.category(c) != 'Mn'
        )
    return texto

# Atualizar os dados no banco
for issue in data:
    issue_id = issue.get("number")
    tema_relacionado = issue.get("tema_relacionado")
    
    if tema_relacionado:
        tema_relacionado = remover_acentos(tema_relacionado)
        cursor.execute(
            """
            UPDATE issueschema.issues
            SET tema_relacionado = %s
            WHERE issue_id = %s
            """,
            (tema_relacionado, issue_id)
        )

# Confirmar e fechar a conexão
conn.commit()
cursor.close()
conn.close()

print("Dados atualizados com sucesso!")
