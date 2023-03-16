
from flask import Flask, jsonify, request

import sys
  
# creating a Flask app
app = Flask(__name__)
  
from utils.extractandenconding import extractFeature, matchingTemplate
from time import time
import argparse

# args
# parser.add_argument("--filename", type=str,
#                     help="Image file to verify")


def verify_helper(filename):

    print('printing', file=sys.stdout)

    parser = argparse.ArgumentParser()
    parser.add_argument("--feature_dir", type=str, default="./Feature/",
                    help="Source of the features database")
    parser.add_argument("--threshold", type=float, default=0.37,
                    help="Threshold for matching.")

                    
    args = parser.parse_args()

    # timing
    start = time()
    print('\tStart verifying {}\n'.format(filename))
    template, mask, filename = extractFeature(filename)
    result = matchingTemplate(template, mask, args.feature_dir, args.threshold)

    # results 
    if result == -1:
        print('\tNo registered sample.')
    elif result == 0:
        print('\tNo sample found.')
    else:
        print('\tsamples found (desc order of reliability):'.format(len(result)))
        for res in result:
            print("\t", res)
    # total time
    end = time()
    time_taken = ('\n\tTotal time: {} [s]\n'.format(end - start))
    print ('\n\tTotal time: {} [s]\n'.format(end - start))

    return result, time_taken

@app.route('/', methods = ['GET', 'POST'])
def home():
    # if(request.method == 'GET'):
  
    data = "hello worlds"
    return jsonify({'data': data})
  

@app.route('/verify/<filename>', methods = ['GET'])
def verifier(filename):
    if(request.method == 'GET'):
        data, time_taken = verify_helper(filename)
        # final_data = "samples found (desc order of reliability):\n\n" + data
        return jsonify({'Help': "samples found (desc order of reliability):\n\n", 'data': data, 'time taken' : time_taken})

if __name__ == '__main__':
    app.run(debug = True)