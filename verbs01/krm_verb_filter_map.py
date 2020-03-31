#-*- coding:utf-8 -*-
"""krm_verb_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs

class Verb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*)$',line)
  self.L,self.k1,self.k2,self.code = m.group(1),m.group(2),m.group(3),m.group(4)
  self.mw = None
  self.mwcode = None  # match code.  How the match determined
  self.krmvariant = None  # see krm_mw_variants
def init_verb(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Verb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

class MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False

def init_mwverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [MWVerb(x) for x in f]
 print(len(recs),"mwverbs read from",filein)
 #recs = [r for r in recs if r.cat == 'verb']
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 #recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"verbs returned from mwverbs")
 d = {}
 for rec in recs:
  k1 = rec.k1
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d


def init_dp_mw_map(recs,mwd):
 """ recs is list of Westmw objects"""
 d = {}
 for rec in recs:
  mwroots = [x[0] for x in rec.mwinfopairs]
  for wroot in rec.wroots:
   if wroot not in d:
    a = []
   else:
    a = d[wroot]
   for mwroot in mwroots:
    if mwroot == '?':
     continue
    if mwroot not in mwd:  # be sure it IS a root!
     continue
    if mwroot not in a:
     a.append(mwroot)
   if a != []:
    d[wroot] = a
 return d

krm2mw_special = {
 #krm:mw
 # mw = krm + ya
 'kuwumba':'kuwumbaya',
 'kumAra':'kumAraya',
 'kusma':'kusmaya',
 'keta':'ketaya',
 'kAla':'kAlaya',
 'Una':'Unaya',
 'guRa':'guRaya',
 #'gfha':'gfhaya',
 'gfha':'grah',  # causal. also gfhaya
 'goma':'gomaya',
 'grAma':'grAmaya',
 'citra':'citraya',
 'Cidra':'Cidraya',
 'tIra':'tIraya',
 'tutTa':'tutTaya',
 'daRqa':'daRqaya',
 'palpUla':'palpUlaya',
 'pAra':'pAraya',
 'mUtra':'mUtraya',

 # other patterns
 'tatri':'tantraya',
 'daridrA':'drA',  # mw desiderative
 'zanja':'saYj',
 'zasja':'sajj',
 'zUN':'sU',  # sU is also in krm
 'zfnBu':'sfmB',
 'zfBu':'sfB',
 'zmiN':'smi',
 'saNketa':'saMketaya',
 'saNgrAma':'saMgrAm',
 'sAra':'sAraya',
 'skanBuH':'skamB',  # krm also has skaBi. mw also has skaB
 'hAk':'hA',
 #'hAN':'hA',
 #'hnuN':'hnu',
 'olaqi':'olaRq',
 'ftiH':'ft',

 'kex':'kel', # a guess
 'Kex':'Kel',
 'Kox':'Kol',
 'pex':'pel',
 'Pex':'Pel',
 'Sex':'Sel',

 'kzamUz':'kzam',
 'kzIz':'kzI',
 'gfji':'gfj',
 'Gaza':'GaMz', #?
 'Guzi':'Guz',  #?
 'cakziN':'cakz',
 'cukkaM':'cukk',
 'Carda':'Cfd', #causal
 'trapUz':'trap',
 'nivAsa':'nivas',  # causal of ni+vas
 'pacaz':'pac',
 'ravi':'raRv',
 'rivi':'riRv',
 'laBaz':'laB',
 'Sarda':'SfD', # causal
 'sAtiH':'sAt',
 'qukrIY':'krI',
 'kfvi':'kfv',
 'kzaji':'kzaj',
 'gadi':'gad',
 'guvIM':'gurv',
 'gfhU':'grah',
 'Ceda':'Cid',
 'garDa':'gfD',
 'jFz':'jF',
 'tuji':'tuj',
 'tUrI':'tur', #? tvar?
 'JFz':'JF',
 'tfnhU':'tfh',
 'jYapa':'jYA',  # causal ?
 'dAR':'dA',
 'dApU':'dA',
 'dEp':'dE',
 'Dew':'De',
 'puzpa':'puzpya',
 'pUrI':'pF',
 'basta':'vast',  # krm basta/vasta similar
 'BAja':'Baj',  # causal
 'mrewwa':'mrew',
 'lola':'lul',
 'vara':'vf', # causal
 'varza':'vfz', # causal
 'vITf':'veT',  #?
 'zaRa':'san',
 'zaRu':'san',
 'zwage':'sTag',
 'zwupa':'stUp',
 # from comparisons of krm and mdp (mADavIyaDAtuvftti)
 'ik':'i',
 'iR':'i',
 'BuvaH':'BU',

 'kawi':'kaw',  # mw kaRw cf kaw.  
 'kUN':'ku',   # mw kU or ku
 'knaTa':'kraT', # mw knaT cf kraT, klaT
 'guWi':'guRq',  #mw guRW df guRq, guD
 'graTa':'granT', # mw graT or granT
 'cyusa':'cyu',  #mw cyus. See cyu
 # mw traNk, traNK, traNg.
 # mw triNK vl for traNK
 'triKi':'traNk',
 'daBa':'damB', # mw daB or damB
 'DUSa':'DUs',  # mw DUS or DUz or DUs
 'DUza':'DUs',  # mw DUS or DUz or DUs
 'naqi':'naw',  # mw naq cf naw
 'pfji':'pfYj', # mw pfj, pfYj.   vl for pfc. vl for pij
 'bugi':'vuNg', # mw buNg or vuNg
 'Bruqa':'vruq', # same by sense, similar by spelling
 'raSa':'rAs', # mw rAS vl for rAs.  rAs senses similar to sens of krm raSa
 'riKa':'riNK', #mw riK cf riNK
 'vahi':'baMh',  # mw vaMh See baMh
 'zage':'sTag',  # mw zag, zaG, zac see sag.  mw sag cf sTag
 'zaGa':'sTag',  # mw zag, zaG, zac see sag.  mw sag cf sTag
 'zawwa':'saww', # mw zaww cf saww
 'zaca':'sac',  # identity of sense
 'zivi':'ninv',  #mw sinv . See ninv
 'sniwa':'snih', # mw sniw cf snih
 'zRE':'stE',    # mw snE vl stE
 'sPala':'sPul',  # mw sPal vl for sPul
 'svarta':'Svart', # mw svart vl for Svart
 'rusi':'ruMS',   # sense agrees.
 'UWa':'uW',      # mw uW or UW
 'Ku':'ku',       # by sense
 '':'',
 '':'',

}
def map2mw(d,k1):

 if k1 in d:
  return k1,'MW1'
 
 if k1.endswith('a'):
  k = k1[0:-1] # remove final 'a'
  if k in d:
   return k,'MWa'
 return '?','?'
 if False:
  k2 = k.replace('cC','C')
  if k2 in d:
   return k2
  k2 = re.sub(r'r(.)\1',r'r\1',k)
  if k2 in d:
   return k2
  k2 = re.sub(r'^R','n',k)
  if k2 in d:
   return k2
  k2 = re.sub(r'^z','s',k)
  if k2 in d:
   return k2
  k2 = k1 + 'ya'
  if k2 in d:
   return k2

 else:
  k = k1
  k2 = k.replace('cC','C')
  if k2 in d:
   return k2
  k2 = re.sub(r'r(.)\1',r'r\1',k)
  if k2 in d:
   return k2
  k2 = re.sub(r'^R','n',k)
  if k2 in d:
   return k2
  k2 = re.sub(r'^z','s',k)
  if k2 in d:
   return k2

 return ans

drop_endings = ['a','f','I','e','x','u','U','Y','A','ir','o','N']

def dpadjust_a(k,v='a'):
 if not k.endswith(v):
  return None
 n = len(v)
 ans = k[0:-n]
 #if True:
 # if v == 'ir':print('check: %s -> %s'%(k,ans))
 return ans
def homorganic_nasal(c):
 vargas = ['kKgGN','cCjJY','wWqQR','tTdDn','pPbBm','yrlvn','SzshM']
 for varga in vargas:
  if c in varga:
   return varga[-1]  # nasal
 return None

def dpadjust_i(k):
 if not k.endswith('i'):
  return None
 if k == 'i':
  return None
 k1 = k[0:-1] # drop final 'i'
 # insert homorganic nasal after first vowel
 m = re.search(r'^(.*?)([aAiIuUfFxXeEoO])(.)(.*)$',k1)
 if m == None:
  # k = ri.
  print('dpadjust_i fails:',k)
  return None
 a = m.group(1) # letters (if any) before vowel
 v = m.group(2) # vowel
 c = m.group(3) # letter after vowel. Assumed a consonant
 b = m.group(4) # letters (if any) after consonant
 n = homorganic_nasal(c)
 ans = a + v + n + c + b
 #print('dpadjust: %s -> %s' %(k,ans))
 return ans

def krmmap_helper2(k1,mwd):
 #rec.mw,rec.mwcode = map2mw(mwd,k1)
 if k1 in mwd:  # 
  return k1,'3'
 for v in drop_endings:
  k1a = dpadjust_a(k1,v)
  if k1a in mwd:
   return k1a,'3' + v
 # try nasal insertion
 k1a = dpadjust_i(k1)
 if k1a in mwd:
  return k1a,'3nasal'
 # no joy
 if k1.endswith('IN'):
  k1a = k1[0:-1]
  if k1a in mwd:
   return k1a,'3IN'

 return '?','?'

variant_subs = [
  (r'^R',r'n'),
  (r'^z',r's'),
  (r'^zw',r'st'),
  (r'^zW',r'sT'),
  (r'^zR',r'sn'),
  (r'nc',r'Yc'),
  (r'nj',r'Yj'),
  (r'nS',r'MS'),
  (r'ns',r'Ms'),
  (r'nB',r'mB'),
  (r'nP',r'mP'),
  (r'np',r'mp'),
  (r'cC',r'C'),
  (r'sj','jj'),
 ]

def krm_mw_variants(k):
 ans = [(k,-1)] # -1 means no change
 for isub,sub in enumerate(variant_subs):
  r1,r2 = sub
  x = re.sub(r1,r2,k)
  if x not in ans:
   ans.append((x,isub))
 return ans

def krmmap_rec(rec,mwd):
 if rec.k1 in krm2mw_special:
  mw = krm2mw_special[rec.k1]
  if mw in mwd:  # this test for safety. Should always hold
   rec.mw = krm2mw_special[rec.k1]
   rec.mwcode = 'S'
   rec.krmvariant = -2  # an 'unknown' change
   return
 variants = krm_mw_variants(rec.k1)
 for variant in variants:  
  k1,krmvariant = variant
  
  rec.mw,rec.mwcode = krmmap_helper2(k1,mwd)
  if not rec.mwcode.startswith('?'):
   rec.krmvariant = krmvariant
   return
 rec.mwcode='?'
 rec.mw='?'

def krmmap(recs,mwd):
 for rec in recs:
  krmmap_rec(rec,mwd)

def write(fileout,recs):
 n = 0
 nomw = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   n = n + 1
   line = rec.line
   # combine mwcode and krmvariant
   var = rec.krmvariant
   if var == None:
    var = '?'
   elif var == -1:
    var = 'NC'  # no change
   elif var == -2:
    var = 'S'   # special
   else:
    var = '%02d'%var
   code = '%s-%s' %(rec.mwcode,var)
   line = line.replace('code=1','code='+code)
   out = '%s, mw=%s' %(line,rec.mw)
   f.write(out + '\n')
   if rec.mw =='?':
    nomw = nomw + 1
 print(n,"records written to",fileout)
 print(nomw,"verb have no mw match")

 
def unused_test(fileout,recs,mwverbsd,filecode,filevar):
 # make copy of recs
 newrecs = [Verb(rec.line) for rec in recs]
 # set dpmwdict to empty, so it won't be used to map krm to mw
 newdpmwdict = {}
 krmmap(newrecs,mwverbsd,newdpmwdict)
 write(fileout,newrecs)
 write_codes(filecode,newrecs)
 write_variants(filevar,newrecs)

def get_varcodename(var):
 if var == -2:
  return 'S','Special'
 elif var == -1:
  return 'NC','no extra change'
 else:
  sub = variant_subs[var]
  old,new = sub
  varname = '%s -> %s' %(old,new)
  varcode = '%02d' %var
  return varcode,varname


def write_variants(fileout,recs):
 d = {}
 for rec in recs:
  var = rec.krmvariant
  if var == None:
   var = -2
  if var not in d:
   d[var] = 0
  d[var] = d[var] + 1
 varcodes = sorted(d.keys())  # -2, -1, 0 to len(variant_subs)-1
 # write markdown format table
 with codecs.open(fileout,"w","utf-8") as f:
  f.write('code|description|count|\n')
  f.write('----|-----------|-----|\n')
  for c in varcodes:
   code,codename = get_varcodename(c)
   out = '%s|%s|%s|' %(code,codename,d[c])
   f.write(out+'\n')
 print(len(varcodes),'matching varcodes written to',fileout)

def get_codename(c):
 if c == '?':
  return 'unmatched'
 if c == 'S':
  return 'special'
 if c == '3':
  return 'no drop'
 if c == '3nasal':
  return 'insert nasal'
 m = re.search(r'^3(.*)$',c)
 end = m.group(1)
 return 'drop final %s'%end

def get_variants_by_code(recs,c):
 # number of recs with mwcode == c which
 # have krmvariant set
 recs1 = [r for r in recs if r.mwcode == c]
 nc = len(recs1)
 n = 0
 for rec in recs1:
  if rec.krmvariant == None:
   continue
  if rec.krmvariant == -1:
   continue
  n = n + 1  # some variant spelling used
 return n,nc

def write_codes(fileout,recs):
 d = {}
 for rec in recs:
  c = rec.mwcode
  if c not in d:
   d[c] = 0
  d[c] = d[c] + 1
 codes = sorted(d.keys())

 # write markdown format table
 with codecs.open(fileout,"w","utf-8") as f:
  f.write('code|description|count|# other variations|\n')
  f.write('----|-----------|-----|-----|\n')
  for i,c in enumerate(codes):
   codename = get_codename(c)
   num_variants,nc = get_variants_by_code(recs,c)
   assert nc == d[c]
   out = '%s|%s|%s|%s|' %(c,codename,d[c],num_variants)
   f.write(out+'\n')
 print(len(codes),'matching codes written to',fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  krm_verb_filter.txt
 filein1 = sys.argv[2] # mwverbs1
 #filein2 = sys.argv[3]  # west_mw_map.txt
 fileout = sys.argv[3]  # krm_verb_filter_map.txt
 filecode = sys.argv[4] #  krm_verb_filter_codes.txt
 filevar = sys.argv[5]  # krm_verb_filter_variants.txt
 #fileout2a = sys.argv[6] # extension of west_mw_map
 recs = init_verb(filein)
 mwverbrecs,mwverbsd= init_mwverbs(filein1)


 krmmap(recs,mwverbsd)
 write(fileout,recs)
 write_codes(filecode,recs)
 write_variants(filevar,recs)
