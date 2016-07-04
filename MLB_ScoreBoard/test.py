#Get XML Libraries
from xml.dom import minidom
import urllib

#Get Date Libraries
import time

#Get MLB XML
url_str = 'http://gd2.mlb.com/components/game/mlb/year_2016/month_06/day_25/scoreboard.xml'
xml_str = urllib.urlopen(url_str).read()
xmldoc = minidom.parseString(xml_str)

print xml_str
#END OF GET MLB XML

#Get Current Date Function
print (time.strftime("%m/%d/%Y"))
#End OF GET DATE






