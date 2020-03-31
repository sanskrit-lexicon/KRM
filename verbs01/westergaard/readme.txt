
This work is incomplete.
It deals with 
* mw dictionary
* Westergaard Dhatupatha
* Sayana's Madhaviya Dhatuvrtti

Start with two files, produced in 2009.

* mw-wdp.txt
 copied from /c/ejf/LexFund/Westergaard/mwtab/
This shows correspondence between 'wsid' (Westergaard sutra id) and
MW key1 and L (cologne record id). For instance:
1. <key1>ADI</key1><ls>Dha1tup._xxiv_,_68<wsid>24.68</wsid></ls><L>24187</L>
There are 1619 such correspondences.  
Note that sometimes two different Westergaard sutras are mentioned in
connection with 1 MW entry. For instance:
2. <key1>svid</key1><ls>Dha1tup._xviii_,_4<wsid>18.4</wsid></ls><L>259802</L>
3. <key1>svid</key1><ls>Dha1tup._xxvi_,_79<wsid>26.79</wsid></ls><L>259802</L>

* wdp-mw.xml
 copied from /c/ejf/LexFund/Westergaard/wdp/

This shows correspondence between wsid and sutras of Madhaviya dhatupatha.
For each Madhaviya sutra entry,  the corresponding one or more Westergaard
sutra entries are provided, along with the Westergaard root spelling for each
sutra.  
There are 1491 of these madhaviya sutras;  these have a single corresponding
Westergaard sutra except in 230 cases (which have one or more Westergaard
sutra correspondences.
It also shows the 'sense' from the Madhaviya sutra.


Following the examples above:
1. wsid = 24.68
<sutra msid="02.0084"><root wsid="24.68">dIDIN</root><sense>dIptidevanayoH</sense></sutra>
2. wsid = 18.4
<sutra msid="01.0481"><root wsid="18.4">YizvidA</root><sense mdp="snehasya mocane ca">snehanamocanayoH</sense></sutra>
3. wsid = 26.79
<sutra msid="04.0084"><root wsid="26.79" mdp="zvidA">YizvidA</root><sense>gAtraprakzaraRe</sense></sutra>

* west_mw_map.txt
 This combines wdp-mw.xml and mw-wdp.txt
python west_mw_map.py wdp-mw.xml mw-wdp.txt west_mw_map.txt

1491 records in wdp-mw.xml are xml '<sutra>' elements
1426 of these can be readily parsed.  
 The other 65 are currently ignored.
There are 1808 distinct wsid values in sutras.
3 of these correspond to multiple sutra records
['4.40', '7.72', '7.74']


All 1619 records in  mw-wdp.txt can be parsed.
Each of these has a wsid (Westergaard sutra number), and
 a key1,L from MW.
Some sutras are mentioned in multiple MW records.
There are 1327 distinct wsid values.
227 of these are associated with multiple MW records.

Format of west_mw_map.txt:
1811 records
5 colon-separated fields:
 wsid  Westergaard sutra id
 wroot Westergaard root spellings
       sometimes there is a different Madhaviya spelling;
       Example:  wdp root = GagGa,  mdp root = GaGa.  
        wroot = GaGga/GaGa   (i.e. '/' separation)
 sense Westergaard sense.  As with root, sometimes there is a different
       sense from Madhaviya. 
 msid  Madhaviya sutra id
 mw    key1,L    Sometimes there are multiple cases. This occurs when
       there are the given Dhatupatha reference is mentioned under more than
       one entry of MW.
       There are 201 such cases.  In such a case, the key1,L elements are
       separated by ';'. 
       Example:  2.4:bADf:loqane:01.0006:bAD,144318;loqana,182923

