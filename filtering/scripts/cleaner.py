
# Input: 1) it requires the presence of the processed pickeled file in the following directory: /files/processed/
# and 2) requires the existence of the following directory: /files/cleaned/

# Main function: to clean, that is, filter the processed .txt files into new .txt files with a predefined format

# Output: .txt files with the following format: "password\n",
# pickle file containing all cleaned datasets in the form of a pickled object
# and it also prints in the terminal the following meta-information: number of passwords
# in each password dataset after cleaning, according to relaxed/CCS18 conditions applied


import os, re, html, pickle


cur_path = os.path.dirname(__file__)
read_path = os.path.relpath('../files/processed/', cur_path)
write_path = os.path.relpath('../files/cleaned/', cur_path)


# creates a new pickle file with all 3 cleaned datasets in the form of a pickled object
def save_data(cleaned_pickle):
	filename = 'cleaned.pickle'
	print('\n\t> Writing to the following new pickled file:', filename)

	pickled_file = open(os.path.join(write_path, filename), 'wb')
	pickle.dump(cleaned_pickle, pickled_file)

	print('\t> The following file was created:', filename)

# writes two new .txt files: one filtered with relaxed conditions and another with CCS18 conditions
def clean(file, passwords):
	print('\n\t> Cleaning the following dataset file:', file)
	frequent_file = file.split('.')[0][:-2] + 'FreqV2.txt'
	infrequent_file = file.replace('1', '2')

	total_count, total_removed = 0, 0
	total_CC18_count, total_nonCC18_count = 0, 0 

	# output data structure that will contain the 3 cleaned datasets, with their respective passwords, to be pickeled at the end
	cleaned_passwords_freq, cleaned_passwords = [], []
	
	# sets the minimum policy length according to all datasets (RockYou is 5, LinkedIn and 000WebHost is 6)
	minimum_policy_length = 5 if 'RockYou' in file else 6

	# HTML list containing the most commonly used tag elements and the http:// prefix
	HTML_tags = ['<html', '<title', '<head', '<body', '<link', '<form', '<a href', '<img', '<div', '<table', '<object', '<!DOCTYPE', '<embed', '<script', '<style', 'http://']

	with open(os.path.join(write_path, frequent_file), 'w') as output_file_1:
		with open(os.path.join(write_path, infrequent_file), 'w') as output_file_2:
			for password, count in passwords.items():
				total_count += count

				# boolean values indicating wheter the relaxed (infrequent passwords included) and the CCS18 conditions are met
				relaxed_conditions = (minimum_policy_length <= len(password) <= 64 and all(31 < ord(char) < 128 for char in html.unescape(password)))
				CCS18_conditions = (minimum_policy_length <= len(password) <= 64 and all(31 < ord(char) < 128 for char in html.unescape(password)) and int(count) >= 10)

				# boolean value indicating whether the password has HTML code in it or not > found exclusively on the RockYou dataset
				invalid_HTML = any(tag for tag in HTML_tags if bool(re.search(tag, password)))

				# boolean value indicating whether that password is encoded or not > found exclusively on the LinkedIn dataset
				invalid_encodings = ('$HEX[' in password or (len(password) == 15 and password.isdigit()))

				if 'LinkedIn' in file:
					if CCS18_conditions and not invalid_HTML and not invalid_encodings:
						total_CC18_count += count
						cleaned_passwords_freq.append(password)
						output_file_1.write(password + '\n')

					if relaxed_conditions and not invalid_HTML and not invalid_encodings:
						total_nonCC18_count += count
						cleaned_passwords.append(password)
						output_file_2.write(password + '\n')
					else:
						total_removed += count
				
				else:
					if CCS18_conditions and not invalid_HTML:
						total_CC18_count += count
						cleaned_passwords_freq.append(password)
						output_file_1.write(password + '\n')	

					if relaxed_conditions and not invalid_HTML:
						total_nonCC18_count += count
						cleaned_passwords.append(password)
						output_file_2.write(password + '\n')
					else:
						total_removed += count


			print("total count and removed:", file, total_count, total_removed)
			print("total unrelaxed and relaxed", total_CC18_count, total_nonCC18_count)
			print("total unrelaxed and relaxed, but unique entries:", len(cleaned_passwords_freq), len(cleaned_passwords))

		output_file_2.close()
	output_file_1.close()

	cleaned_dataset = {frequent_file : cleaned_passwords_freq, infrequent_file : cleaned_passwords}
	return cleaned_dataset
		
def main():
	# output data structure that will contain the 3 cleaned datasets, with their respective passwords, to be pickeled at the end
	cleaned_pickle = []

	# loading the pickled file containing the processed datasets
	input_file = open(os.path.join(read_path, 'processed.pickle'),'rb')
	datasets = pickle.load(input_file)
	
	for dataset in datasets:
		for file, passwords in dataset.items():
			cleaned_dataset = clean(file, passwords)
			
			# add the new cleaned dataset to the output data structure
			cleaned_pickle.append(cleaned_dataset)

	save_data(cleaned_pickle)

	# pickled object has the following format:

	'''
	[	{'RockYouFreqV2' : 		[password1, password2, ...], 	'RockYouV2' : 		[password1, password2, ...]		}, 
		{'LinkedinFreqV2' : 	[password1, password2, ...], 	'LinkedInV2' : 		[password1, password2, ...]		},
		{'000WebHostFreqV2' : 	[password1, password2, ...], 	'000WebHostV2' : 	[password1, password2, ...]		}	]
	'''

	# compute pre-stats (before/after cleaning the datasets?)...

if __name__ == "__main__":
	main()


