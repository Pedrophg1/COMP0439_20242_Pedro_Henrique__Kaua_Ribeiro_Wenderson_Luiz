import json
import os
import re
import matplotlib.pyplot as plt

# Caminho absoluto do arquivo JSON
JSON_PATH = r"C:\Users\Dell\Documents\scriptsengsoft\scriptsengsoft-main\arquivos-usados\últimas_releases.json"

def classificar_versao(tag_name):
    match = re.match(r"v(\d+)\.(\d+)\.(\d+)(-rc\.\d+)?", tag_name)
    if match:
        major, minor, patch = map(int, match.groups()[:3])
        if match.group(4):
            return "Release Candidate"
        elif patch > 0:
            return "Patch"
        elif minor == 0 and patch == 0:
            return "Major"
        elif minor > 0 and patch == 0:
            return "Minor"
    return "Unknown"

def carregar_json():
    """Carrega o JSON do caminho fixo, tentando diferentes codificações."""
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except UnicodeDecodeError:
            print("Erro de codificação UTF-8. Tentando abrir com outra codificação...")
            with open(JSON_PATH, 'r', encoding='latin-1') as f:  # Alternativa para Windows
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar o arquivo JSON: {e}")
            return []
    else:
        print(f"Arquivo JSON não encontrado: {JSON_PATH}")
        return []


def contar_versoes(versoes):
    contagem = {"Major": 0, "Minor": 0, "Patch": 0, "Release Candidate": 0, "Unknown": 0}
    for release in versoes:
        tipo_versao = classificar_versao(release.get('tag_name', ''))
        contagem[tipo_versao] += 1
    return contagem

def gerar_grafico(contagem):
    contagem.pop("Unknown", None)
    plt.bar(contagem.keys(), contagem.values())
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
