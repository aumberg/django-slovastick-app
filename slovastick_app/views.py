# ~*~ coding: utf-8 ~*~

# you must relocate URL's "/favicon.ico" and "/robots.txt" to STATIC_URL

import subprocess, base64, logging, urllib, pprint, json, time
import braille_json, audio.audio
import django.conf

from datetime import datetime, timedelta
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render_to_response

def hello(request):
    return redirect('/static/slovastick_app/hello.wav')

def index(request):
    #if test server
    if request.META.has_key('SERVER_SOFTWARE') \
        and 'WSGIServer/0.1 Python/2.7.3' == request.META["SERVER_SOFTWARE"] :
            request_uri = request.META["PATH_INFO"][1:] #without any question simbol
            if request_uri in ["favicon.ico", "robots.txt"] :
                return HttpResponse("")
    else :
        request_uri = urllib.unquote(request.META["REQUEST_URI"])
        request_uri = request_uri.decode('utf8')[1:]

    if 512 < len(request_uri) :
        text = "Limit max URI length expire, and Arnold Shvarcneger says: Get Out."

        return HttpResponse(text, content_type="text/plain")

    # logging.info(request_uri)
    # pprint.pprint(braille_json.get(u"⠛"))
    # logging.info(braille_json.get(request_uri[1:2], "unicode"))
    # print pprint.pformat(braille_json.get(request_uri))
    # return HttpResponse(pprint.pformat(braille_json.get(request_uri)))

    TextToAudio = audio.audio.TextToAudio(request_uri)
    out = audio.audio.TextToAudio(request_uri).run()
    response = HttpResponse(out, content_type='audio/x-wav')
    response['Content-Length']  = len(out)

    if not django.conf.settings.DEBUG :  
        expires = datetime.utcnow() + timedelta(minutes=2)
        response['Cache-Control']   = "public, max-age=7200" #2 minutes
        response['Expires']         = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")

    return response