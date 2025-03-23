import json
import os
import re
from collections import Counter
import matplotlib.pyplot as plt

# Obtém o caminho do diretório onde o script está localizado
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define o nome do arquivo JSON
json_file = os.path.join(script_dir, 'últimas_releases.json')

# Carregar o JSON a partir do arquivo
with open(json_file, 'r') as file:
    parsed_data = json.load(file)

# Contar os contribuidores
contributors_count = Counter()

# Expressão regular para identificar os nomes dos contribuidores
contributor_regex = r'@([a-zA-Z0-9_-]+)'

# Iterar sobre cada release
for release in parsed_data:
    body = release.get('body', '')  # Pega o corpo da release
    # Encontrar todos os nomes de usuários no corpo usando regex
    contributors = re.findall(contributor_regex, body)
    # Atualizar o contador com os contribuidores dessa release
    contributors_count.update(contributors)

# Mostrar a quantidade de vezes que cada contribuinte aparece
for contributor, count in contributors_count.items():
    print(f'{contributor} apareceu em {count} releases')

# Ordenar os contribuidores por número de contribuições (decrescente)
sorted_contributors = sorted(contributors_count.items(), key=lambda x: x[1], reverse=True)

# Separar os dados ordenados
contributors_sorted = [item[0] for item in sorted_contributors]
counts_sorted = [item[1] for item in sorted_contributors]

# Criar um gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(contributors_sorted, counts_sorted, color='skyblue')
plt.xlabel('Contribuidores')
plt.ylabel('Número de Releases')
plt.title('Número de Releases por Contribuidor')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
