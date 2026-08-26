import importlib.util
import os
import sys

# Add project directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Path to your wsgi.py
wsgi_path = os.path.join(os.path.dirname(__file__), "core", "wsgi.py")

spec = importlib.util.spec_from_file_location("wsgi", wsgi_path)
wsgi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wsgi)
application = wsgi.application