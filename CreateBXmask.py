#!/bin/python

import argparse

desc = "Script to create BX mask blocking trigger during a bunch train as well as for a specified amount of bunch crossings before and after."

parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--injection_scheme', '-s', type=str, dest='scheme_file', help='Path to csv file containing injection scheme.', required=True)
parser.add_argument('--BXpre', '-f', type=int, default=1, dest="BXpre", help='How many BX before bunch train shall be blocked.')
parser.add_argument('--BXpost', '-a', type=int, default=1, dest="BXpost", help='How many BX after bunch train shall be blocked.')

opts = parser.parse_args()

data = [line.strip() for line in open(opts.scheme_file, 'r')]

print 79*"#"
print "This is untested software, please check the bunch mask for correctness!"
print "Possible reasons for problems:"
print " - Spurious special character in whitspace"
print "   Fix: Delete all whitespace and use spaces)"
print 79*"#"

bx_ranges = []
lowest_bx = 0
for line in data:
    tokenized_line = line.split(',')
    if len(tokenized_line) == 9:
        try:
            start_bx = 1+(int(tokenized_line[3].strip(), 10)-1)/10
            end_bx = start_bx+int(tokenized_line[5].strip(), 10)
	    if start_bx-1 > lowest_bx:
                # Adding 1 to lower edge as we're blocking bunch train+1
                # Subtracting 2 to upper edge for similar reason
                bx_ranges.append(str(lowest_bx+opts.BXpost) + "-" + str(start_bx-1-opts.BXpre))
            if end_bx > lowest_bx:
                lowest_bx = end_bx
        except ValueError:
            continue

bx_ranges.append(str(lowest_bx) + "-" + "2563")

print "Bunch crossing mask excluding all bunch trains as well as +/-1 bunch around them:"
print " ".join(bx_ranges)

