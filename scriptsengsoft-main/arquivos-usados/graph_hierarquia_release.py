import json
import re
import matplotlib.pyplot as plt

def classificar_versao(tag_name):
    match = re.match(r"v(\d+)\.(\d+)\.(\d+)(-rc\.\d+)?", tag_name)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3))
        
        if match.group(4):
            return "Release Candidate"
        elif patch > 0:
            return "Patch"
        elif minor == 0 and patch == 0:
            return "Major"
        elif minor > 0 and patch == 0:
            return "Minor"
        else:
            return "Patch"
    return "Unknown"

def carregar_json():
    try:
        with open('últimas_releases.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar o arquivo JSON: {e}")
        return []

def contar_versoes(versoes):
    contagem = {"Major": 0, "Minor": 0, "Patch": 0, "Release Candidate": 0}
    
    for release in versoes:
        if 'tag_name' in release:
            tipo_versao = classificar_versao(release['tag_name'])
            if tipo_versao in contagem:
                contagem[tipo_versao] += 1
            else:
                contagem["Unknown"] += 1
        else:
            contagem["Unknown"] += 1
    
    return contagem

def gerar_grafico(contagem):
    if "Unknown" in contagem:
        del contagem["Unknown"]

    categorias = list(contagem.keys())
    valores = list(contagem.values())
    
    plt.bar(categorias, valores)
    plt.title('Distribuição das versões de Release')
    plt.xlabel('Tipo de versão')
    plt.ylabel('Quantidade')
    plt.show()

def main():
    versoes = carregar_json()
    if versoes:
        contagem = contar_versoes(versoes)
        gerar_grafico(contagem)
    else:
        print("Não foi possível carregar as versões do arquivo.")

if __name__ == "__main__":
    main()
