import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Configuração da conexão com o banco de dados
DB_HOST = "localhost"
DB_PORT = "5432"  # Porta padrão do PostgreSQL
DB_NAME = "Issues_db"
DB_USER = "pedroadmin"
DB_PASSWORD = "@dmin159"

# Criar a conexão com o banco de dados usando psycopg2
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Consulta SQL para buscar a coluna 'tema_relacionado' da tabela desejada
query = "SELECT tema_relacionado FROM issueschema.issues"

# Carregar os dados do banco diretamente para um DataFrame Pandas
df = pd.read_sql(query, conn)

# Fechar a conexão com o banco de dados
conn.close()

# Contar as ocorrências de cada valor na coluna 'tema_relacionado'
contagem_temas = df['tema_relacionado'].value_counts()

# Criar o gráfico de barras
plt.figure(figsize=(10, 6))
ax = contagem_temas.plot(kind='bar', color='skyblue')

# Adicionar títulos e rótulos aos eixos
plt.ylabel('Quantidade de Ocorrências')
plt.title('Frequência dos Temas')

# Adicionar os números em cima de cada barra
for i, v in enumerate(contagem_temas):
    ax.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=8)

# Ajuste dos rótulos do eixo X para evitar sobrecarga
plt.xticks(rotation=45, ha='right')

# Ajustar layout para que tudo fique bem posicionado
plt.tight_layout()

# Exibir o gráfico
plt.show()
