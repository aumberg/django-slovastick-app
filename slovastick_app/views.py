# ~*~ coding: utf-8 ~*~

# you must relocate URL's "/favicon.ico" and "/robots.txt" to STATIC_URL

import urllib
import audio.audio, lib

from django.conf import settings

def index(request):
    #if test server
    if request.META.has_key('SERVER_SOFTWARE') \
        and 'WSGIServer/0.1 Python/2.7.3' == request.META["SERVER_SOFTWARE"] :
            request_uri = request.META["PATH_INFO"][1:] #without any question simbol

            if request_uri in ["favicon.ico", "robots.txt"] :
                return lib.response_text("")
    else :
        request_uri = urllib.unquote(request.META["REQUEST_URI"])
        request_uri = request_uri.decode('utf8')[1:]

    if 512 < len(request_uri) :
        text = "Limit max URI length expire, and Arnold Shvarcneger says: Get Out."

        return lib.response_text(text)

    TextToAudio = audio.audio.TextToAudio(request_uri)
    out = audio.audio.TextToAudio(request_uri).run()
    response = lib.response_audio(out)

    if not settings.DEBUG :
        lib.response_cache(response)

    return response