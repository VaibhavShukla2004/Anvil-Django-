import json
with open('../data/exercises.json', 'r') as f:
    data = json.load(f)

muscles = set()
equipment = set()

for d in data:
    for m in d.get('primary_muscles', []):
        muscles.add(m)
    for e in d.get('equipment', []):
        equipment.add(e)

print('Muscles:', sorted(list(muscles)))
print('Equipment:', sorted(list(equipment)))
