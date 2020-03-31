#-*- coding:utf-8 -*-
"""mdp_verb_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs

class Mdp(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')  
  self.line = line
  #m = re.search('sid=(.*?), fullroot=(.*?), sense=(.*?), othrroots=(.*)$',line)
  m = re.search('sid=(.*?), fullroot=(.*?), sense=(.*?)$',line)
  self.sid = m.group(1)
  self.fullroot = m.group(2)
  self.sense = m.group(3)
  #self.othrrootstr = m.group(4)
  #self.othrroots = self.othrrootstr.split('/')
  parts = self.fullroot.split(' ')  # remove premarker (57 cases) if any
  self.k1 = parts[-1]
  self.mdpvariant = None
  self.mwcode = None  # a code describing
 def __repr__(self):
  #ans = 'fullroot=%s, sense=%s, sid=%s, othrroots=%s' %(self.fullroot,self.sense,self.sid,self.othrrootstr)
  ans = 'fullroot=%s, sense=%s, sid=%s' %(self.fullroot,self.sense,self.sid)
  return ans

def init_mdp(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = [Mdp(line) for line in f]
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

class Westmw(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  try:
   self.wsid,self.rootstr,self.sensestr,self.msid,self.mwinfostr = line.split(':')
  except:
   print('Westmw error',line)
   exit(1)
  self.wroots = self.rootstr.split('/')
  self.senses = self.sensestr.split('/')
  self.mwinfostrpairs = self.mwinfostr.split(';')
  self.mwinfopairs = [x.split(',') for x in self.mwinfostrpairs]
  # each element of mwinfopairs is a tuple containing key1 and L (MW reference)
  
  self.used = False
  
def init_westmw(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Westmw(x) for x in f]
 print('init_westmw:',len(recs),"records from",filein)
 """
 d = {}
 for rec in recs:
  wsid = rec.wsid
  if wsid in d:
   print('init_westmw: Unexpected duplicate',wsid)
  d[wsid] = rec
 return recs,d
 """
 return recs

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
mdp2mw_special = {
 'hiWa':'hiw',
 'KarKa':'KakK',
 'depf':'de',  # ? by sense
 'Drana':'DraR',
 'saRa':'san',
 'saRu':'san',
 'rivi':'riRv',
 'ravi':'raRv',
 'varza':'vfz',   # causal?
 'gfha':'grah',   # one of these could point to grfhaya in mw ?
 'gfhi':'grah', 
 'gfhU':'grah', 
 'cakziN':'cakz',
 #'iR':'i',
 'daridrA':'drA', # desiderative
 'puzpa':'puzpya',
 'pUrI':'pF',
 'tUrI':'tur', # or tF
 'tfMhU':'tfh',
 'olaqi':'olaRq',
 'pija':'piYj', # same sense as piji
 'Carda':'Cfd', # causal
 'jYapa':'jYA',  # causal ?
 'kzaya':'kzi', 
 'garDa':'gfD', #causal
 'tatri':'tantraya',
 'kuwumba':'kuwumbaya',
 'basta':'vast',
 'kusma':'kusmaya',
 'sadaH':'sad', # inflected
 'rusi':'ruMS', # not in westergaard
 'vara':'vf',  # causal
 'sAra':'sAraya',
 'goma':'gomaya',
 'kumAra':'kumAraya',
 'kAla':'kAlaya',
 'palpUla':'palpUlaya',
 'nivAsa':'nivas',  # causal of ni+vas
 'BAja':'Baj',  # causal
 'Una':'Unaya',
 'saNketa':'saMketaya',
 'grAma':'grAmaya',
 'guRa':'guRaya',
 'keta':'ketaya',
 'mUtra':'mUtraya',
 'pAra':'pAraya',
 'tIra':'tIraya',
 'bazka':'vazk',  # b/v
 'citra':'citraya',
 'saNgrAma':'saMgrAm', # prefix
 'Cidra':'Cidraya',
 'daRqa':'daRqaya',
 'Ceda':'Cid',  # ?
 'tutTa':'tutTaya',
 'stage':'sTag',  # also sTage
 'basu':'vas', # also vasu
 'asta':'must', #? 
 'klevf':'glev', #?

 'klada':'kland',   # klad also in mw
 'krada':'krand',   # krad also in mw
 'aca':'aYc',  # ac also in mw
 'acu':'aYc',  # ac also in mw.
 'aW':'aRW',   # aW also in mw
 'ucCI':'uC',  # ucCI is preverb in mw.
 'UW':'uW',    # variants acc. to mw
 'F':'f',      # acc. to mw
 'kuwi':'kuRq',  # acc. to mw, == kuRw
 'kubi':'kumb',  # acc. to mw, == kumB
 'kuBi':'kumb',  # mw. kumB vl for kumb
 'kuSa':'kus',   # acc. to mw, == kus
 #'kxp':'kfp',    # ?
 'kzapa':'kzip',  # preraRa
 'cutir':'cyut',    # acc. to mw, cut ~= cyut
 'juna':'juq',    # acc. to mw, jun v.l. for juq
 'taYjU':'taYc',  # acc. to mw, taYj v.l. for taYc
 'tUqf':'tuq',    # acc. to mw, tUq == tuq
 'traKi':'traNk',  # acc. to mw, traNK == traNk == traNg
 'daGi':'daG',    # mw. also has daNG
 'dipf':'tip',    # mw. tip/dip related
 'dfPa':'dfp',    # mw. dfp = dfP
 'DUSa':'DUs',    # mw. DUS = DUz = DUs
 'DUza':'DUs',    # mw. DUS = DUz = DUs
 'DrAGf':'drAG',  # mw. DrAG = drAG
 'Druva':'Dru',   # mw. Druv v.l. for Dru
 'naqi':'naw',    # mw. naq cf. naw
 'pUrRa':'puR', #? mw. pUR cf puR, pUl
 'pfjI':'pfYj',  #mw. pfj == pfYj
 'pyusa':'vyuz',  # mw. pyus vl vyuz
 'plakza':'Blakz', #mw. plakz vl for Blakz (mw correction)
 'plava':'plu',    #mw. plav cf plu
 'plevf':'pev',    #mw. plev cf peb, pev, sev
 'badi':'bad',     #mw. band or bad
 #'bugi':'vuNg',    #mw. buNg or vuNg  for krm
 'behf':'veh',      #mw. beh also written veh
 'byusa':'vyuz',    #mw. byus see vyuz
 'braRa':'vraR',    #mw braR see vraR
 'bruqa':'vruq',    #mw bruq see vruq, vrUs
 'Bidi':'bind',     #mw Bind vl for bind
 'BraSa':'BraMS',   #mw BraS or BraMS
 'miDf':'miT',      #mw miD or meD, = miT
 'muqa':'muw',      #mw muq vl for muw
 'meTf':'miT',      #mw meT strong form of miT
 'makza':'mrakz',   #mw makz cf mrakz
 'raGa':'rak',      #mw raG vl for rak
 'riha':'riP',      #mw rih (vedic form of lih), also vl for riP
 'ruqi':'ruRw',     #mw ruRq see ruRw
 'luqa':'luW',      #mw luq connected with lul and luW
 'luqi':'luRw',     #mw luRq vl for luRw
 'vfhi':'bfh',      #mw vfMh see bfh
 'Scutir':'Scyut',  #mw Scut often written Scyut, cf cyut
 'SloRf':'SroR',    #mw SloR also written SroR
 'sasti':'sas',     #mw saMst = sas
 'sage':'sTag',     #mw sag cf sTag
 'sac':'zac',       # same sense. 
 'zivi':'ninv',     #mw sinv see ninv
 'sila':'Sil',      #mw sil also written Sil
 'suBa':'SuB',       #mw suB vl for SuB   
 'sumBa':'SumB',    #mw sumB see suB
 'sniwa':'snih',    #mw sniw cf. snih
 'spF':'SF',        #mw spF vl for SF
 'sPawa':'sPuw',    # mw sPaw = and vl fo sPuw
 'sPuwi':'sPuw',    # sPuwi == sPuwir
 'srE':'SrE',       # mw srE see SrE, SrA
 'svarda':'svad',   # mw svard cf svad
 'aWa':'aRW',       # mw aRW or aW
 #'bazka':'vask',    # b/v 
 'vAhf':'bAh',      # bAh see vAh
 'svalka':'Svalk',
 '':'',
 '':'',
 '':'',
 '':'',
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

drop_endings = ['a','f','I','e','x','u','U','Y','A','ir','o','N',
   'i','p','Uz','w','R','az','k','z']  # new for mdp, not used in krm.

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
 

def mdpmap_helper2(k1,mwd):
 #rec.mw,rec.mwcode = map2mw(mwd,k1)
 if k1 in mwd:  # 
  return k1,'3'
 for v in drop_endings:
  if v == 'i': 
   # Try homorganic nasal insertion first before dropping the 'i'
   k1a = dpadjust_i(k1)
   if k1 == 'sPuwi':print('helper2: %s -> %s'%(k1,k1a))
   if k1a in mwd:
    return k1a,'3nasal'
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

def dp_mw_variants(k):
 ans = [(k,-1)] # -1 means no change
 #variant_subs = []
 for isub,sub in enumerate(variant_subs):
  r1,r2 = sub
  x = re.sub(r1,r2,k)
  if x not in ans:
   ans.append((x,isub))
 return ans

def mdpmap_rec(rec,mwd):
 #if rec.k1 == 'kuBi':print(rec.k1,rec.k1 in mdp2mw_special)
 if rec.k1 in mdp2mw_special:
  mw = mdp2mw_special[rec.k1]
  #if rec.k1 == 'kuBi':print(rec.k1,mw,mw in mwd)
  if mw in mwd:  # this test for safety. Should always hold
   rec.mw = mdp2mw_special[rec.k1]
   rec.mwcode = 'S'
   rec.mdpvariant = -2  # an 'unknown' change
   return
 variants = dp_mw_variants(rec.k1)
 for variant in variants:  
  k1,mdpvariant = variant
  
  rec.mw,rec.mwcode = mdpmap_helper2(k1,mwd)
  if not rec.mwcode.startswith('?'):
   rec.mdpvariant = mdpvariant
   return
 rec.mwcode='?'
 rec.mw='?'

def mdpmap(recs,mwd):
 for rec in recs:
  mdpmap_rec(rec,mwd)
   

def write(fileout,recs):
 n = 0
 nomw = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   n = n + 1
   line = rec.line
   # combine mwcode and mdpvariant
   var = rec.mdpvariant
   if var == None:
    var = '?'
   elif var == -1:
    var = 'NC'  # no change
   elif var == -2:
    var = 'S'   # special
   else:
    var = '%02d'%var
   code = '%s-%s' %(rec.mwcode,var)
   #line = line.replace('code=1','code='+code)
   out = '%s, mw=%s, code=%s' %(line,rec.mw,code)
   f.write(out + '\n')
   if rec.mw =='?':
    nomw = nomw + 1
 print(n,"records written to",fileout)
 print(nomw,"verb have no mw match")

 

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
  var = rec.mdpvariant
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
 # have mdpvariant set
 recs1 = [r for r in recs if r.mwcode == c]
 nc = len(recs1)
 n = 0
 for rec in recs1:
  if rec.mdpvariant == None:
   continue
  if rec.mdpvariant == -1:
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
 filein = sys.argv[1] #  mdp_parse.txt
 filein1 = sys.argv[2] # mwverbs1
 fileout = sys.argv[3]  # mdp_parse_map.txt
 filecode = sys.argv[4] #  mdp_parse_codes.txt
 filevar = sys.argv[5]  # mdp_parse_variants.txt
 recs = init_mdp(filein)
 mwverbrecs,mwverbsd= init_mwverbs(filein1)
 mdpmap(recs,mwverbsd)
 write(fileout,recs)
 write_codes(filecode,recs)
 write_variants(filevar,recs)
