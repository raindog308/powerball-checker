#!/usr/bin/python3 

recipients = [ 'someone@example.com', 'someoneelse@example.com' ]
email_from = 'root@your-host.example.com'

my_nums = ( '1', '2', '3', '4', '5' )
my_pb_num = '6'

results_url = 'https://data.ny.gov/api/views/d6yy-54nr/rows.csv?accessType=DOWNLOAD&sorting=true'
results_file = '/tmp/powerball_results.csv'

# ------------------------------------------

import argparse
from datetime import date
from datetime import timedelta
import urllib.request
import smtplib
from email.mime.text import MIMEText

def debug (message):
    if ( args.verbose ):
        print (message)

parser = argparse.ArgumentParser(
    prog='Powerball Results Checker (powerball_checker)',
    description='Checks Powerball results against your chosen numbers.'
)

parser.add_argument('-d', '--date', help='use MM/DD/YYYY date')
parser.add_argument('-v', '--verbose', help='turn on debugging', action='store_true')
parser.add_argument('-f', '--file', help="don't fetch new results, use from file")
parser.add_argument('-m', '--mail', help="mail to recipients", action='store_true')
parser.add_argument('-o', '--output', help="print to console", action='store_true')

args = parser.parse_args()

# which results date to use?

if ( args.date != None ):
    results_date = args.date
else:
    today = date.today()
    yesterday = today - timedelta(days = 1)
    parts = str(yesterday).split('-')
    results_date = parts[1] + "/" + parts[2] + "/" + parts[0]
debug ("Results date is %s" % ( results_date ))

# get results (file or URL)

all_results = []

if args.file is not None:
    results_file = args.file
else:
    urllib.request.urlretrieve(results_url, results_file)

f = open ( results_file, "r" )
all_results = f.readlines()
f.close()
debug ("Have %d results from file %s" % ( len(all_results), results_file ))

# Draw Date,Winning Numbers,Multiplier
# 07/31/2023,02 11 48 58 65 13,2
winning_numbers = None
for result in all_results:
    parts = result.split (',')
    if parts[0] == results_date:
        winning_numbers_string = parts[1]

if ( winning_numbers_string is None ):
    raise Exception('No results for date %s' % ( results_date ))

winning_nums = winning_numbers_string.split(' ')
winning_pb = winning_nums.pop()
debug ( "Winning numbers: " + ' '.join(winning_nums) + ' Powerball: ' + winning_pb )

# analyze matches

# we compare int-to-int
winning_num_ints = []
for winning_num in winning_nums:
    winning_num_ints.append(int(winning_num))

num_winning = 0
for my_num in my_nums:
    if int(my_num) in winning_num_ints:
        num_winning += 1

debug("num winning: %d" % ( num_winning ))

pb_won = 0
if int(my_pb_num) == int(winning_pb):
    pb_won = 1
    debug('powerball matched')
else:
    debug('powerball did not match')

prize = 'Sorry, no prize.'
if ( pb_won == 1 ):
    prize = 'Won $4'
    debug ('prize match: pb_won == 1')

if ( pb_won == 1 and num_winning == 1):
    prize = 'Won $4'
    debug ('prize match: pb_won == 1 and num_winning == 1')

if ( pb_won == 1 and num_winning == 2):
    prize = 'Won $7'
    debug ('prize match: pb_won == 1 and num_winning == 2')

if ( num_winning == 3):
    if ( pb_won == 1 ):
        prize = 'Won $100'
        debug ('prize match: pb_won == 1 and num_winning == 3')
    else:
        prize = 'Won $7'
        debug ('prize match: pb_won == 0 and num_winning == 3')

if ( num_winning == 4):
    if ( pb_won == 1 ):
        prize = 'Won $50,000'
        debug ('prize match: pb_won == 1 and num_winning == 4')
    else:
        prize = 'Won $100'
        debug ('prize match: pb_won == 0 and num_winning == 4')

if ( num_winning == 5):
    if ( pb_won == 1 ):
        prize = 'Hit the JACKPOT!'
        debug ('prize match: pb_won == 1 and num_winning == 5')
    else:
        prize = 'Won $1,000,000'
        debug ('prize match: pb_won == 0 and num_winning == 5')

debug("Prize: %s" % ( prize ))

message = prize
message += "\n"
message += "My numbers: " + " ".join(my_nums) + " Powerball: " + my_pb_num + "\n"
message += "Winning numbers: " + ' '.join(winning_nums) + ' Powerball: ' + str(winning_pb)

if ( args.output):
    print(message)

for recipient in recipients:
    msg = MIMEText(message)
    msg['Subject'] = "Powerball Results for %s: %s" % ( results_date, prize )
    msg['To'] = recipient
    msg['From'] = email_from

    s = smtplib.SMTP('localhost')
    s.sendmail(email_from, [recipient], msg.as_string())
    s.quit()
