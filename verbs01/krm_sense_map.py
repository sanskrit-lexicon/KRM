#-*- coding:utf-8 -*-
"""krm_sense_map.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
#import transcoder
#transcoder.transcoder_set_dir('transcoder')

class Krmmap(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*), mw=(.*)$',line)
  self.L,self.k1,self.k2,self.code,self.mw = m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)
  
def init_krmmap(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Krmmap(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

class Krmsense(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), fullroot=([^,]*), sense=(.*)$',line)
  self.L,self.k1,self.fullroot,self.sense = m.group(1),m.group(2),m.group(3),m.group(4)
  
def init_krmsense(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Krmsense(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

def write_sensemap(fileout,srecs,mrecs):
 """ assume srecs and mrecs are parallel arrays.
     merge the attributes.
 """ 
 n = 0
 coded = {}
 with codecs.open(fileout,"w","utf-8") as f:
  for i,srec in enumerate(srecs):
   mrec = mrecs[i]
   assert srec.L == mrec.L
   assert srec.k1 == mrec.k1
   L = srec.L
   k1 = srec.k1
   #if srec.k1 != mrec.k1:
   # print('srec.k1=%s, mrec.k1=%s, L=%s' %(srec.k1,mrec.k1,L))
   #assert srec.fullroot == mrec.k1
   n = n + 1
   fullroot = srec.fullroot
   sense = srec.sense
   if ',' in sense:
    print("sense comma:",sense,"L=%s, k1=%s"%(L,k1))
   #assert ',' not in sense
   mw = mrec.mw
   code = mrec.code
   # put 'sense' last, since 3 sense terms have a comma
   out = ';; Case= %04d, L=%s, k1=%s, fullroot=%s, mw=%s, code=%s, sense=%s' % (
     n,L,k1,fullroot,mw,code,sense)
   f.write(out+'\n')
 print('%04d' %n,"verbs written to",fileout)


if __name__=="__main__": 
 filein = sys.argv[1] #  krm_sense.txt
 filein1 = sys.argv[2] # krm_verb_filter_map.txt
 fileout = sys.argv[3] #  krm_sense_map.txt
 srecs = init_krmsense(filein)  
 mrecs = init_krmmap(filein1)   
 
 write_sensemap(fileout,srecs,mrecs)
