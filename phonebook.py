#!/usr/bin/env python

import glob
import os
import sys
import fileinput

# Store valid commands and the number of arguments they take
VALID_COMMANDS = {'create': 1,
                  'lookup': 2,
                  'add': 3,
                  'change': 5,
                  'remove': 3,
                  'reverse-lookup': 2,
                  'view': 0,
                  'about': 0
                  }


def create(args):
    """Creates a new phonebook textfile"""
    phonebook = args[1]
    # Create empty phonebook
    with open(phonebook, 'w') as f:
        f.close()
        return ['Sucessfully created %s.\n' % phonebook]


def lookup(args):
    """Returns entries in the phonebook containing the given name"""
    name = args[1]
    phonebook = args[2]
    try:
        with open(phonebook) as f:
            intermediate_variable = [line for line in f if line.index(name) >= 0]
            f.close()
            return intermediate_variable
    except IOError:
        return ['Error: no such phonebook.']
    except ValueError:
        return ['Error: %s not found.' % name]


def add(args):
    """Adds an entry to the phonebook"""
    name = args[1]
    number = args[2]
    phonebook = args[3]
    with open(phonebook, 'a') as f:
        f.write('%s %s\n' % (name, number))
        f.close()
        return ["Successfully added %s." % name]


def change(args):
    """Changes or removes an entry in the phonebook"""
    command = args[0].lower()
    name = args[1]
    number = args[2]
    new_name = args[3]
    new_number = args[4]
    phonebook = args[5]
    game = name + ' ' + number
    new_game = new_name + ' ' + new_number
    try:
        with fileinput.FileInput(phonebook, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(game, new_game), end='')
            return ['Successfully changed %s.\n' % name]

    except OSError:
        return ['Error: no such phonebook.']
    except ValueError:
        return ['Error: %s not found.' % name]

def remove(args):
    command = args[0].lower()
    name = args[1]
    number = args[2]
    new_name = ''
    new_number = ''
    game = name + ' ' + number
    new_game = new_name + ' ' + new_number
    phonebook = args[3]
    try:
        with fileinput.FileInput(phonebook, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(game, new_game), end='')
            return ['Successfully removed %s.\n' % name]
    except OSError:
        return ['Error: no such phonebook.']
    except ValueError:
        return ['Error: %s not found.' % name]



def validate_args(args):
    """Validates the number of arguments"""
    command = args[0]
    args_length = len(args) - 1
    return VALID_COMMANDS[command] == args_length


def validate_command(command):
    """Validates the command name"""
    return command in list(VALID_COMMANDS.keys())


def view(args):
    """Adds an entry to the phonebook"""
    print("List of all available phonebooks:")
    for file in glob.glob("*.ph"):
        print(file)


def about(args):
    """Author information and sample commands"""
    print(ABOUT)


def main(args=sys.argv[1:]):
    # Command line processing
    if len(args) == 0:
        print(USAGE)
    else:
        # Command validation
        command = args[0].lower()
        valid = validate_command(command)
        if not valid:
            print(('Error: %s is not a valid command.' % command))
            return 1
        # Argument validation
        valid = validate_args(args)
        if not valid:
            print(('Error: expected %d argument(s) for the %s command'
                   % (VALID_COMMANDS[command], command)))
            return 1

        commands = {
            'create': create,
            'lookup': lookup,
            'add': add,
            'change': change,
            'remove': remove,
            'reverse-lookup': lookup,
            'view': view,
            'about': about
        }
        # Call appropriate function and print results
        try:
            for line in commands[command](args):
                print(line, end=' ')
            return 0
        except:
            pass


USAGE = """

/***
 *       ___   __                   ___              __     ___   ___
 *      / _ \ / /  ___   ___  ___  / _ ) ___  ___   / /__  <  /  / _ \
 *     / ___// _ \/ _ \ / _ \/ -_)/ _  |/ _ \/ _ \ /  '_/  / /_ / // /
 *    /_/   /_//_/\___//_//_/\__//____/ \___/\___//_/\_\  /_/(_)\___/
 *
 */

Usage:
    python phonebook.py create           phonebook.ph
    python phonebook.py lookup           name phonebook.ph
    python phonebook.py add              'full name' 'number' phonebook.ph
    python phonebook.py change           'previous name' 'previous number' 'new name' 'new number' phonebook.ph
    python phonebook.py remove           'full name' 'number' phonebook.ph
    python phonebook.py reverse-lookup   'full name' phonebook.ph
    python phonebook.py view
    python phonebook.py about

NOTE: Please add a .ph extension to the name of the phonebook. In order to distinguist it from a .txt file.
"""

ABOUT = """

/***
 *       ___   __                   ___              __     ___   ___
 *      / _ \ / /  ___   ___  ___  / _ ) ___  ___   / /__  <  /  / _ \
 *     / ___// _ \/ _ \ / _ \/ -_)/ _  |/ _ \/ _ \ /  '_/  / /_ / // /
 *    /_/   /_//_/\___//_//_/\__//____/ \___/\___//_/\_\  /_/(_)\___/
 *
 */

This is a simple commandline script to manage phonebooks.


Examples:

To create a phonebook use the following command:

	python3 phonebook.py create book-Vashisth.ph

Add entries to the created phonebook using the following:

	python3 phonebook.py add 'Careful Friend' '+1-202-555-0143' book-Vashisth.ph
	python3 phonebook.py add 'Mexican Mother' '+52(722)213-1915' book-Vashisth.ph
	python3 phonebook.py add 'Missing Sailor' '+7(901)234-56-78' book-Vashisth.ph
	python3 phonebook.py add 'Natural Banana' '+3655429698' book-Vashisth.ph
	python3 phonebook.py add 'Nuclear Potato' '+353(20)9107119' book-Vashisth.ph
	python3 phonebook.py add 'Serious Thomas' '+1-613-555-0199' book-Vashisth.ph
	python3 phonebook.py add 'Unknown Pirate' '+7(800)555-35-35' book-Vashisth.ph
	python3 phonebook.py add 'Useless George' '+44(1632)960868' book-Vashisth.ph
	python3 phonebook.py add 'Yakutov Dmitry' '+7(911)163-71-28' book-Vashisth.ph

To view all the phonebook use the following:

	python3 view

To change an entry in the phonebook use the following:
	
	python3 phonebook.py change "Natural Banana" "+3655429698" "Sorry Shaqtiman" "+666 666 666" book-Vashisth.ph

To remove an entry in the phonebook use the following:
	
	python3 phonebook.py change "Sorry Shaqtiman" "+666 666 666" book-Vashisth.ph

Author Information:

	Mrinal Vashisth, ITMO University
	mrinalmanu10@gmail.com

	This is the final exam task for Semester I of MSc Bioinformatics and Systems Biology Specialization.

	Shake it, shake it! :)

"""

if __name__ == '__main__':
    status = main()
    sys.exit(status)
