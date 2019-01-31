import yaml

with open("document.yaml", 'r') as stream:
    try:
        a = (yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)

print a["defaults"]
print a["defaults"]["volumes"]
for i in a["defaults"]["volumes"].keys():
    print i
    print a["defaults"]["volumes"][i]