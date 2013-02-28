# please mount tmpfs to tmpfs folder there
# it's spike for fast creation .csd files in Csound
# in linux: sudo mount tmpfs path_to_folder/tmpfs -t tmpfs -o size=8m
import shlex, os
from django.conf import settings

appName         = "slovastick_app"
pathThis        = os.path.abspath(os.path.dirname(__file__))
pathTmpfs       = os.path.join(pathThis, "tmpfs")
pathStatic      = os.path.join(settings.STATIC_ROOT, appName)
pathStaticWav   = os.path.join(pathStatic, "wav")