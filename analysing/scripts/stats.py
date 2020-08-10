# Input 1: pickle files previously assembled

# Main function: to compute the pre and post attack password classification distributions,
# according to: full sample, dataset, individual sample

# Output: pre_stats and post_stats in the following directory ../stats_files/

import decimal
import os, pickle


cur_path = os.path.dirname(__file__)
write_stats_path = os.path.relpath('../stats_files/', cur_path)
read_pickle_path = os.path.relpath('../pickle_files/', cur_path)



def save_data(pre_data, post_data):
	pre_stats_filename = 'pre.stats'
	post_stats_filename = 'post.stats'
	file = open(os.path.join(write_stats_path, pre_stats_filename), 'w')
	file.write(pre_data)
	file = open(os.path.join(write_stats_path, post_stats_filename), 'w')
	file.write(post_data)

	print('The following files were created:', pre_stats_filename, post_stats_filename)

def process_attack_stats(output, file, attack_stats, pre_stats, passwords_len):
	#print(output, file, attack_stats, pre_stats, passwords_len)

	banner = '# ---------------------------------------------------------------------------------------------- #\n'
	header = '\t' + output + ' ;\t' + str(passwords_len) + ' passwords ;  \t' + file + '\n'
	pretty_stats = '\n' + banner + header + banner + '\n'

	for meter, evaluations in attack_stats.items():
		line = ''
		for level, count in evaluations.items():
			if count == 0:
				pre_percentage = sum(pre_stats[meter].values())
				line = line + level + ': ' + str(count) + " (0'" + str(round(pre_stats[meter][level]/pre_percentage * 100, 2)) + '%) '
			elif pre_stats[meter][level] == 0:
				line = line + level + ': ' + str(count) + ' (0%) '
			else:
				pre_percentage = sum(pre_stats[meter].values())
				cracked_percentage = round(count/pre_stats[meter][level]*pre_stats[meter][level]/pre_percentage*100, 2)
				uncracked_percentage = round(pre_stats[meter][level]/pre_percentage*100 - cracked_percentage, 2)
				#print(level, count, cracked_percentage, uncracked_percentage)

				line = line + level + ': ' + str(count) + ' (' + str(cracked_percentage) + "'" + str(uncracked_percentage) + ')% '

		pretty_stats = pretty_stats + '{0:^15}'.format(meter) + ' -  ' + line[:-1] + '\n'
	return pretty_stats

def process_stats(output, file, stats, passwords_len):
	banner = '# ---------------------------------------------------------------------------------------------- #\n'
	header = '\t' + output + ' ;\t' + str(passwords_len) + ' passwords ;  \t' + file + '\n'
	pretty_stats = '\n' + banner + header + banner + '\n'

	for meter, evaluations in stats.items():
		line = ''
		for level, count in evaluations.items():
			line = line + level + ': ' + str(count) + ' [' + str(round(decimal.Decimal(count/passwords_len * 100), 2)) + '%] '
		pretty_stats = pretty_stats + '{0:^15}'.format(meter) + ' -  ' + line[:-1] + '\n'
	return pretty_stats

def get_stats(passwords):
	stats = {
		'twitter' 			: {'Curta demais' : 0, 'Fraca' : 0, 'Bom' : 0, 'Forte' : 0, 'Muito forte' : 0},
		'airbnb' 			: {'Weak' : 0, 'Fair' : 0, 'Strong' : 0},			# Weak, Fair, Strong for exp_1 || weak, good, strong for exp_2
		'bestbuy' 			: {'Not Strong Enough' : 0, 'Acceptable' : 0, 'Strong' : 0},
		'haveibeenpwned' 	: {'not found': 0, '1' : 0, '2-5' : 0, '6-50' : 0, '51-...' : 0},
		'cryptowallet' 		: {'1' : 0, '2' : 0, '3' : 0, '4' : 0, '5' : 0},
		'dropbox' 			: {'Weak' : 0, 'So-so' : 0, 'Good' : 0, 'Great!' : 0},
		'facebook' 			: {'Too short' : 0, 'Weak' : 0, 'Medium' : 0, 'Strong' : 0},
		'reddit' 			: {'0%' : 0, '25%' : 0, '50%' : 0, '75%' : 0, '100%' : 0},
		'thehomedepot' 		: {'Weak' : 0, 'Fair' : 0, 'Strong' : 0},
		'microsoftV3' 		: {'Weak' : 0, 'Medium' : 0, 'Strong' : 0, 'Very strong' : 0},
		'slack' 			: {'Muito fraca' : 0, 'Fraca' : 0, 'Média' : 0, 'Boa' : 0, 'Ótima' : 0},
		'target' 			: {'Too Short' : 0, 'Weak' : 0, 'Average' : 0, 'Good' : 0, 'Strong' : 0, 'Too Long' : 0, 'Cannot Contain ~ Or Spaces.' : 0},
		'zxcvbn' 			: {'0 / 4' : 0, '1 / 4' : 0, '2 / 4' : 0, '3 / 4' : 0, '4 / 4' : 0}	
	}

	for data in passwords:
		for password, evaluations in data.items():
			for meter, result in evaluations.items():
				if meter == 'haveibeenpwned':				# this quantization can be altered into a different scale/number of bins
					if result == 'not found':
						stats[meter]['not found'] += 1
					elif 1 == int(result):
						stats[meter]['1'] += 1
					elif 2 <= int(result) <= 5:
						stats[meter]['2-5'] += 1
					elif 6 <= int(result) <= 50:
						stats[meter]['6-50'] += 1
					else:
						stats[meter]['51-...'] += 1
				else:
					stats[meter][result] += 1
	return stats

