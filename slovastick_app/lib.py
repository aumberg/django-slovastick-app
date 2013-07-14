# please mount tmpfs to tmpfs folder there
# it's spike for fast creation .csd files in Csound
# in linux: sudo mount tmpfs path_to_folder/tmpfs -t tmpfs -o size=8m
import shlex, os

from datetime import datetime, timedelta
from django.http import HttpResponse
from django.conf import settings

appName         = "slovastick_app"
pathThis        = os.path.abspath(os.path.dirname(__file__))
pathTmpfs       = os.path.join(pathThis, "tmpfs")
pathStatic      = os.path.join(settings.STATIC_ROOT, appName)
pathStaticWav   = os.path.join(pathStatic, "wav")

def response_text(out):
    return HttpResponse(out, content_type="text/plain")

def response_audio(out):
    response = HttpResponse(out, content_type='audio/x-wav')
    response['Content-Length']  = len(out)

    return response

def response_cache(response, timeMinutes=2):
    expires = datetime.utcnow() + timedelta(minutes=timeMinutes)
    response['Cache-Control']   = "public, max-age=" + str(3600 * timeMinutes)
    response['Expires']         = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")

    return response