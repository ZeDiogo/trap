from slack import slack
import os, sys
import json
import time

def run(me, msg, destination, as_user=True, ask_confirmation=False):
	s = slack(me, as_user=as_user, ask_confirmation=ask_confirmation)
	s.send(msg, destination)

def help():
    print('USAGE:')
    print('> python send msg destination')

def isValid(data):
    return True if time.time() - data['timestamp'] < data['timeout'] else False

def getDestination():
    try:
        with open(os.path.abspath('destination.tmp')) as f:
            data = json.load(f)
            if isValid(data):
                return data['destination']
            else:
                sys.exit('Destination has expired')
    except FileNotFoundError as fnfe:
        sys.exit('You need to provide a destination: check --help')

def saveDestination(destination):
    try:
        with open(os.path.abspath('destination.tmp'), 'w') as f:
            timestamp = time.time()
            timeout = 1 * 3600 # 1 hour
            data = {'destination' : destination, 'timestamp' : timestamp, 'timeout': timeout}
            vars = json.dump(data, f)
    except FileNotFoundError as fnfe:
        sys.exit('You need to provide a destination: check --help')

def main():
    #TODO: use argparse instead: https://docs.python.org/3/library/argparse.html
    args = sys.argv
    if len(args) == 2:
        if args[1] == '--help' or args[1] == '-h':
            help()
    if len(args) == 4:
        action = args[1]
        msg = args[2]
        destination = args[3]
        # print('{} {} to {}'.format(action, msg, destination))
        saveDestination(destination)
        run('ze', msg, destination)
    elif len(args) == 3:
        action = args[1]
        msg = args[2]
        destination = getDestination()
        run('ze', msg, destination)
    else:
        help()

if __name__=="__main__":
    main()
