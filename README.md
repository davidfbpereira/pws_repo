# pws_repo

Passwords remain the primary authentication method in today’s digital world. Password strength meters (PSMs) are a popular password security mechanism that helps users choose stronger passwords. However, building an accurate PSM is one of the main challenges towards guiding users into better password selection.

We share our study about password guessing resistance against off-the-shelf guessing attacks as an accuracy measure of PSMs. We compare how PSMs rate passwords and analyze the relation between the classifications produced by PSMs and the passwords guessing resistance to guessing attacks performed using different attack tools.

This repository has the necessary code to: 
1) filter and randomly sample passwords;
2) perform advanced heuristic password guessing attacks;
3) query and evaluate PSM's accuracy.

The repository has the following directory structure: 
```sh
.
├── README.md
├── analysing
│   ├── attack_files
│   │   ├── hashcat.out
│   │   ├── johntheripper.out
│   │   ├── markov.out
│   │   ├── neural.out
│   │   └── pcfg.out
│   ├── pickle_files
│   │   ├── hashcat.pickle
│   │   ├── johntheripper.pickle
│   │   ├── markov.pickle
│   │   ├── neural.pickle
│   │   └── pcfg.pickle
│   ├── scripts
│   │   ├── attack_plotter.py
│   │   ├── chart.png
│   │   ├── sample.hash
│   │   ├── seeker.py
│   │   └── stats.py
│   └── stats_files
│       ├── post.stats
│       └── pre.stats
├── attacking
│   ├── hashcat
│   │   ├── attack.sh
│   │   └── custom.rule
│   └── johntheripper
│       ├── attack.sh
│       ├── external.conf
│       └── john.conf
├── filtering
│   ├── files
│   │   ├── cleaned
│   │   ├── originals
│   │   └── processed
│   └── scripts
│       ├── RockYou_to_CSV.py
│       ├── cleaner.py
│       └── pre_processor.py
├── querying
│   ├── results
│   │   ├── haveibeenpwned_000WebHost.txt
│   │   ├── haveibeenpwned_000WebHostFreq.txt
│   │   ├── haveibeenpwned_LinkedIn.txt
│   │   ├── haveibeenpwned_LinkedInFreq.txt
│   │   ├── haveibeenpwned_RockYou.txt
│   │   ├── haveibeenpwned_RockYouFreq.txt
│   │   ├── query_results.pickle
│   │   ├── zxcvbn_000WebHost.txt
│   │   ├── zxcvbn_000WebHostFreq.txt
│   │   ├── zxcvbn_LinkedIn.txt
│   │   ├── zxcvbn_LinkedInFreq.txt
│   │   ├── zxcvbn_RockYou.txt
│   │   └── zxcvbn_RockYouFreq.txt
│   └── scripts
│       ├── assembler.py
│       ├── meters.py
│       └── querier.py
└── sampling
    ├── samples
    │   ├── 000WebHostFreq_Sample_10000.txt
    │   ├── 000WebHost_Sample_10000.txt
    │   ├── LinkedInFreq_Sample_10000.txt
    │   ├── LinkedIn_Sample_10000.txt
    │   ├── RockYouFreq_Sample_10000.txt
    │   └── RockYou_Sample_10000.txt
    └── scripts
        └── meter_sampler.py
```

### Step 0: Instalation
Source code can be downloaded via git:
```sh
$ git clone https://github.com/davidfbpereira/pws_repo.git
```
All Python code snippets were tested using 3.8.1 version.
Assuming pip and wget tools are pre-installed, Selenium Framework and WebDriver (required for the querying stage) can be installed with the following commands:
```sh
$ pip install selenium
```
To allow Selenium to communicate and automate the browser, we need to install a web browser's driver. The WebDriver for Google Chrome can be found [here]. 
Download and install the driver with the following commands:
```sh
$ wget https://chromedriver.storage.googleapis.com/<release>/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip
$ chmod +x chromedriver
$ sudo mv chromedriver /usr/local/bin/
```
Finally, the [JohnTheRipper] and [Hashcat] binaries are needed in order to perform the local heuristic password guessing attacks. 
### Step 1: Filtering
The filtering step is responsible for:
  - Converting RockYou.txt file to a .csv normalized file;
  - Pre-processing each dataset file;
  - Cleaning each dataset file into "relaxed" and "unrelaxed" datasets.

The `/files/` sub-directories are empty. RockYou, LinkedIn and 000WebHost dataset files should be place in `/files/originals` in order to proceed to the next stage.

### Step 2: Sampling
Next, we randomly sample 10.000 passwords from each dataset file in a total of 60.000 passwords.

### Step 3: Querying
Each meter is then queried according to each dataset sample, thus producing various classification results which are then assembled into a single .pickle file for later use.

### Step 4: Attacking
The whole sample is attacked: 1) locally, using the JohnTheRipper and Hashcat password guessing tools and 2) remotelly, using the [PGS] service by CMU. Only the configuration and rule files are shared. Wordlits can be found in this [repo].

### Step 5: Analysis
Finally, the last analysis step is responsible for:
  - Plotting the attacking graph;
  - Assembling the classification and cracking results;  
  - Calculating the password classification distributions before and after the guessing attacks.



[here]: <http://chromedriver.chromium.org/downloads>
[JohnTheRipper]: <https://www.openwall.com/john/>
[Hashcat]: <https://hashcat.net/hashcat/>
[PGS]: <https://pgs.ece.cmu.edu/>
[repo]: <https://github.com/berzerk0/Probable-Wordlists/tree/master/Real-Passwords>
