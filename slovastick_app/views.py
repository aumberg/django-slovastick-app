# ~*~ coding: utf-8 ~*~

import re, os
import urllib
import audio.audio, lib

from datetime       import datetime, timedelta
from django.conf    import settings

def hello(request):
    accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    lang = "En" 

    if re.search("ru", accept) :
        lang = "Ru"

    thePath = os.path.join(lib.pathStatic, "hello" + lang + ".wav")
    theFile = open(thePath, "r")
    audio = theFile.read()
    theFile.close()

    return lib.response_cache(lib.response_audio(audio))

def index(request, text=""):
    text = urllib.unquote_plus(text.decode('ascii').encode('utf-8')).decode('utf-8')

    if 50 < len(text) :
        text = "Limit max URI length expire, and Arnold Shvarcneger says: Get Out."

        return lib.response_text(text)

    response = lib.response_audio(audio.audio.TextToAudio(text).run())

    if not settings.DEBUG :
        lib.response_cache(response)
    
    return response