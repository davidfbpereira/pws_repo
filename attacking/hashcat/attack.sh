hashcat -a 0 -m 99999 sample.hash Top304Thousand-probable-v2.dict -r rules/custom.rule --potfile-disable --outfile-format=10 -o hashcat.out

# sample.hash > concatenation of all dataset samples into the same file
# Top304Thousand-probable-v2.dict > https://github.com/berzerk0/Probable-Wordlists
# custom.rule > Best64, T0XlC and Generated2 mangling rules