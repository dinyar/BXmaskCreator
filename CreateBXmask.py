#!/bin/python

import argparse

desc = "Script to create BX mask blocking trigger during a bunch train as well\
        as for a specified amount of bunch crossings before and after."

parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--injection_scheme', '-s', type=str, dest='scheme_file',
                    help='Path to csv file containing injection scheme.',
                    required=True)
parser.add_argument('--BXpre', '-f', type=int, default=1, dest="BXpre",
                    help='How many BX before bunch train shall be blocked.')
parser.add_argument('--BXpost', '-a', type=int, default=1, dest="BXpost",
                    help='How many BX after bunch train shall be blocked.')

opts = parser.parse_args()

data = [line.strip() for line in open(opts.scheme_file, 'r')]

print 79 * "#"
print "This is untested software, please check the bunch mask for correctness!"
print "Possible reasons for problems:"
print " - Spurious special character in whitspace"
print "   Fix: Delete all whitespace and use spaces)"
print 79 * "#"

bx_ranges = []
for line in data:
    tokenized_line = line.split(',')
    if len(tokenized_line) == 9:
        try:
            # Generate list of filled bunches
            train_length = int(tokenized_line[5].strip(), 10)
            PSbatchSpacing = int(tokenized_line[6].strip(), 10) / 25
            nPSbatches = int(tokenized_line[7].strip(), 10)
            for i in range(nPSbatches):
                bunch_train = []  # Should be 2 values (start+end)
                startRFbucket = int(
                    tokenized_line[3].strip(), 10)
                bunch_train.append(i * PSbatchSpacing + 1 + (startRFbucket - 1) / 10)
                bunch_train.append(
                    bunch_train[0] + train_length - 1)
                bx_ranges.append(bunch_train)
        except ValueError:
            continue

excluded_ranges = []
lowest_bx = 0
old_lowest = -1
for bx_range in bx_ranges:
    end_bx = bx_range[0]-opts.BXpre-1
    start_bx = bx_range[1]+opts.BXpost+1

    if (end_bx > lowest_bx) and (lowest_bx > old_lowest):
        excluded_ranges.append(str(lowest_bx) + "-" + str(end_bx))
        old_lowest = lowest_bx
    lowest_bx = start_bx

excluded_ranges.append(str(lowest_bx) + "-3563")

print "Bunch crossing mask excluding all bunch trains as well as +/-1 bunch around them:"
print " ".join(excluded_ranges)
