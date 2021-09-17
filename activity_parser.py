#!/usr/bin/python3

import xml.etree.ElementTree as ET 
import os
import csv
import io
from tkinter import filedialog
from tkinter import *


def find_all(name, path):
  result = []
  print(name+' '+path) 
  for root, dirs, files in os.walk(path):
    if name in files:
      result.append(os.path.join(root, name))
  #result = [ x for x in result if "test" not in x and "Test" not in x and "frameworks" not in x ]
  print('Found '+str(len(result))+' files.')
  return result

root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()

manifests=[]
manifests=find_all('AndroidManifest.xml',folder_selected)

with open('gm_activities.csv', 'w') as csvfile:
  activitylist = csv.writer(csvfile, dialect='excel', delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
  activitylist.writerow(["Package Name", "Activity Name","Distraction Optimized"])

scan_failures=0
total_activity=0
for filename in manifests: 
  try:   
    tree = ET.parse(filename) 
  except:
    print("ill formed XML in ", filename)
    scan_failures+=1
    pass
  root = tree.getroot()
  pname = root.attrib.get('package')   
  #print(pname)  
  for activity in root.findall(".//activity"):
    total_activity+=1 
    new_row = []
    new_row.append(pname)      
    #print(activity.get('{http://schemas.android.com/apk/res/android}name')) 
    do = False
    for child in activity.findall("./meta-data"):
      do = True
      #print(child.attrib.get('{http://schemas.android.com/apk/res/android}value'))
    #if not do:
      #print("false")
    new_row.append(activity.get('{http://schemas.android.com/apk/res/android}name'))
    new_row.append(do)
    with open('gm_activities.csv', 'a', newline='') as csvfile:
      filewriter=csv.writer(csvfile, dialect='excel', delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
      filewriter.writerow(new_row)

print("Total manifest files found and scanned:  ", str(len(manifests)))
print("Number of manifest files that were not able to be scanned:  ",str(scan_failures))
print("Total number of activities found across all manifest files:  ", str(total_activity))

