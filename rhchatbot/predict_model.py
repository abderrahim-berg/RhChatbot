from keras.backend import argmax
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

nltk.download('punkt')
from tensorflow import keras 
from keras import models
from keras import layers
import numpy
import random
import json
import pickle
def respond(inp):
    with open("C:\\Users\\dell\\django_projects\\chatbot\\rhchatbot\\intents.json",encoding="utf-8") as file:
        data = json.load(file)


    try:
        with open("data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)
    except:
        words = []
        labels = []
        docs_x = []
        docs_y = []

        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

        words = [stemmer.stem(w.lower()) for w in words if w != "?"]
        words = sorted(list(set(words)))

        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            bag = []

            wrds = [stemmer.stem(w.lower()) for w in doc]

            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)


        training = numpy.array(training)
        output = numpy.array(output)

        with open("data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)

    model = models.Sequential()
    model.add(layers.Dense(32, activation='relu', input_shape=(None,len(training[0]))))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dense(len(output[0]), activation='softmax'))
    try:
        model = keras.models.load_model('my_model')
    except:
        model.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])
        model.fit(training, output, epochs=100, batch_size=8)
        model.save('my_model')

        
    def bag_of_words(s, words):
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1

        return numpy.array(bag)

    results = model.predict(numpy.expand_dims(bag_of_words(inp,words), axis=0))[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]
        
    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']
    s=random.choice(responses)
    return(s)
