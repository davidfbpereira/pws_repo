

import os, sys, math, pickle


cur_path = os.path.dirname(__file__)
read_results = os.path.relpath('../results/')
read_datasets = os.path.relpath('../../sampling/samples')


def save_data(assembled_results):
	filename = 'query_results.pickle'
	pickled_file = open(os.path.join(read_results, filename), 'wb')
	pickle.dump(assembled_results, pickled_file)
	print('The following file was created:', filename)

def assemble_results():
	assembled_results = {}

	for subdir, dirs, files in os.walk(read_results):
		for file in files:
			if file.endswith('.txt'):
				meter, dataset = file[:-4].split('_')[0:2]
								
				if dataset not in assembled_results:
						assembled_results[dataset] = {}

				for line in open(os.path.join(subdir, file)):
					password = line[30:].rstrip('\n')
					if meter == 'zxcvbn':
						evaluation = line[11:30].rstrip()
					else:
						evaluation = line[0:30].rstrip()

					if password in assembled_results[dataset]:
						assembled_results[dataset][password][meter] = evaluation
					else:
						assembled_results[dataset][password] = {meter : evaluation}

	return assembled_results
	
def main():
	assembled_results = assemble_results()
	save_data(assembled_results)
	
		
if __name__ == "__main__":
	main()

