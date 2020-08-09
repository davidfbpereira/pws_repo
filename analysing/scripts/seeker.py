
# Input 1: text file from a given cracking tool containing the cracked passwords;
# Input 2: text file of the original sample containing all passwords (sample.hash);

# Main function: to build a nested data structure with all passwords,
# separated according to the various files where they belong and 
# with their respective classifications from the meters results;

# Output: pickle file containing a serialized python object with the final data,
# in the following directory: ../pickle_files/

import os, pickle
from pathlib import PurePath


cur_path = os.path.dirname(__file__)
results_path = os.path.relpath('../../querying/results/', cur_path)
attacks_path = os.path.relpath('../attack_files', cur_path)
output_path = os.path.relpath('../pickle_files/')



def save_data(attack_file, data):
	pickle_filename = attack_file.split('.')[0] + '.pickle'
	pickled_file = open(os.path.join(output_path, pickle_filename), 'wb')
	pickle.dump(data, pickled_file)

	print('The following file was created:', pickle_filename)

# gets the dataset for each cracked and uncracked password
def assemble(query_results, cracked):
	cracked_datasets, uncracked_datasets = {}, {}

	for dataset, passwords in query_results.items():
		for password, classifications in passwords.items():
			print(dataset, password, classifications)
			if password in cracked:
				if dataset not in cracked_datasets:
					cracked_datasets[dataset] = {}
				cracked_datasets[dataset][password] = classifications

			else:
				if dataset not in uncracked_datasets:
					uncracked_datasets[dataset] = {}
				uncracked_datasets[dataset][password] = classifications
						
	data = {'cracked' : cracked_datasets, 'uncracked' : uncracked_datasets}
	return data
	
# returns the set of cracked passwords (CP) and the set of uncracked passwords (UP = Batch - CP)
def process_attack_file(attack_file):
	cracked, sample = [], []

	if attack_file.split('.')[0] == 'johntheripper':
		for line in open(os.path.join(attacks_path, attack_file)):
			if line.startswith('?:'):							# format of the jtr file is '?:password\n'
				cracked.append(line[2:].rstrip('\n'))
	elif attack_file.split('.')[0] == 'hashcat':
		for line in open(os.path.join(attacks_path, attack_file)):
			cracked.append(line.rsplit(':', 1)[0].rstrip('\n'))			# format of the hc file is 'password:guesses\n'
	else:				# conditional clause related to probabilistic models (markov, pcfg and neural) output files from PGS 
		for line in open(os.path.join(attacks_path, attack_file)):
			if not line.rstrip('\n').endswith('-5'):			# format of the PGS file is 'password\tguess_number\n'
				cracked.append(line.split('\t')[0])		# PGS rates '-5' to uncracked passwords

	for line in open('sample.hash'): 			# whole sample from the experiment						
		sample.append(line.rstrip('\n'))			# format of the sampled file is 'password\n'

	cracked = set(cracked)
	uncracked = [password for password in sample if password not in cracked]

	return cracked, uncracked

def load_pickle():
	pickle_filename = 'query_results.pickle'	
	file = open(os.path.join(results_path, pickle_filename),'rb')
	query_results = pickle.load(file)

	return query_results


def main():
	query_results = load_pickle()

	for subdir, dirs, files in os.walk(attacks_path):
		for attack_file in files:
			if attack_file.endswith('.out'):
				cracked, uncracked = process_attack_file(attack_file)
				print(attack_file, len(cracked), len(uncracked))

				data = assemble(query_results, cracked)
				save_data(attack_file, data)

	# ... with the following format:

	'''
	{ cracked: 
		{ RockYou_Results.txt: [
			{ password1: { meter1: result1, meter2: result2, ... } },
			{ password2: { meter1: result1, meter2: result2, ... } }, 
			... ],
		... },
	  uncracked: 
	 	{ RockYou_Results.txt: [
			{ password1: { meter1: result1, meter2: result2, ... } },
			{ password2: { meter1: result1, meter2: result2, ... } }, 
			... ],
		... }
	}	
	'''

if __name__ == "__main__":
	main()


