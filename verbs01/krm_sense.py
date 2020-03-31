#-*- coding:utf-8 -*-
"""krm_sense.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
#import transcoder
#transcoder.transcoder_set_dir('transcoder')
slp_from = "aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
slp_to =   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
slp_from_to = str.maketrans(slp_from,slp_to)

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  # linenum1,2 are int
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into a dictionary
  #self.meta = Hwmeta(self.metaline)
  self.metad = parseheadline(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
  #L = self.meta.L
  L = self.metad['L']
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
  #  extra attributes
  self.marked = False # from a filter of markup associated with verbs
  self.markcode = None
  self.markline = None

def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs

def get_sense(line):
 m = re.search(u'^\([0-9A-]+\) {@<s>[“‘](.*?)[”’]</s>@}¦',line)
 if not m:
  print('parse error:',line)
  exit(1)
 x = m.group(1)
 parts = re.split(r' +',x)
 if parts == ["Buvo'vakalkane"]:
  root = 'BuvaH'  # mdp.xml 'inflectedRoot'
  fullroot = 'BU' 
  sense = 'avakalkane'
 elif len(parts) == 1:
  root = parts[0]
  fullroot = root
  sense = ''
 elif parts[0] == 'kawi[kawI]':
  root = 'kawi'
  fullroot = 'kawi/kawI' # alternates
  sense = parts[1]
 elif parts[0] == 'Kava[ca]':
  root = 'Kava' # drop the 'ca'
  fullroot = root
  sense = parts[1]
 elif parts[0] == 'lu[Yca]nca':
  root = 'lunca'
  fullroot = 'lunca/luYca' # alternates
  sense = parts[1]
 elif parts[0] == 'svada[rda]':
  root = 'svada'
  fullroot = 'svada/svarda' # alternates
  sense = parts[1]
 elif parts[0] == '':
  root = ''
  fullroot = '' # alternates
  sense = parts[1]

 elif len(parts) == 2:
  # assume root, sense
  root = parts[0]
  fullroot = root
  sense = parts[1]
  #return x,parts[0],parts[1]
 elif parts[0] in ['[ano]','[ANaH]','[qu]','[]','[]','[]']:
  temp = parts[0]
  premarker = temp[1:-1] # strip the brackets
  root = parts[1]
  fullroot = ' '.join([premarker,root])
  sense = ' '.join(parts[2:])
 elif (parts[0],parts[1]) in [('[wu','o]'),('wu','o')]:
  premarker = 'wuo'
  root = parts[2]
  fullroot = ' '.join([premarker,root])
  sense = ' '.join(parts[3:])
 elif (parts[0],parts[1]) == ('I','(vI)'):
  #premarker = ''
  root = 'I'  # krm also has 'vI'
  fullroot = root
  sense = ' '.join(parts[2:])

 elif parts[0] in ['Yi','qu','o','I','wu','u']:
  premarker = parts[0]
  root = parts[1]
  fullroot = ' '.join([premarker,root])
  sense = ' '.join(parts[2:])
 else:
  m = re.search(r'^([^ ]+)(.*)$',x)
  root = m.group(1)
  fullroot = root
  sense = m.group(2)
  #return x,k1,sense
 sense = sense.strip()
 return x,root,sense,fullroot

def write_sense(fileout,entries):
 n = 0
 coded = {}
 with codecs.open(fileout,"w","utf-8") as f:
  for ientry,entry in enumerate(entries):
   n = n + 1
   outarr = []
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   x,k1chk,sense,fullroot = get_sense(entry.datalines[0])
   if k1 != k1chk:
    #print('key problem:L=%s, k1=%s, k1chk=%s'%(L,k1,k1chk))
    print('key problem:L=%s, k1=%s, x=%s'%(L,k1,x))
   out = ';; Case= %04d, L=%s, k1=%s, fullroot=%s, sense="%s"' % (
     n,L,k1,fullroot,sense)
   f.write(out+'\n')
 print('%04d' %n,"verbs written to",fileout)

def check1(entries):
 d = {}  # records with given 'k1'
 for ientry,entry in enumerate(entries):
  k1 = entry.metad['k1']  
  if k1 not in d:
   d[k1] = []
  d[k1].append(entry)
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
 for c in [4,5]:
  klist = [k for k in keys if len(d[k]) == c]
  kstr = ', '.join(klist)
  print('values of k1 with %s entries=%s' %(c,kstr))

def check_alpha(entries):
 for ientry,entry in enumerate(entries):
  k1 = entry.metad['k1']  
  if ientry == 0:
   k1prev = k1
   continue
  if k1prev == k1:
   continue
  if k1prev.translate(slp_from_to) < k1.translate(slp_from_to):
   k1prev = k1
   continue
  # out of order
  L = entry.metad['L']
  pc = entry.metad['pc']
  print('order error: %s, [%s], %s >%s'%(L,pc,k1prev,k1))
  k1prev = k1

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[2] # 
 entries = init_entries(filein)
 write_sense(fileout,entries)
 check1(entries)  # duplicates
 check_alpha(entries)
