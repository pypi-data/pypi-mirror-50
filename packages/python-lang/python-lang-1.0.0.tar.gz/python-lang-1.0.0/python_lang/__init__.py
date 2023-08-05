import os
import xml.etree.ElementTree as et

langs = {}
selected = None
file = None

def get(text):
    if file:
        for t in file.iter("translation"):
            if t.attrib["text"] == text:
                return t.text
    return text

def add(path, code=None):
    global file
    global selected
    if os.path.isfile(path):
        root = et.parse(path).getroot()
        if not code:
            if "code" in root.attrib:
                code = root.attrib["code"]
            else:
                code = str(len(langs)+1)
        langs[code[:2]] = path
        return True
    else:
        return False

def select(lang=None):
    global file
    global selected
    if lang:
        if langs[lang]:
            if os.path.isfile(langs[lang]):
                file = et.parse(langs[lang]).getroot()
                selected = lang
                return True
            else:
                return False
        else:
            return False
    else:
        file = None
        selected = None
        return True

def all():
    return list(lang for lang in langs)