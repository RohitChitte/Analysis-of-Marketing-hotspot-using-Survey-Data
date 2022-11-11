import os
from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
from flask_cors import CORS, cross_origin
import shutil, os
import json
import pandas

from file_ai_speech_to_text.transcriptGenerator import generateTranscript
from file_ai_spellingcorrector.spellcorrector import spell_corrector
from file_ai_keywordspotter.keywordSpotter import AddMultiKeywords


app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True


class ClientService:
    def __init__(self):
        self.FolderPath = "InputFiles"
        self.fileList = os.listdir(self.FolderPath)
        self.separatedOutputFiles = "./SeparatedOutputFiles"
        self.outputText = {}

    def processAudioFile(self):
        outputResponseObj = {}
        for val in self.fileList:
            inputFileTranscriptedOp = generateTranscript(os.path.join(self.FolderPath,val), self.separatedOutputFiles)

        outputResponseObj["inputFileTranscriptedOp"] = inputFileTranscriptedOp

        spellCorrectedOpMap = {}
        for val in inputFileTranscriptedOp.keys():
            spellcorrectedOp = spell_corrector(inputFileTranscriptedOp[val])

            spellCorrectedOpMap[val] = spellcorrectedOp
            # inputFileTranscriptedOp[val] = spellcorrectedOp
        outputResponseObj["spellCorrectedOpMap"] = spellCorrectedOpMap


        extractedKeywordMap = {}
        extractedKeywordMap_2 = {}
        for val in inputFileTranscriptedOp.keys():
            adding = AddMultiKeywords(inputFileTranscriptedOp[val],
                                      {"place": ["england"],
                                       "team": ["manchester united"],
                                       "game": ["football"]})
            result = adding.addkey()
            extractedKeywordMap[val] = result
            result_2 = adding.key_value()
            extractedKeywordMap_2[val] = result_2
        newoutputdict = {}
        newoutputdict_2 = {}

        for i in extractedKeywordMap.keys():
            if extractedKeywordMap[i] != []:
                newoutputdict[i] = extractedKeywordMap[i]

        for i in extractedKeywordMap_2.keys():
            if extractedKeywordMap_2[i] != {}:
                newoutputdict_2[i] = extractedKeywordMap_2[i]



        outputResponseObj["extractedKeywors"] = newoutputdict
        outputResponseObj["extractedKeywors_2"] = newoutputdict_2

        return outputResponseObj


inputFileDir = "./InputFiles"
archiveDir = './ArchivedInputFiles'


def archiveOldInputFiles():
    files = os.listdir(inputFileDir)
    for f in files:
        if os.path.exists(os.path.join(archiveDir, f)):
            os.remove(os.path.join(archiveDir, f))
        shutil.move(os.path.join(inputFileDir, f), archiveDir)


@app.route("/", methods=["GET"])
def homePage():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def getInputFIle():
    opReap = {}
    try:
        inputFile = request.files.get('file')
        archiveOldInputFiles()
        inputFile.save(os.path.join("InputFiles", inputFile.filename))
    except Exception as e:
        opReap["outputError"] = str(e)
        jsonStr = json.dumps(opReap, ensure_ascii=False).encode('utf8')
        return Response(jsonStr.decode())
    opReap["output"] = "Successfully uploaded the file"
    jsonStr = json.dumps(opReap, ensure_ascii=False).encode('utf8')
    return Response(jsonStr.decode())

@app.route("/startprocessing")
def render_html():
    opResponseObj = clntApp.processAudioFile()
    jsonStr = json.dumps(opResponseObj, ensure_ascii=False).encode('utf8')
    #print(opResponseObj)
    output_1 = opResponseObj["inputFileTranscriptedOp"]
    output_2 = opResponseObj["spellCorrectedOpMap"]
    #output_3 = opResponseObj["extractedKeywors"]
    output_3 = opResponseObj["extractedKeywors_2"]
    return render_template("index2.html", output_1=output_1,output_2=output_2,output_3=output_3)



if __name__ == "__main__":
    clntApp = ClientService()
    app.run(debug=True,port=5000)