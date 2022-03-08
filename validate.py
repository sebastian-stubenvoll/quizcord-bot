import yaml
import json

quiz = input('Type a quiz name (e.g. test.yaml)')

with open(quiz, "r") as stream:
    try:
        print(json.dumps(yaml.safe_load(stream), indent=4))
    except yaml.YAMLError as e:
        print(e)


