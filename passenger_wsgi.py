# passenger_wsgi.py
# Das Ändern:
import os
import sys
from app import MyApp as application
CONDA_ENV = "slack-bot"
PYTHON_VERSION = "python3.9"
MINICONDA_ROOT = "/miniconda3"
"""
Diese Start Datei wird in dem von Netcup bestimmten Python Interpreter geladen.
mit os.execl("python","python","this_file") wird die Datei im definierten Python Interpreter neu geladen.
Alle Packages die der Python Interpreter zur Verfügung hat können importiert werden.
Code leicht geändert von: https://help.dreamhost.com/hc/en-us/articles/215769548-Passenger-and-Python-WSGI
"""
INTERP = os.environ["HOME"]+MINICONDA_ROOT + \
    "/envs/"+CONDA_ENV+"/bin/"+PYTHON_VERSION
# INTERP = os.environ["HOME"]+"/miniconda3/envs/testenv/bin/python3.9"
"""
os.environ["HOME"] ist wie ~/
wenn Passenger diese Datei als dein Webhosting User öffnet
befindet sich das Nutzer Verzeichnis nicht mehr unter:
"/" sonder "/var/www/vhosts/hosting*user*.*server*.netcup.net/"
"/miniconda3/envs/testenv/bin/python3.9" muss der Path zu den Python Binaries sein
python -m venv testenv // funzt nicht, denn dabei wird nur ein Link zur Haupt Python Anwendung erstellt.
lieber: conda create --name testenv // hierbei werden augenscheinlich die Python Binaries direkt in der Venv abgelegt.
"""
"""
Debugging:
Im 1. Durchlauf sollte der original Interpreter geprinted werden.
Im 2. Druchlauf dein INTERP
"""
# print(sys.path)
# print(sys.executable)
# INTERP is present twice so that the new Python interpreter knows the actual executable path
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
# Dieser Code wird erst beim finalen Interpreter ausgeführt:
# Das Ändern:
