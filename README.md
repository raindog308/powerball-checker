This script allows you to automatically check if you've won anything in the Powerball drawing.

The results are published by the State of New York, but generally the file is not updated until the following day, so this script by default checks yesterday's date.

Powerball is drawn Monday, Wednesday, and Saturday, so I suggest this cron job:

    00 06 * * Tue,Thu,Sun /path/to/script/powerball-checker.py -m

## Configuration

Edit the file to include your numbers, and email address if you want results by email.

## Typical Usage

    powerball-checker.py -m

sends results via email

    powerball-checker.py -o

sends results to console

## Development Options ==
  
    powerball-checker.py -v

turn on debugging output

    powerball_checker.py -d MM/DD/YYYY

use MM/DD/YYYY for the date instead of yesterday's date

    powerball_checker.py -f <file>

do not fetch results but instead use <file>  

## Help (-h)

    usage: Powerball Results Checker (powerball_checker) [-h] [-d DATE] [-v] [-f FILE] [-m] [-o]

    Checks Powerball results against your chosen numbers.

    optional arguments:
      -h, --help            show this help message and exit
      -d DATE, --date DATE  use MM/DD/YYYY date
      -v, --verbose         turn on debugging
      -f FILE, --file FILE  don't fetch new results, use from file
      -m, --mail            mail to recipients
      -o, --output          print to console

  
