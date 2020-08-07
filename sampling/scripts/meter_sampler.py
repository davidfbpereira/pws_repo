
# Input: 1) it requires the presence of the cleaned pickled file in the following directory: ../../filtering/files/cleaned/

# Main function: to sample each dataset into new .txt files with a predefined format and size

# Output: .txt files with the following format: "password\n",
# with the following name: "[dataset]_Sample_10000.txt",
# in the following directory: ../samples/


import os, pickle, random


cur_path = os.path.dirname(__file__)
read_path = os.path.relpath('../../filtering/files/cleaned/', cur_path)
write_path = os.path.relpath('../samples/', cur_path)


# writes a new .txt sample file for each dataset with the following predefined format: "password\n"
def sample(datasets):
	# set structure that will contain all passwords that were sampled thus far
	already_sampled = set()

	for dataset in datasets:
		for file, passwords in dataset.items():
			print('\n\t> Randomly sampling the following dataset file:', file)

			# generate a new sample while having into account the passwords that were already sampled || k is the desired sample size
			new_sample = random.sample(set(passwords) - already_sampled, k = 10000)

			sample_filename = file.split('.')[0][:-2] + '_Sample_10000.txt'
			with open(os.path.join(write_path, sample_filename), 'w') as output_file:
				for password in new_sample:
					output_file.write(password + '\n')
			output_file.close()

			already_sampled.update(new_sample)		# update the set structure with the newly sampled passwords, so as to avoid duplicates

def main():
	# input data structure that contains the 3 cleaned datasets, with their respective passwords after filtering
	cleaned_pickle = 'cleaned.pickle'

	# loading the pickled file containing the cleaned datasets
	input_file = open(os.path.join(read_path, cleaned_pickle), 'rb')
	datasets = pickle.load(input_file)
	
	sample(datasets)

if __name__ == "__main__":
	main()


