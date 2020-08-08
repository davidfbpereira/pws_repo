./john --format=plaintext --wordlist="Top304Thousand-probable-v2.lst" --rules:custom sample.hash --pot=experiment.pot --conf=john.conf --external=AutoStatus 2> experiment.log

# sample.hash > concatenation of all dataset samples into the same file
# Top304Thousand-probable-v2.dict > https://github.com/berzerk0/Probable-Wordlists
# custom.rule > stock, SpiderLabs and Megatron mangling rules