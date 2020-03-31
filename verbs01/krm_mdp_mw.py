#-*- coding:utf-8 -*-
"""krm_mdp_mw.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
import transcoder
from transcoder import transcoder_processString
transcoder.transcoder_set_dir('transcoder')
# transcoder_processString(x,tranin,tranout)
slp_from = "aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh?"
slp_to =   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx"
slp_from_to = str.maketrans(slp_from,slp_to)

class Krm(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')  
  m = re.search('L=(.*?), k1=(.*?), fullroot=(.*?), mw=(.*?), code=(.*?), sense=(.*?)$',line)
  self.L = m.group(1)
  self.k1 = m.group(2)
  self.fullroot = m.group(3)
  self.mw = m.group(4)
  self.code = m.group(5)
  self.sense = m.group(6)

 def __repr__(self):
  ans = 'fullroot=%s, sense=%s, L=%s' %(
         self.fullroot,self.sense,self.L)
  return ans

 def transcode(self,tranin,tranout):
  fullroot = transcoder_processString(self.fullroot,tranin,tranout)
  sense = self.sense
  if tranout == 'deva':
   sense = sense.replace('"','')
  sense = transcoder_processString(sense,tranin,tranout)
  L = self.L
  code = self.code
  ans = 'fullroot=%s, sense=%s, L=%s, mwcode=%s' %(
         fullroot,sense,L,code)
  return ans

def init_krm(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = [Krm(line) for line in f]
 print(len(recs),"krm records read from",filein)
 return recs

class Mdp(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')  
  #m = re.search('sid=(.*?), fullroot=(.*?), sense=(.*?), othrroots=(.*), mw=(.*), code=(.*)$',line)
  m = re.search('sid=(.*?), fullroot=(.*?), sense=(.*?), mw=(.*), code=(.*)$',line)
  self.sid = m.group(1)
  self.fullroot = m.group(2)
  self.sense = m.group(3)
  #self.othrrootstr = m.group(4)
  #self.othrroots = self.othrrootstr.split('/')
  self.mw = m.group(4)
  self.code = m.group(5)
 def __repr__(self):
  #ans = 'fullroot=%s, sense=%s, sid=%s, othrroots=%s' %(
  #  self.fullroot,self.sense,self.sid,self.othrrootstr)
  ans = 'fullroot=%s, sense=%s, sid=%s' %(
    self.fullroot,self.sense,self.sid)
  return ans

 def transcode(self,tranin,tranout):
  fullroot = transcoder_processString(self.fullroot,tranin,tranout)
  sense = self.sense
  if tranout == 'deva':
   sense = sense.replace('"','')
  sense = transcoder_processString(sense,tranin,tranout)
  #othrrootstr = transcoder_processString(self.othrrootstr,tranin,tranout)
  sid = self.sid
  code = self.code
  #ans = 'fullroot=%s, sense=%s, sid=%s, othrroots=%s, mwcode=%s' %(
  #  fullroot,sense,sid,othrrootstr,code)
  ans = 'fullroot=%s, sense=%s, sid=%s, mwcode=%s' %(
    fullroot,sense,sid,code)
  return ans

def init_mdp(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = [Mdp(line) for line in f]
 print(len(recs),"mdp records read from",filein)
 return recs

class Keyobj(object):
 def __init__(self,key,x):
  self.k = key
  self.x = x

def rec_to_keyobj(recs):
 d = {}  # records with given 'mw'
 for rec in recs:
  mw = rec.mw
  if mw not in d:
   d[mw] = []
  d[mw].append(rec)
 keys = sorted(d.keys(),key = lambda x: x.translate(slp_from_to))
 keyobjs = [Keyobj(key,d[key]) for key in keys]
 return keyobjs

def merge(recs1,recs2):
 # recs1 and recs2 are lists of objects which have
 # a 'k' attribute.  The value of this k attribute is
 # a string assumed to be an SLP1 transliteration of a Sanskrit word or phrase
 # It is assumed that each of recs1, recs2 is sorted in Sanskrit alphabetical
 # order by the value of the 'k' attribute.
 # The routine returns a list of pairs. 
 # Each pair has one of three forms:
 # (r1,r2)  where r1.k == r2.k
 # (r1,None)
 # (None,r2)
 # and the pairs are in Sanskrit alphabetical order.
 ans = []
 n1 = len(recs1)
 n2 = len(recs2)
 i1 = 0
 i2 = 0
 while (i1<n1) and (i2<n2):
  r1 = recs1[i1]
  r2 = recs2[i2]
  if r1.k == r2.k:
   ans.append([r1,r2])
   i1 = i1+1
   i2 = i2+1
   continue
  """
  if merge_approx_match(r1,r2):
   ans.append([r1,r2])
   i1 = i1+1
   i2 = i2+1
   continue
  """
  # no match or approximate match found. Proceed by alphabetical order
  if r1.k.translate(slp_from_to) < r2.k.translate(slp_from_to):
   ans.append([r1,None])
   i1 = i1 + 1
  else:
   ans.append([None,r2])
   i2 = i2 + 1
 return ans
 
def write(option,fileout,mergerecs,tranout,name1,name2):
 tranin = 'slp1'
 n = 0
 nflag = 0
 neq = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for imerge,mergerec in enumerate(mergerecs):
   rec1,rec2 = mergerec
   outarr1 = []
   outarr2 = []
   flagok = True
   if (rec1 == None) or (rec2 == None):
    flagok = False
   if (rec1 != None) and (rec1.k == '?'):
    flagok = False
   if (rec2 != None) and (rec2.k == '?'):
    flagok = False
   if (option == 1) and (not flagok):
    # skip this problem merged record
    continue
   if (option == 2) and flagok:
    # skip this non-problem merged record
    continue
   n = n + 1
   if rec1 == None:
    out1 = '?'
    outarr1.append('%s: %s' %(name1,out1))
   else:
    out1 = rec1.k
    k = rec1.k
    for r in rec1.x:
     rstr = r.transcode(tranin,tranout)
     outarr1.append('%s: %s' %(name1,rstr))
     assert k == r.mw
   if rec2 == None:
    out2 = '?'
    outarr2.append('%s: %s' %(name2,out2))
   else:
    out2 = rec2.k
    k = rec2.k
    for r in rec2.x:
     rstr = r.transcode(tranin,tranout)
     outarr1.append('%s: %s' %(name2,rstr))
     assert k == r.mw
   outarr = []
   kstr = transcoder_processString(k,tranin,tranout)
   outarr.append('; Case %04d: mw = %s' %(n,kstr))
   outarr = outarr + outarr1 + [';'] + outarr2 + [';']
   for out in outarr:
    f.write(out + '\n')
 print(n,"records written to",fileout)
 #print(nflag,"matches are approximate")

if __name__=="__main__": 
 tranout = sys.argv[1] #  slp1 or deva
 filein1 = sys.argv[2] #  krm_sense_map
 filein2 = sys.argv[3] #  mdp_parse_map
 fileout = sys.argv[4] #  krm_mdp_mw
 fileout1 = sys.argv[5] #  krm_mdp_nomw
 krm_recs= init_krm(filein1)
 mdp_recs = init_mdp(filein2)

 krm_keyobjs = rec_to_keyobj(krm_recs)
 mdp_keyobjs = rec_to_keyobj(mdp_recs)
 mergerecs =  merge(krm_keyobjs,mdp_keyobjs)
 write(1,fileout,mergerecs,tranout,'krm','mdp')
 write(2,fileout1,mergerecs,tranout,'krm','mdp')

 #write_sense(fileout,entries)
 #check1(entries)  # duplicates
