
from flask import Flask, jsonify, request

import sys
import os
import base64 
import io

app = Flask(__name__)
  
from utils.extractandenconding import extractFeature, matchingTemplate
from time import time
import argparse

def verify_helper(filename):

    print('printing', file=sys.stdout)

    parser = argparse.ArgumentParser()
    parser.add_argument("--feature_dir", type=str, default="./Feature/",
                    help="Source of the features database")
    parser.add_argument("--threshold", type=float, default=0.37,
                    help="Threshold for matching.")

                    
    args = parser.parse_args()

    start = time()
    print('\tStart verifying {}\n'.format(filename))
    template, mask, filename = extractFeature(filename)
    result = matchingTemplate(template, mask, args.feature_dir, args.threshold)

    if result == -1:
        print('\tNo registered sample.')
    elif result == 0:
        print('\tNo sample found.')
    else:
        print('\tsamples found (desc order of reliability):'.format(len(result)))
        for res in result:
            print("\t", res)

    end = time()
    time_taken = ('\n\tTotal time: {} [s]\n'.format(end - start))
    print ('\n\tTotal time: {} [s]\n'.format(end - start))

    return result, time_taken

@app.route('/', methods = ['GET', 'POST'])
def home():
    data = "hello worlds"
    return jsonify({'data': data})


@app.route('/accuracy', methods = ['GET'])
def get_accuracy():
    return jsonify({'Train Accuracy score': str(train_acc), 'Test Accuracy score': str(test_acc)})

@app.route('/verify/<filename>', methods = ['GET'])
def verifier(filename):
    if(request.method == 'GET'):
        data, time_taken = verify_helper(filename)
        return jsonify({'Help': "samples found (desc order of reliability):\n\n", 'data': data, 'time taken' : time_taken})

@app.route('/save/image', methods = ['POST'])
def save_img():
    filename = request.json["filename"]
    photo = request.json["image"]

    photo1 = photo.replace(" ", "")
    f = (base64.b64decode(photo1))
    a = io.BytesIO()
    with open(filename + ".jpg", "wb") as file:
        file.write(f)

    return jsonify({"Ticket": "20.00"})

@app.route('/register', methods = ['POST'])
def register():
    photo1 = request.json["image1"]
    photo2 = request.json["image2"]
    username = request.json["username"]

    photo1 = photo1.replace(" ", "")
    photo2 = photo2.replace(" ", "")
    f1 = (base64.b64decode(photo1))
    a1 = io.BytesIO()

    f2 = (base64.b64decode(photo2))
    a2 = io.BytesIO()

    newpath = "Dataset/" + username

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    
    filename1 = username + "_1_1"
    filename2 = username + "_1_2";

    
    with open(newpath + "/" + filename1 + ".jpg", "wb") as file:
        file.write(f1)
    with open(newpath + "/" + filename2 + ".jpg", "wb") as file:
        file.write(f2)

    return jsonify({"server message": "Registration successful"})

if __name__ == '__main__':
    app.run(debug = True)