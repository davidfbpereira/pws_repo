
# meter crawling code interactions with selenium framework
# meters should be added here and called in querier.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

import time, os, hashlib, requests


cur_path = os.path.dirname(__file__)
read_path = os.path.relpath('../../sampling/samples', cur_path)
write_path = os.path.relpath('../results', cur_path)


# most common user agents: https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
defaultUseragent = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'


def zxcvbn(chunk_filename, int):
	print(chunk_filename, int, os.getpid())

	options = webdriver.ChromeOptions() 	
	options.add_argument('--incognito')
	options.add_argument('user-agent=' + defaultUseragent)
	options.add_experimental_option("detach", True) 	# for chromedriver to stay open afterward
	options.add_argument('headless')	 # to operate in the background without any pop-up window

	driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) 		# to create the instance of Chrome WebDriverload with loaded options
	# driver.fullscreen_window()

	driver.get("https://lowe.github.io/tryzxcvbn/") 	# navigate to page
	time.sleep(30)
	
	try:
		password_input_field = driver.find_element_by_id('search-bar') 		# get input location within HTML page
	except NoSuchElementException:
		print("Error: Element with id='search-bar' was not found." + '\n')

	new_file = 'zxcvbn_' + chunk_filename.split('_')[0] + '.txt'
	new_directory = os.path.join(write_path)

	output_file = open(os.path.join(new_directory, new_file), 'w')		# output auxiliary file with the PSM evaluation results
	
	with open(os.path.join(read_path, chunk_filename)) as chunk:
		for line in chunk:
			line = line.rstrip('\r\n') 			

			password_input_field.send_keys(line) 		# send new password to input field
			time.sleep(1) 		# wait some time (in seconds) until password as been fully evaluated

			try:
				guesses_log10 = driver.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[2]/td[2]')		 # search for the result within the page
			except NoSuchElementException:
				print("Error: Element with xpath = '/html/body/div[1]/table/tbody/tr[2]/td[2]' was not found.")
			
			try:
				score = driver.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[3]/td[2]')		 # search for the result within the page
			except NoSuchElementException:
				print("Error: Element with xpath = '/html/body/div[1]/table/tbody/tr[3]/td[2]' was not found.")

			dataRow = '{0:<10} {1:<18} {2}\n'.format(guesses_log10.text, score.text, line) 			# output to text file: <guesses_log10 \t score \t password>
			print(dataRow[:-1])
 		 
			output_file.write(dataRow)

			password_input_field.clear() # reset input field

			output_file.flush()

	output_file.close()
	driver.quit()

	return new_file

def lookup_pwned_api(pwd):
    """Returns hash and number of times password was seen in pwned database.

    Args:
        pwd: password to check

    Returns:
        A (sha1, count) tuple where sha1 is SHA1 hash of pwd and count is number
        of times the password was seen in the pwned database.  count equal zero
        indicates that password has not been found.

    Raises:
        RuntimeError: if there was an error trying to fetch data from pwned
            database.
    """
    sha1pwd = hashlib.sha1(pwd.encode('ascii')).hexdigest().upper()
    head, tail = sha1pwd[:5], sha1pwd[5:]
    url = 'https://api.pwnedpasswords.com/range/' + head
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError('Error fetching "{}": {}'.format(
            url, res.status_code))
    hashes = (line.split(':') for line in res.text.splitlines())
    count = next((int(count) for t, count in hashes if t == tail), 0)
    return sha1pwd, count

def haveibeenpwned(chunk_filename, int):
	print(chunk_filename, int, os.getpid())

	new_file = 'haveibeenpwned_' + chunk_filename.split('_')[0] + '.txt'
	new_directory = os.path.join(write_path)

	output_file = open(os.path.join(new_directory, new_file), 'w')		# output auxiliary file with the PSM evaluation results
	
	with open(os.path.join(read_path, chunk_filename)) as chunk:
		for line in chunk:
			pwd = line.rstrip('\r\n') 			
			sha1pwd, count = lookup_pwned_api(pwd)
			if count:
				dataRow = '{0:<29} {1}\n'.format(count, pwd)
			else:
				dataRow = '{0:<29} {1}\n'.format('not found', pwd)
			print(dataRow[:-1])
			output_file.write(dataRow)  

	return new_file


