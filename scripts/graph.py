import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo CSV
df = pd.read_csv('dataset.csv')

# Contar as ocorrências de cada valor na coluna 'tema' (ajuste o nome conforme necessário)
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
