echo "krm_sense"
python krm_sense.py ../krm.txt krm_sense.txt
echo "mdp_parse"
python mdp_parse.py mdp.xml mdp_parse.txt
echo "mdp_parse_map"
python mdp_verb_filter_map.py mdp_parse.txt mwverbs1.txt mdp_parse_map.txt mdp_parse_codes.txt mdp_parse_variants.txt
echo "krm_verb_filter"
python krm_verb_filter.py ../krm.txt krm_verb_filter.txt
echo "krm_verb_filter_map"
python krm_verb_filter_map.py krm_verb_filter.txt mwverbs1.txt krm_verb_filter_map.txt krm_verb_filter_codes.txt krm_verb_filter_variants.txt
echo "krm_sense_map"
python krm_sense_map.py krm_sense.txt  krm_verb_filter_map.txt krm_sense_map.txt
echo "krm_mdp_mw and krm_mdp_nomw"
python krm_mdp_mw.py slp1 krm_sense_map.txt mdp_parse_map.txt krm_mdp_mw.txt krm_mdp_nomw.txt

python krm_mdp_mw.py deva krm_sense_map.txt mdp_parse_map.txt krm_mdp_mw_deva.txt krm_mdp_nomw_deva.txt
