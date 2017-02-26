#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from flask import Flask, request, render_template, request, url_for, \
    redirect, flash, request, abort, jsonify
import random
import numpy as np
app = Flask(__name__)
i = 0
review = []
reviewStrings = []
word = {}
data = ''
dataString = ''
#data_set = open('data-set.txt', 'w+')
index = 0
rand = random.randint(1, 11)
position = (rand - 1) * 9
position = 0
docCount = 0
with open('foods.txt', 'r') as infile:
    for (i, myString) in enumerate(infile):
        myString = unicode(myString, errors='ignore')
        if i >= position:
            if myString and myString.strip():
                dataString = dataString + '\n' + myString
                array = myString.split(':')
                if array[0] == 'review/text' or array[0] \
                    == 'review/summary':
                    data = data + array[1]
            else:
                docCount += 1
                print docCount
                x = [x.lower().strip() for x in data.split()]
                a = set()
                for elem in x:
                    a.add(elem)
                    if elem not in word.keys():
                        temp = set()
                        temp.add(index)
                        word[elem] = temp
                    else:
                        word[elem].add(index)
                index += 1
                review.append(a)
                reviewStrings.append(dataString)

                # data_set.write(dataString)
                # data_set.write("\n")

                data = ''
                dataString = ''
            if docCount == 500:
                break
        else:
            continue
#data_set.close()


def search(token):
    try:
        token = [x.lower().strip() for x in token.split(',')]

        # print len(review)

        if len(token) != 0:
            index = 0
            search_result = []
            documents = []
            length = len(token)
            depth = [word[elem] for elem in token if elem
                     in word.keys()]
            depth = set().union(*depth)
            if len(depth) == 0:
                return ['Empty Search']

        # print depth
        # print "wewerqer" in review[1]

            result = [0] * (max(depth) + 1)
            print depth
            for x in depth:
                count = 0

            # print review[x]

                for y in token:
                    if y in review[x]:
                        count += 1
                    else:
                        pass
                result[x] = count / length

            final_result = list((np.argsort(result)[::-1])[:20])

            i = 0
            for x in final_result:
                if result[x] != 0:
                    search_result.append(str(reviewStrings[x]) + '\n'
                            + 'Score: ' + str(result[x]) + '\n')
                    i = i + 1
                else:
                    pass
            print len(search_result)
            return search_result
        else:
            print empty
            return ['Empty Search']
    except Exception, e:
        return str(e)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            search_token = request.form['search']
            search_result = search(search_token)
            print search_result

            # search_result

            return render_template('result.html', data=search_token,
                                   var=search_result)
        else:
            return render_template('index.html')
    except Exception, e:
        flash(e)


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/hello')
def hello():
    return 'Hello World!%s' % request.method


@app.route('/api', methods=['GET'])
def api():

    try:
        search_token = request.args.get('search_token')
        search_result = search(search_token)
        search_engine = {'search_token': search_token,
                         'search_result': search_result}
        return (jsonify({'search_engine': search_engine}), 200)
    except Exception, e:

        return (str(e) + 'ERROR' + str(search_result), 400)
        flash(e)

target = open('query-set.txt', 'w+')
search_url = 'http://127.0.0.1:5000/api?search_token='
i = 0
while i < 100000:
    N = random.randint(1, 11)
    x = random.sample(word.keys(), N)
    line = ','.join(x)
    line = search_url + line
    target.write(line)
    target.write('\n')
    i = i + 1
target.close()

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()

			
