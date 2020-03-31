
This work was done in a temporary folder temp_verbs02 of csl-orig/v02/krm/.
The initial aim was to find correspondences between the krm headwords of
the Cologne digitization and mw root spellings.
A secondary goal was to similarly find correspondences between the
DAtupAWa sutras and MW root spellings. For the DAtupAWa sutras, this study
uses a 2009 extract (mdp.xml) of 
Peter Scharf's digitization of mADavIyaDAtuvftti of sAyaRa 
(ref: https://sanskritlibrary.org/Sanskrit/Vyakarana/Dhatupatha/index2.html).


* mwverbs
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
#copy from v02/mw/temp_verbs
#cp ../../mw/temp_verbs/verb.txt mwverbs.txt
each line has 5 fields, colon delimited:
 k1
 L
 verb category: genuinroot, root, pre,gati,nom
 cps:  classes and/or padas. comma-separated string
 parse:  for pre and gati,  shows x+y+z  parsing prefixes and root

* mwverbs1.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
Merge records with same key (headword)
Also  use 'verb' for categories root, genuineroot, nom
and 'preverb' for categories pre, gati.
Format:
 5 fields, ':' separated
 1. mw headword
 2. MW Lnums, '&' separated
 3. category (verb or preverb)
 4. class-pada list, ',' separated
 5. parse. Empty for 'verb' category. For preverb category U1+U2+...+root

* krm_verb_filter.

python krm_verb_filter.py ../krm.txt krm_verb_filter.txt


Each entry of krm is a verb.
There is currently no pattern searching involved;
rather just use the k1,k2,L of the metaline for each entry.
Also, note that k2 is same as k1 in this digitization.

Counts of total patterns:

2061 verbs written to krm_verb_filter.txt

Format of file krm_verb_filter.txt:
;; Case 0001: L=1, k1=aka, k2=aka, code=1

* krm_sense.txt
python krm_sense.py ../krm.txt krm_sense.txt

2061 cases, 1 for each entry of krm.
Sample:
;; Case= 0144, L=139, k1=kaka, fullroot=kaka, sense="lOlye"
fullroot oddities:
1) premarker. 51 cases
;; Case= 0073, L=70, k1=inDI, fullroot=Yi inDI, sense="dIptO"
2) multiple values for fullroot.  3 cases
;; Case= 0151, L=146, k1=kawi, fullroot=kawi/kawI, sense="gatO"

There are many instances of 2 or more entries of krm that have the same key1:
1699 unique values of k1
1408 values of k1 with 1 records
0230 values of k1 with 2 records
0052 values of k1 with 3 records
0008 values of k1 with 4 records
0001 values of k1 with 5 records   
values of k1 with 4 entries=qipa, tfpa, puza, vawa, vasa, vida, SaWa, SraTa
values of k1 with 5 entries=luwa

python krm_verb_filter_map.py krm_verb_filter.txt mwverbs1.txt krm_verb_filter_map.txt krm_verb_filter_codes.txt krm_verb_filter_variants.txt

Get correspondences between krm verb spellings and
 - krm verb spellings
 - mw verb spellings

