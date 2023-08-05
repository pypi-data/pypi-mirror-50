import __main__
import cdsapi
import sys

c = cdsapi.Client()

with open(__main__.__file__) as f:
   code = f.read()

print(c.download(c.workflow(code)))
sys.exit(0)
