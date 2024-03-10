import json

with open('rhyme_analysis.json', 'r') as file:
    rhymes_data = json.load(file)

nodes = []
links = []
seen_words = set()

for word, rhymes in rhymes_data.items():
    if word not in seen_words:
        nodes.append({"id": word, "group": 1})
        seen_words.add(word)
    
    for rhyme in rhymes:
        if rhyme not in seen_words:
            nodes.append({"id": rhyme, "group": 2})
            seen_words.add(rhyme)
        
        links.append({"source": word, "target": rhyme, "value": 1})

graph_data = {"nodes": nodes, "links": links}

with open('network_data.json', 'w') as outfile:
    json.dump(graph_data, outfile, indent=4)

print("Network data has been saved to 'network_data.json'")