Note we use :
a. the krm verb spelling (closely related to spelling from some DAtupAWa
b. thw mw verb spellings, from MW ditionary

Format of krm_verb_filter_map.txt:
 Adds a field mw=xxx to each line of krm_verb_filter.txt,
indicating the MW root believed to correspond to the KRM root.
For example, aMSa in KRM is believed to correspond to aMS in MW.
;; Case 0001: L=4, k1=aMSa, k2=aMSa, code=r, mw=aMS

In 20 cases, no correspondence could be found. These use 'mw=?'. For example:
;; Case 0056: L=6356, k1=iBa, k2=iBa, code=X, mw=?

The 'code' is a complex coding of  match between krm (k1) and mw.
It has two parts A-B.
A indicates changes regarding dropping final characters of k1 or
inserting a nasal in k1.
B indicates other changes, such as changing initial 'z' to 's', intial 'R' to
'n'.
Two additional files summarizing these codes are prepared:
krm_verb_filter_codes.txt   (the various 'A' values, and number of 'B' values)

3|no drop|162|13|   means that there are 162 codes of form A-X (for some X)
  and all but 13 of these were 'NC' (no change) in the B part of code.
The description 'no drop' means there were no ending characters dropped,
nor nasal insertions made.
3a|drop final a|1037|85|  means there are 1037 cases where the match required
 dropping of a final 'a' in the KRM spelling. And 85 of these required 
 some other spelling variation.


krm_verb_filter_variants.txt gives similar information regarding the 'B'
part of the 'A-B' code values.

S|Special|112|   these are 'ad hoc' mappings of krm to mw, rather than
    some more systematic change
NC|no extra change|1793| means that 1793 mappings occured with only the
   changes as indicated by the A part of the A-B code.
The other code values are two digits, with a description representing
   a regular expression substition that was made to the krm spelling.
   For example
00|^R -> n|34|  means that code '00' changed an initial 'R' (retroflex nasal)
   to 'n'. For example root 'RI' in KRM corresponds to 'nI' in mw.
   34 of the matches made use of this change.


* krm_sense.txt
python krm_sense.py ../krm.txt krm_sense.txt

For comparison with Madhaviya DP, we want to pull the DP reference from
the first line of each krm entry.  
Sample:
;; Case= 0001, L=1, k1=aka, fullroot=aka, sense="kuwilAyAM gatO"
Here k1 is the value of the 'k1' parameter in the metaline ( same as 'key1'
value in the xml version krm.xml at Cologne).
'fullroot' consists of the premarker (if any) in krm's dp quote, along
with the root and its usually affixed marker. Example with premarker (Yi)
;; Case= 0073, L=70, k1=inDI, fullroot=Yi inDI, sense="dIptO"

In 3 cases the full root has alternate values. Example
;; Case= 0151, L=146, k1=kawi, fullroot=kawi/kawI, sense="gatO"

* krm_sense_map.txt
This combines the mw mapping of krm_verb_filter_map.txt with the
information in krm_sense.txt.
Sample (with the new 'mw=ak' and 'code=3a-NC' information).
;; Case= 0001, L=1, k1=aka, fullroot=aka, mw=ak, code=3a-NC, sense="kuwilAyAM gatO"

* mdp.xml copied from /c/ejf/LexFund/mwmdpsummary/mdp.xml .
The current work starts with this extract from mADavIyaDAtuvftti digitization.

* mdp_parse.txt

python mdp_parse.py mdp.xml mdp_parse.txt

mdp_parse.txt provides some simplification of mdp.xml
Recall
2274 cases. Sample:
;; Case= 1199, sid=02.005-01, fullroot=duha, sense="prapUraRe"

Fullroot can have a premarker. 57 cases. Sample:
;; Case= 0080, sid=01.057-01, fullroot=wu nadi, sense="samfdDO"

compound sense values are hyphenated:
;; Case= 0078, sid=01.055-01, fullroot=gaqi, sense="vadana-ekadeSe"
Contrast to krm_sense.txt, where the components are joined by sandhi:
;; Case= 0383, L=374, k1=gadi, fullroot=gadi, sense="vadanEkadeSe"


There are many instances of 2 or more entries of mdp that have the same 
  k1. Here k1 = fullroot, but ignoring the premarker. For example,
  the k1 for 'wu nadi' is taken as 'nadi'.

1755 unique values of k1
1361 values of k1 with 1 records
0295 values of k1 with 2 records
0080 values of k1 with 3 records
0013 values of k1 with 4 records
0005 values of k1 with 5 records
0001 values of k1 with 6 records
values of k1 with 5 entries=vawa, luwa, SraTa, vasa, tfpa
values of k1 with 6 entries=vida

* mdp_parse_map.txt
mdp vs. mw
python mdp_verb_filter_map.py mdp_parse.txt mwverbs1.txt mdp_parse_map.txt mdp_parse_codes.txt mdp_parse_variants.txt

Add mw root headword spelling, and code indicating the transformations 
of the mdp fullroot spelling used to get the mw root spelling.
This code is similar to the A-B code used in krm_verb_filter_map; see the
description above.
Samples:
;; Case= 0001, sid=01.001-01, fullroot=BU, sense="sattAyAm", mw=BU, code=3-NC
;; Case= 0002, sid=01.003-01, fullroot=eDa, sense="vfdDO", mw=eD, code=3a-NC
;; Case= 0020, sid=01.018-02, fullroot=svarda, sense="AsvAdane", mw=svad, code=S-S

* krm_mdp_mw.txt
merge krm and mdp using the mappings to mw 
of krm_sense_map.txt for krm
and of mdp_parse_map.txt for mdp.

python krm_mdp_mw.py slp1 krm_sense_map.txt mdp_parse_map.txt krm_mdp_mw.txt krm_mdp_nomw.txt

Devanagari versions of output
python krm_mdp_mw.py deva krm_sense_map.txt mdp_parse_map.txt krm_mdp_mw_deva.txt krm_mdp_nomw_deva.txt

