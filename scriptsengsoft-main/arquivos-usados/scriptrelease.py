import json
import os
import re
from collections import Counter
import matplotlib.pyplot as plt


script_dir = os.path.dirname(os.path.abspath(__file__))


json_file = os.path.join(script_dir, 'últimas_releases.json')


with open(json_file, 'r') as file:
    parsed_data = json.load(file)


contributors_count = Counter()


contributor_regex = r'@([a-zA-Z0-9_-]+)'


for release in parsed_data:
    body = release.get('body', '')  
    contributors = re.findall(contributor_regex, body)
    
    contributors_count.update(contributors)

for contributor, count in contributors_count.items():
    print(f'{contributor} apareceu em {count} releases')

sorted_contributors = sorted(contributors_count.items(), key=lambda x: x[1], reverse=True)

contributors_sorted = [item[0] for item in sorted_contributors]
counts_sorted = [item[1] for item in sorted_contributors]


plt.figure(figsize=(10, 6))
plt.bar(contributors_sorted, counts_sorted, color='skyblue')
plt.xlabel('Contribuidores')
plt.ylabel('Número de Releases')
plt.title('Número de Releases por Contribuidor')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
