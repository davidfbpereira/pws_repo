
# Input: 1) it requires the presence of the original files in the following directory: /files/originals/
# and 2) requires the existence of the following directory: /files/processed/

# Main function: to process the original .csv files into .txt files with a predefined format

# Output: .txt files with the following format: "count, probability, password\n",
# pickle file containing all processed datasets in the form of a pickled object
# and it also prints in the terminal the following meta-information: repeated passwords, 
# total dataset size and the amount of unique/duplicated of passwords in each original dataset file


import os, csv, pickle
from numpy import format_float_scientific


cur_path = os.path.dirname(__file__)
read_path = os.path.relpath('../files/originals/', cur_path)
write_path = os.path.relpath('../files/processed/', cur_path)


# creates a new pickle file with all 3 processed datasets in the form of a pickled object
def save_data(datasets):
	filename = 'processed.pickle'

	pickled_file = open(os.path.join(write_path, filename), 'wb')
	pickle.dump(datasets, pickled_file)

# writes a new .txt file with the processed dataset statistics with the following predefined format: "count, probability, password\n"
def process(file, pre_processed_dataset, stats):
	newFile = file.split('.')[0] + 'V1.txt'

	with open(os.path.join(write_path, newFile), 'w') as output_file:
		for password, count in pre_processed_dataset.items():
			probability = count / stats.get('Dataset size')
			formated_prob = format_float_scientific(probability, exp_digits=1, precision=6)
			dataRow = str(count) + ', ' + formated_prob + ', ' + password + '\n'

			output_file.write(dataRow)
	output_file.close()

	print('\t> The following file was successfully created:', newFile)
	print('\t> Dataset stats of', newFile, ':', stats)

# returns a dictionary with the following stats: total dataset size and the number of unique/duplicated passwords within the dataset
def password_counter(pre_processed_dataset):
	stats = {'Unique passwords' : 0, 'Duplicated passwords' : 0, 'Dataset size' : 0}

	for password, count in pre_processed_dataset.items():
		stats['Dataset size'] += count

		if count == 1:
			stats['Unique passwords'] += 1
		else:
			stats['Duplicated passwords'] +=1

	return stats

# returns a data structure with all passwords and their respective count, after pre-processing (removing duplicated passwords) the original .csv file
def pre_process_csv(file):
	processed_dataset, repeated_passwords = {}, []

	with open(os.path.join(read_path, file), 'r') as input_file:
		reader = csv.reader((line.replace('\0','') for line in input_file))
		next(reader)			# skip the first line, because it contains the following header text: "password, frequency\n"
		for line in reader:
			count, password = int(line[1]), line[0]		# line[0] corresponds to the first row, while line[1] corresponds to the second row

			if password in processed_dataset:			# meaning that it is a duplicated entry in the original dataset file...
				repeated_passwords.append([password, count])
				processed_dataset[password] += count
			else:
				processed_dataset[password] = count
	
	if repeated_passwords:
		print('\t> The following repeated passwords and their counts were found:')
		for element in repeated_passwords:
			print('\t\tpassword:', element[0], '|| count:', element[1])
	else:
		print('\t> No repeated passwords were found...')

	return processed_dataset


def main():
	# input .csv files stored in the following directory: /files/originals/
	original_files = ['RockYou.csv', 'LinkedIn.csv', '000WebHost.csv']

	# output data structure that will contain the 3 processed datasets, with their respective passwords and countings, to be pickeled at the end
	datasets = []

	for file in original_files:
		processed_dataset = pre_process_csv(file)		# remove duplicated entries
		datasets.append({file.split('.')[0] + 'V1.txt' : processed_dataset})
		stats = password_counter(processed_dataset)		
		process(file, processed_dataset, stats)

	save_data(datasets)	

	# pickled object has the following format:

	'''
	[ 	{ 'RockYouV1.txt' : 	{'password1' : count1, 'password2' : count2, ... }		}, 
		{ 'LinkedInV1.txt' : 	{'password1' : count1, 'password2' : count2, ... }		}, 
		{ '000WebHostV1.txt' : 	{'password1' : count1, 'password2' : count2, ... }		}	]
	'''

	# compute stats (after cleaning the datasets?)...

if __name__ == "__main__":
	main()


