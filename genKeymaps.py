#!/usr/bin/env python3
import json
import os

files = []
docPath = './docs/'
rawFileBaseURL = 'https://raw.githubusercontent.com/mayankmetha/Rucky-KeyMap/main/'
pagesFileBaseURL = 'https://mayankmetha.github.io/Rucky-KeyMap/'
versionRecord = {}

def findFiles():
    tmpList = [os.path.join(docPath,f) for f in os.listdir(docPath) if os.path.isfile(os.path.join(docPath,f))]
    files.extend(list(set(tmpList).difference(set([os.path.join(docPath,f) for f in ['index.md','_config.yml']]))))
    appendHIDDocs()

def appendHIDDocs():
    header = '''## Rucky HID Keymaps\n\nSl. No.|HID Name|Rucky HID Config File\n:---:|:---:|:---:\n'''
    for _ in range(len(files)):
        line = str(int(_+1))+"|"
        filename = files[_].split("/")[-1].replace(".md","")
        line += "["+filename.replace("_"," ").upper()+"]("+pagesFileBaseURL+filename+")|["+filename+".json]("
        line += pagesFileBaseURL+filename+".json)\n"
        header += line
    file = open(os.path.join(docPath,'index.md'),'w')
    file.write(header)
    file.close()
    generateHIDKeymapFiles()

def generateHIDKeymapFiles():
    for f in files:
        mdFile = open(f,'r',encoding="utf-8")
        jsonFile = open(f.split("/")[-1].replace(".md",".json"),'w')
        jsonObj = {}
        mapping = {}

        for _ in mdFile.readlines():
            if "Version" in _:
                jsonObj['version'] = _.strip().split(" ")[2]
                versionRecord[f.split("/")[-1].replace(".md","").upper()] = _.strip().split(" ")[2]
            if "0x" in _:
                if "\\|" in _:
                    _ = _.replace("\|","[pipe]")
                line = _.replace("\n","").split("|")
                if(len(line) != 8):
                    line.append("")
                modifiers = {
                    'ctrl': line[3].replace(" ",""),
                    'shift': line[4].replace(" ",""),
                    'alt': line[5].replace(" ",""),
                    'meta': line[6].replace(" ","")
                }
                key = {
                    'name': line[7],
                    'keycode': line[2].replace("0x",""),
                    'modifier': modifiers
                }
                mapping[line[1]] = key

        mdFile.close()
        jsonObj['mapping'] = mapping

        jsonFile.write(json.dumps(jsonObj, ensure_ascii=False).replace("\\\\","\\"))
        jsonFile.close()
    generateKeymapList()

def generateKeymapList():
    jsonArray = []
    for f in files:
        name = f.split("/")[-1].replace(".md","").upper()
        jsonObj = {
            'name': name.replace("_"," "),
            'revision': versionRecord[name],
            'filename': f.split("/")[-1].replace(".md",".json"),
            'url': rawFileBaseURL+f.split("/")[-1].replace(".md",".json")
        }
        jsonArray.append(jsonObj)
    file = open('keymap.json','w')
    file.write(json.dumps(jsonArray))
    file.close()

if __name__ == '__main__':
    findFiles()