# ~*~ coding: utf-8 ~*~

import subprocess, base64, logging, urllib, pprint, json, time, shlex, os
import slovastick_app.braille_json.braille_json as braille_json, slovastick_app.lib as lib
import django.conf

from slovastick_app.audio.audio_lib import get_score_standart

class TextToAudio:
    modules = {}
    # 
    argsProcSox = shlex.split('sox -t ircam - -t wav -')
    #
    tempo = 0.5
    # 
    timeStart = 0.5
    #
    csdOptions = "csound -d -m0 -R --format=ircam -o stdout ;--syntax-check-only /mnt/tmpfs/test.orc /mnt/tmpfs/test.sco"
    # 
    csdOptionsIns = """
    sr = 16000
    ksmps = 16
    nchnls = 2
    0dbfs = 1
    """
    #
    scoreLastWrap = "\ni \"silence\" %s 0.5 ;final pause 0.5 sec\n"
    # 
    csdWrap = """
<CsoundSynthesizer>
<CsOptions>
%(csdOptions)s 
</CsOptions>
<CsInstruments>
%(csdOptionsIns)s

instr silence
endin

%(instruments)s

</CsInstruments>
<CsScore>
%(score)s
e
</CsScore>
</CsoundSynthesizer>
"""

    def __init__(self, text="", settings={}):
            # for no debug all instruments modules saved in self.modules
            # if django.conf.settings.DEBUG :
            #     self.modules = {}

        self.modules = {}
        # 
        self.text = text
        self.instruments = ""
        self.score = ""

        if settings :
            if "tempo" in settings and settings["tempo"] in map(str,range(1,10)) :
                settings["tempo"] = 1.5 / int(settings["tempo"]) # 1/5
                self.tempo = int(round(settings["tempo"]))

    def run(self):
        if not self.text :
            return
        # # get score
        for info in braille_json.get(self.text) :
            #!!! encode back to utf8 for python 2.*
            for some in ["dots", "self"] :
                if some in info :
                    info[some] = info[some].encode('utf8')
            # 
            if "language" in info :
                lang = info["language"]
            else :
                lang = "global"

            insNames = []
            insNames.append("dots.%s.i1" % lang)

            # !!!not finaly part of code -->
            if "ru" == lang :
                insNames.append("alphabet.ru.i1")
            #
            for insName in insNames :
                if insName not in self.modules :
                    mod = {}
                    # trueName = self.instrumentName.replace("_", ".")
                    thePackagePath = lib.appName + ".audio." + insName 
                    fromlist = insName.rsplit(".", 1)[-1:]
                    
                    try :
                        mod = __import__(thePackagePath, fromlist=fromlist)
                        ins = mod.Instrument()
                        prefix = len(self.modules) + 1
                        prefix = str(prefix) if 10 > prefix else str(prefix * 10)

                        mod = {
                            "theInstrument": ins,
                            "insPrefix": prefix
                        }
                        # add instruments
                        self.instruments = self.instruments + \
                            ins.get_instrument({
                                "insPrefix": mod["insPrefix"]
                            })
                        # add init score
                        if hasattr(ins, "get_score_init") :
                            self.score = self.score + ins.get_score_init({
                                "insPrefix": mod["insPrefix"]
                            }) + "\n"

                        self.modules[insName] = mod
                    except Exception, e :
                        print thePackagePath
                        print "error !!!!! in get_score " + thePackagePath
                        print "---> ", e
                        continue

                mod = self.modules[insName]
                ins = mod["theInstrument"]

                settings = {
                    "insPrefix": mod["insPrefix"],
                    "iStart"   : self.timeStart,
                }

                if hasattr(ins, "get_score") :
                    self.score = self.score + ins.get_score(info, settings)
                else :
                    self.score = self.score + get_score_standart(info, settings)
            # ready to next time iteration
            self.timeStart = self.timeStart + self.tempo
        # pause at end of score
        self.score = self.score + self.scoreLastWrap % self.timeStart
        # limit filename and write to tmpfs
        strTime = str(time.time())
        partName = base64.b64encode(self.text[:10].encode('utf8'), ("+", "-"))
        theFilePath = os.path.join(lib.pathTmpfs, partName + strTime + ".csd")
        theFile = open(theFilePath, "w")

        theData = self.csdWrap % {
            "csdOptions": self.csdOptions,
            "csdOptionsIns": self.csdOptionsIns,
            "instruments": self.instruments,
            "score": self.score,
        }

        theFile.write(theData)
        theFile.close()
        pip     = subprocess.PIPE
        err     = None if django.conf.settings.DEBUG else pip
        proc    = subprocess.Popen(['csound', theFilePath], stdout=pip, stderr=err)
        proc2   = subprocess.Popen(self.argsProcSox, stdin=proc.stdout, stdout=pip, stderr=err)
        out     = proc2.communicate()[0]

        # delete file from tmpfs
        # !!!for debug in csound editor like qutesound, save this file,
        # and set output option to -odac 
        os.unlink(theFilePath)
        # 

        return out