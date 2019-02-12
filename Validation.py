from pykwalify.core import Core
import yaml


with open('boxes.yaml', 'r') as file:
    boxes = yaml.load(file)

print boxes
for i in boxes.keys():
    print i

c = Core(source_file="boxes.yaml", schema_files=["schema.yaml"])
c.validate(raise_exception=True)

