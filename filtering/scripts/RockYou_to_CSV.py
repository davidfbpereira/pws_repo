
# Input: inputs given, but 1) it requires the existence of the
# RockYou.txt original file in the following directory: /files/originals/ 

# Main function: to convert the original RockYou .txt file into a .csv file with a predefined format

# Output: RockYou.csv file with the following format: "password, count\n"
# stored in the following directory: /files/originals


import os, csv


cur_path = os.path.dirname(__file__)
read_path = os.path.relpath('../files/originals/', cur_path)


# writes the new .csv file stored at /files/originals, with the following predefined format: "password, count\n"
def convert_to_csv(original_file):
	new_file_name = original_file.split('.')[0] + '.csv'
	
	with open(os.path.join(read_path, new_file_name), 'w') as output_file:
		writer = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(['password', 'frequency'])					# header text to match the other 2 dataset files...
		with open(os.path.join(read_path, original_file), 'r') as input_file:
			for line in input_file:
				count, password = int(line[:7]), line[8:].rstrip('\n') 		# example of line entry format in the original file: "  13456 qwerty\n"
				writer.writerow([password, count]) 							# chosen format: "password, count\n"
		input_file.close()
	output_file.close()

def main():
	# source file: https://wiki.skullsecurity.org/Passwords
	convert_to_csv('RockYou.txt')		# input .txt file to be converted to .csv file
	
if __name__ == "__main__":
	main()