def get_post_distributions(pickle_object, pickle_filename):
	pre_global, pre_dataset, pre_samples = [], {}, {}

	for output, datasets in pickle_object.items():
		for file, passwords in datasets.items():
			if file.startswith('RockYou'):
				if 'RockYou' not in pre_dataset:
					pre_dataset['RockYou'] = passwords[:]
				else:
					pre_dataset['RockYou'].extend(passwords)
				
			if file.startswith('LinkedIn'):
				if 'LinkedIn' not in pre_dataset:
					pre_dataset['LinkedIn'] = passwords[:]
				else:
					pre_dataset['LinkedIn'].extend(passwords)

			if file.startswith('000WebHost'):
				if '000WebHost' not in pre_dataset:
					pre_dataset['000WebHost'] = passwords[:]
				else:
					pre_dataset['000WebHost'].extend(passwords)

			if file not in pre_samples:
				pre_samples[file] = passwords[:]
			else:
				pre_samples[file].extend(passwords)

			pre_global.extend(passwords)

	pre_global_stats = get_stats(pre_global)

	for dataset, passwords in pre_dataset.items():
		pre_dataset[dataset] = get_stats(passwords)

	for file, passwords in pre_samples.items():
		pre_samples[file] = get_stats(passwords)
		

	global_sample, post_dataset, post_samples = [], {}, {}
	post_data = '\n\n\n\t\t\t\t' + pickle_filename.split('.')[0].upper() + '\n'

	for output, datasets in pickle_object.items():
		for file, passwords in datasets.items():
			if output == 'cracked':
				if file.startswith('RockYou'):
					if 'RockYou' not in post_dataset:
						post_dataset['RockYou'] = passwords[:]
					else:
						post_dataset['RockYou'].extend(passwords)
					
				elif file.startswith('LinkedIn'):
					if 'LinkedIn' not in post_dataset:
						post_dataset['LinkedIn'] = passwords[:]
					else:
						post_dataset['LinkedIn'].extend(passwords)

				else:
					if '000WebHost' not in post_dataset:
						post_dataset['000WebHost'] = passwords[:]
					else:
						post_dataset['000WebHost'].extend(passwords)

				if file not in post_samples:
					post_samples[file] = passwords[:]
				else:
					post_samples[file].extend(passwords)

				global_sample.extend(passwords)

	global_stats = get_stats(global_sample)
	post_data += process_attack_stats('attacking phase', 'full sample', global_stats, pre_global_stats, len(global_sample))

	for dataset, passwords in post_dataset.items():
		post_dataset_stats = get_stats(passwords)		
		post_data += process_attack_stats('attacking phase', dataset, post_dataset_stats, pre_dataset[dataset], len(passwords))

	for dataset, passwords in post_samples.items():
		post_samples_stats = get_stats(passwords)
		post_data += process_attack_stats('attacking phase', dataset, post_samples_stats, pre_samples[dataset], len(passwords))

	return post_data

def get_pre_distributions(pickle_object):
	dataset_samples = {}
	samples, global_sample = {}, []
	pre_data = ''

	for output, datasets in pickle_object.items():
		for file, passwords in datasets.items():
			if file.startswith('RockYou'):
				if 'RockYou' not in dataset_samples:
					dataset_samples['RockYou'] = passwords[:]
				else:
					dataset_samples['RockYou'].extend(passwords)
				
			elif file.startswith('LinkedIn'):
				if 'LinkedIn' not in dataset_samples:
					dataset_samples['LinkedIn'] = passwords[:]
				else:
					dataset_samples['LinkedIn'].extend(passwords)

			else:
				if '000WebHost' not in dataset_samples:
					dataset_samples['000WebHost'] = passwords[:]
				else:
					dataset_samples['000WebHost'].extend(passwords)

			if file not in samples:
				samples[file] = passwords[:]
			else:
				samples[file].extend(passwords)

			global_sample.extend(passwords)

	pre_global_stats = get_stats(global_sample)
	pre_data += process_stats('pre attacking phase', 'full sample', pre_global_stats, len(global_sample))

	for dataset, passwords in dataset_samples.items():
		pre_dataset_stats = get_stats(passwords)
		pre_data += process_stats('pre attacking phase', dataset, pre_dataset_stats, len(passwords))

	for file, passwords in samples.items():
		pre_sample_stats = get_stats(passwords)
		pre_data += process_stats('pre attacking phase', file, pre_sample_stats, len(passwords))

	return pre_data


def main():
	pre_data, post_data = '', ''

	for subdir, dirs, files in os.walk(read_pickle_path):
		for pickle_filename in files:
			if pickle_filename.endswith('.pickle'):
				print(pickle_filename)
				pickle_file = open(os.path.join(read_pickle_path, pickle_filename), 'rb')
				pickle_object = pickle.load(pickle_file)
				
				post_data += get_post_distributions(pickle_object, pickle_filename)

	pre_data = get_pre_distributions(pickle_object)

	save_data(pre_data, post_data)


if __name__ == "__main__":
	main()