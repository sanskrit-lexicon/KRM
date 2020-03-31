#-*- coding:utf-8 -*-
"""mdp_parse.py  parse mdp.xml
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
#import transcoder
#transcoder.transcoder_set_dir('transcoder')

class Mdp(object):
 
 def __init__(self,line):
  line = line.rstrip('\r\n')
  m = re.search(r'<entry sid="(.*?)"',line)
  self.sid = m.group(1)
  #
  m = re.search(r'<inflectedRoot[^>]*>(.*?)</inflectedRoot>',line)
  if m:
   self.inflectedroot = m.group(1)
  else:
   self.inflectedroot = None
  #
  m = re.search(r'<fullDAtu[^>]*>(.*?)</fullDAtu>',line)
  if not m:
   print('no fullDAtu',line)
   self.fullroot = None
   return
  self.fullroot = m.group(1)
  #
  m = re.search(r'<root normal="(.*?)">(.*?)</root>',line)
  if m:
   self.normalroot = m.group(1)
   self.root = m.group(2)
  else:
   m = re.search(r'<root[^>]*>(.*?)</root>',line)
   if not m:
    print('root parse error',line)
    exit(1)
   self.normalroot = None
   self.root = m.group(1)
  #
  m = re.search(r'<senseterm[^>]*>(.*?)</senseterm>',line)
  if not m:
   #print('senseterm parse error',line)
   #exit(1)
   self.senseterm = ""
  else:
   self.senseterm = m.group(1)

  
def init_mdp(filein):
 recs = []
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  nofr = 0 # number with no fullroot
  for line in f:
   if not line.startswith('<entry'):
    continue
   rec = Mdp(line)
   if rec.fullroot == None:
    nofr = nofr + 1
   else:
    recs.append(rec)

 print(len(recs),"mdp entries found in",filein)
 print(nofr,"records skipped as having no fullDAtu element")
 return recs

def get_roots(rootlist):
 first = rootlist[0]
 a = [r for r in rootlist if (r != None) and (r != first)]
 return '/'.join(a)

def root_reformat(fullroot):
 parts = fullroot.split(' ')
 if len(parts) == 1:
  return fullroot
 if len(parts) == 3:  # (wu o) xx
  parts[0] = parts[0] + parts[1]  # (wuo)
  parts[1] = parts[2] # xx
 m = re.search(r'^\((.*?)\)$',parts[0])
 if not m:
  print("root_reformat error",fullroot)
  return fullroot
 a = m.group(1) # drop parens
 b = parts[1]
 return '%s %s'%(a,b)

def write(fileout,recs):
 n = 0

 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs):
   n = n + 1
   outarr = []
   sid = rec.sid
   sense = rec.senseterm
   fullroot = root_reformat(rec.fullroot)
   
   rootstr = get_roots([fullroot,rec.inflectedroot,rec.normalroot,rec.root])
   #rootstr = get_roots([rec.inflectedroot,rec.normalroot,rec.root])
   #out = ';; Case= %04d, sid=%s, fullroot=%s, sense="%s", othrroots=%s' % (
   #  n,sid,fullroot,sense,rootstr)
   # rootstr not useful for this study.
   out = ';; Case= %04d, sid=%s, fullroot=%s, sense="%s"' % (
     n,sid,fullroot,sense)
   f.write(out+'\n')
 print('%04d' %n,"mdp records written to",fileout)

def check1(recs):
 d = {}
 for rec in recs:
  f0 = rec.fullroot
  parts = f0.split(' ') 
  k1 = parts[-1]  # ignore 57 cases with premarker
  if k1 not in d:
   d[k1] = []
  d[k1].append(rec)
 keys = d.keys()
 print(len(keys),"unique values of k1")
 cd = {}
 for k in keys:
  c = len(d[k])
  if c not in cd:
   cd[c] = 0
  cd[c] = cd[c] + 1

 ckeys = sorted(cd.keys())
 for c in ckeys:
  count = cd[c] 
  print('%04d values of k1 with %d records' %(count,c))
 for c in [5,6]:
  klist = [k for k in keys if len(d[k]) == c]
  kstr = ', '.join(klist)
  print('values of k1 with %s entries=%s' %(c,kstr))

if __name__=="__main__": 
 filein = sys.argv[1] #  mdp.xml
 fileout = sys.argv[2] # mdp_parse.txt
 recs = init_mdp(filein)
 write(fileout,recs)
 check1(recs)
