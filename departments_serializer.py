
import os
import json

departments = {} # type: dict
abbreviation = False
def serialize_dep_file(file, language):
    departments = {} # type: dict
    abbreviation = False
    with open(file) as f:
        lines = f.readlines()
        for i in range(0, len(lines) -1):
            if lines[i] == "\n":
                if i == len(lines) -2 and lines[i+1] != "\n":
                    line = lines[i+1].strip("\n")
                    departments[line] = {
                        'name': line,
                        'abbreviation': 'null'
                    }
                abbreviation = False
            elif lines[i + 1] != "\n":
                line = lines[i].strip("\n")
                departments[line] = {
                    'name': line,
                    'abbreviation': lines[i+1].strip("\n")
                }
                abbreviation = True
            elif lines[i + 1] == "\n" and abbreviation == False:
                line = lines[i].strip("\n")
                departments[line] = {
                    'name': line,
                    'abbreviation': 'null'
                }
    with open(f"./src/static/data/departments_{language}.json", "w+", encoding="utf-8") as f:
        f.write(json.dumps(departments, ensure_ascii= False))

serialize_dep_file("./src/static/data/departments_en.txt", "en")
serialize_dep_file("./src/static/data/departments_fr.txt", "fr")



