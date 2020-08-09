
# Input: 1) it requires the presence of the sampled .txt files in the following directory: ../../sampling/samples/
# and 2) requires the existence of the following directory: ../results/

# Main function: to query all samples into a new .txt file with a predefined format

# Output: .txt file with the following format: "classification password\n",
# with the following name: "[meter]_results.txt",
# in the following directory: ../results/

import os, meters
from multiprocessing import Pool
from itertools import repeat


cur_path = os.path.dirname(__file__)
read_path = os.path.relpath('../../sampling/samples', cur_path)
write_path = os.path.relpath('../results', cur_path)


def unite(partitions):
	new_filename = partitions[0].split('_')[0] + '_results.txt'
	new_directory = os.path.join(write_path)

	with open(os.path.join(new_directory, new_filename), 'a') as output_file:
		for partition in partitions:
			with open(os.path.join(new_directory, partition), 'r') as input_file:
				for line in input_file:
					output_file.write(line)
			os.remove(os.path.join(new_directory, partition))
	print('\nThe following results file was successfully created:', new_filename)

def query(chunks):
	print(chunks)
	p = Pool(processes = 6)
	data = p.starmap(meters.zxcvbn, zip(chunks, repeat(1)))
	data.sort()
	p.close()

	return data

def get_chunks():
	chunks = []

	for subdir, dirs, files in os.walk(read_path):
		for chunk in files:
			if '.txt' in chunk:
				chunks.append(chunk)
	chunks.sort()
	return chunks

def main():
	chunks = get_chunks()
	partitions = query(chunks)
	#unite(partitions)
	
if __name__ == "__main__":
	main()


