import numpy
# from cvxopt import matrix
import cvxopt
from datetime import datetime
import time
import urllib

a = datetime.strptime('06:15PM 02/08/2018', '%I:%M%p %m/%d/%Y')
b = a.timestamp()

print ("HI")

urla = 'https://api.darksky.net/forecast/0f28afb4d439038454689fb53cedff26/31.49,-97.29,1518135300?exclude=currently,minutely,hourly,daily,alerts,flags'

with urllib.request.urlopen(urla):
    pass