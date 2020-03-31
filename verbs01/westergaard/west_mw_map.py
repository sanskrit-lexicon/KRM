#-*- coding:utf-8 -*-
"""krm_verb_filter.py
 
"""
from __future__ import print_function
import sys, re,codecs

class Sutra(object):
 def __init__(self,line):
  m = re.search(r'^<sutra msid="([^"]*)">(<root .*</root>)<sense([^>]*)>([^<]+)</sense></sutra>',line)
  if m == None:
   print('Sutra error 1: ',line)
   self.status = 1
   return
  self.msid = m.group(1)
  root0 = m.group(2)
  senseattr = m.group(3)
  self.sense = m.group(4).strip()
  if self.sense == '{20. kita {wdp}) jYAne':
   self.sense = 'jYAne'
   print('Sutra: change sense for',line)
  if self.sense == 'madane ca {wdp duplicate number}':
   self.sense = 'madane ca'
   print('Sutra: change sense for',line)   
  if senseattr == '':
   self.mdpsense = self.sense.strip()
  else:
   m = re.search(r'^ mdp="([^"]+)"$',senseattr)
   if not m:
    print('Sutra error 2. senseattr=',senseattr)
    print(' line=',line)
    self.status = 2
    return
   self.mdpsense = m.group(1)
  rootelts = re.findall(r'<root[^>]*>[^<]*</root>',root0)
  self.westroots = []
  for rootelt in rootelts:
   m = re.search(r'^<root wsid="([^"]+)"([^>]*)>([^<]+)</root>$',rootelt)
   if not m:
    print('Sutra error 3:',line)
    self.status = 2
    return
   wsid = m.group(1)
   root = m.group(3)
   if root == 'drAGf {wdp number repeated}':
    root = 'drAGf'
    print('Sutra. edit root',line)
   # in 27 cases, there is a ':' character in 'root' value. 
   # Change this to '_'
   root = root.replace(':','_')
   rootattr = m.group(2)
   if rootattr == '': # usual case
    mdproot = root
   else:
    m = re.search(r'^ *mdp="([^"]+)" *$',rootattr)
    if m:
     mdproot = m.group(1)
    else:
     mdproot = root
   mdproot = mdproot.replace(':','_')
   westroot = (wsid,root,mdproot) 
   
   self.westroots.append(westroot)  
  self.status = 0

def init_wdp_mw_xml(filein):
 """  This is an xml file, but we parse it as a text file
 """
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 nsutra = 0
 for line in lines:
  if re.search(r'^<sutra .*</sutra>$',line):
   if '.X' in line: ## irregular sutras. Not sure of parsing. 16 cases
    rec = line
   elif '-->' in line:  # 1 case
    rec = line
   else:
    rec = Sutra(line)
    if rec.status != 0:
     rec = line
    else:
     nsutra = nsutra + 1
  else:
   rec = line
  recs.append(rec)
 print(nsutra,"records parsed as sutra")
 return recs

class Westmw(object):
 def __init__(self,line):
  m = re.search(r'^<key1>([^<]*)</key1><ls>([^<]*)<wsid>([^<]*)</wsid></ls><L>([^<]*)</L>$',line)
  self.key1 = m.group(1)
  self.ls = m.group(2)
  self.wsid = m.group(3)
  self.L = m.group(4)

def init_mw_wdp_txt(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 for line in lines:
  try:
   rec = Westmw(line)
  except:
   print('init_mw_wdp_txt parse error',line)
   continue
  recs.append(rec)
 return recs

def init_sutras_dict(sutras):
 d = {}
 for rec in sutras:
  for wsid,wdproot,mdproot in rec.westroots:
   if wsid not in d:
    d[wsid] = []
   d[wsid].append((wdproot,mdproot,rec.sense))
 keys = d.keys()
 dups = [k for k in keys if len(d[k]) > 1]
 print(len(keys),"distinct wsid in sutra objects")
 print(len(dups),"of these correspond to multiple sutra records")
 print(dups)
 return d

def init_westmw_dict(recs):
 d = {}
 for rec in recs:
  wsid = rec.wsid
  # there are many duplicate wsids
  if wsid not in d:
   d[wsid] = []
  d[wsid].append(rec)

 keys = d.keys()
 dups = [k for k in keys if len(d[k]) > 1]
 print(len(keys),"distinct wsid in westmw objects")
 print(len(dups),"of these correspond to multiple mw records")
 return d

def write_sutras(fileout,sutras,westmw_dict):
 with codecs.open(fileout,"w","utf-8") as f:
  outarr = []
  for rec in sutras:
   msid = rec.msid
   wdpsense = rec.sense
   mdpsense = rec.mdpsense
   if wdpsense != mdpsense:
    sense = '%s/%s'%(wdpsense,mdpsense)
   else:
    sense = wdpsense
   #print('wcheck:',msid,len(rec.westroots))
   for wsid,wdproot,mdproot in rec.westroots:
    if mdproot == wdproot:
     root = wdproot
    else:
     root = '%s/%s'%(wdproot,mdproot)
    if wsid in westmw_dict:
     westmwrecs = westmw_dict[wsid]
     mwinfos = ["%s,%s" %(r.key1,r.L) for r in westmwrecs]
     mwinfo = ';'.join(mwinfos)
    else:
     mwinfo = '?'
    outarr.append((wsid,root,sense,msid,mwinfo))
  for a in outarr:
   out = ':'.join(a)
   f.write(out + '\n')
 print(len(outarr),"records written to",fileout)

if __name__=="__main__": 
 filein1 = sys.argv[1] #  wdp-mw.xml
 filein2 = sys.argv[2] #  mw-wdp.txt
 fileout = sys.argv[3] # 

 recs1 = init_wdp_mw_xml(filein1)
 sutras = [r for r in recs1 if type(r) == Sutra]
 print(len(sutras),"Sutra objects parsed from",filein1)
 recs2 = init_mw_wdp_txt(filein2)
 print(len(recs2),"Westmw objects parsed from",filein2)
 sutras_dict = init_sutras_dict(sutras)
 westmw_dict = init_westmw_dict(recs2)
 write_sutras(fileout,sutras,westmw_dict)
