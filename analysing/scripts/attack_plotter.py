# Input 1) attack output .txt files from given cracking tools

# Main function: to plot the percentage of cracked passwords
# in function of the number of guesses, per cracking tool

# Output: .png plot

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import os, re

markers = ['-','--','-.',':','+','x','*','.',',','v','o','^','<','>','1','2',\
    '3','4','s','p','h','H','D','d','|','_']

cur_path = os.path.dirname(__file__)
output_path = os.path.relpath('../attack_files/', cur_path)   

def grapher(full_data):    
    total_count = 60000 # number of passwords from experiment
    
    for tool, data in full_data.items():
        x_axis = []
        y_axis = []

        if tool == 'johntheripper':
            x = 1000000 # interval == 1M guesses per log line
            for guessed_passwords in data:
                y_axis.append(float(guessed_passwords * 100 / total_count))
                x_axis.append(x)
                x += 1000000
                # print(float(guessed_passwords * 100 / total_count), x)

        else:    
            y = 0
            for guesses in data:    
                y += 1
                y_axis.append(float(y * 100 / total_count))
                x_axis.append(guesses)
                # print(float(y * 100 / total_count), guesses)

        plt.plot(x_axis, y_axis, label=tool)

    # plt.title('guessing attacks')
    plt.ylabel('% of passwords cracked')
    plt.xlabel('number of guesses')
    plt.legend()

    axes = plt.axes()
    axes.set_ylim([0, 100])

    plt.grid(linewidth=1, linestyle='-', alpha=0.7, color='#EDEDED')

    # draw grid behind the lines
    ax = plt.subplot(111)
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.set_axisbelow(True)
    ax.set_xscale('log', basex=10)
    ax.set_xlim([0,10**19])
    # ax.set_yscale('log', basey=2)
    # ax.set_ylim([0,max(y_axis)*1.1])

    plt.tight_layout()

    # plt.savefig('chart.pdf', bbox_inches='tight', pad_inches=0)
    plt.savefig('chart.png', dpi=200, bbox_inches='tight', pad_inches=0)
    plt.show()



def main():
    full_data = {}

    for subdir, dirs, files in os.walk(output_path):
        for file in files:
            if file in ['neural.out', 'pcfg.out', 'markov.out', 'hashcat.out', 'johntheripper.log']:
                cracked_passwords = []

                if file == 'johntheripper.log':
                    for line in open(os.path.join(output_path, file)):
                        matches = re.findall(r'^(\d+)g', line.rstrip('\n'))
                        if not matches: continue
                        cracked_passwords.append(float(matches[0]))

                elif file == 'hashcat.out':
                    for line in open(os.path.join(output_path, file)):
                        cracked_passwords.append(float(line.rsplit(':', 1)[-1]))

                else:
                    for line in open(os.path.join(output_path, file)):
                        if not line.rstrip('\n').endswith('-5'):            # format of the PGS file is 'password\tguess_number\n'
                            cracked_passwords.append(float(line.split('\t')[1].rstrip('\n')))       # PGS rates '-5' to uncracked passwords

                cracked_passwords.sort()
                full_data[file[:-4]] = cracked_passwords    
    
    grapher(full_data)


if __name__ == "__main__":
    main()

