''' 
    Author: Lemay.ai
    License: GPLv3
'''
import pandas as pd
import numpy as np
import os
import time
import random
from sklearn.model_selection import train_test_split
import fasttext
import gensim
from gensim.test.utils import get_tmpfile
from gensim.models.word2vec import Word2Vec
import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras import backend as K
from keras.preprocessing.sequence import pad_sequences

class lemay_ai_sidecar():

    popo = 0
    verbose=1
    model_custom=False
    model_pretrained=False
    # Load the model components
    def __init__(self):
        return

    def sentVectorsCustom(self,keywordListIn):
        global model_custom
        sentenceVectorComponents = []

        pattern_vector = False
        n_words = 0
        for keyword in keywordListIn:
            #try splitting into two words
            if not keyword in model_custom:
                for splitIndex in range(len(keyword)):
                    firstWord=keyword[0:splitIndex]
                    secondWord=keyword[splitIndex:]
                    if(firstWord in model_custom):
                        vector = model_custom[firstWord]
                        sentenceVectorComponents.append(vector)
                        n_words+=1 #NOTE: this case messes with the ratio a bit. One word can be counted as 2 after it is unfused
                        break
                    if(secondWord in model_custom):
                        vector = model_custom[secondWord]
                        sentenceVectorComponents.append(vector)
                        n_words+=1 #NOTE: this case messes with the ratio a bit. One word can be counted as 2 after it is unfused
                        break

            if(keyword in model_custom):
                vector = model_custom[keyword]
                sentenceVectorComponents.append(vector)
                n_words += 1
        #print(n_words,pattern_vector)
        return sentenceVectorComponents #pattern_vector    #,n_words,

    def avgVectors(self,keywordListIn):
        global model_pretrained
        sentenceVectorComponents = []

        n_words = 0
        for keyword in keywordListIn:

            #try splitting into two words
            if not keyword in model_pretrained:
                for splitIndex in range(len(keyword)):
                    firstWord=keyword[0:splitIndex]
                    secondWord=keyword[splitIndex:]
                    #print(firstWord,secondWord)
                    if(firstWord in model_pretrained):
                        vector = model_pretrained[firstWord]
                        sentenceVectorComponents.append(vector)
                        n_words+=1 #NOTE: this case messes with the ratio a bit. One word can be counted as 2 after it is unfused
                        break
                    if(secondWord in model_pretrained):
                        vector = model_pretrained[secondWord]
                        sentenceVectorComponents.append(vector)
                        n_words+=1 #NOTE: this case messes with the ratio a bit. One word can be counted as 2 after it is unfused
                        break

            if(keyword in model_pretrained):
                vector = model_pretrained[keyword]
                sentenceVectorComponents.append(vector)
                n_words += 1

        #print(n_words,pattern_vector)
        return sentenceVectorComponents #pattern_vector    #,n_words,
    
    def embedCustom(self,row):
        global verbose
        global popo
        if verbose:
            popo += 1
            if(popo % 1000 == 0):
                print("row " + str(popo))
        return [self.sentVectorsCustom(str(row["body"]).split())]
    
    def embed(self,row):
        global verbose
        global popo
        if verbose:
            popo += 1
            if(popo % 1000 == 0):
                print("row " + str(popo))
        return [self.avgVectors(str(row["body"]).split())]
    
    def extendEmbeddingModel(self,dataset_csv,fname_pretrained, sidecar_lstm_neurons = 80,verbosity=1,
                             SAVE_PROGRESSIVE = False,custom_vecSize = 100,
                             windowSize = 2, timesteps = 100,
                            keras_iterations = 30, batch_size = 128, testSize=0.05,
                            keras_optimizer='adam',randomState=random.randint(0,100000)):
        global verbose
        global popo
        global model_custom
        global model_pretrained
        vecSize = custom_vecSize
        lstm_neurons=sidecar_lstm_neurons
        verbose=verbosity
        df_overall = pd.read_csv(dataset_csv, index_col=0)
        df_overall.head()

        tags = list(df_overall.tags.unique())
        ref = {}
        index=1
        for tag in tags:
            if str(tag) == 'nan':
                continue
            ref[tag]=index
            index+=1
        if verbose:    
            print(ref)
        
        # Plow the text from the dataset into a text file, and the train a custom model on that text
        sentences = np.array(df_overall["body"]).tolist()

        for i in range(len(sentences)):
            sentences[i] = str(sentences[i])
        training_string = '\n'.join(sentences)

        with open("training_file.txt", "w") as text_file:
            text_file.write(training_string)
        if verbose:
            print("Training Custom Model..")

        model_custom = fasttext.train_unsupervised('training_file.txt', model='skipgram', dim=vecSize, ws=windowSize, epoch=5)

        fname_custom = get_tmpfile("model_custom.model")
        model_custom.save_model(fname_custom)
        model_custom = fasttext.load_model(fname_custom)
        if verbose:
            print("Done..")
            print("Starting Custom Vectors Generation")
        popo = 0
        df_overall['vector_custom'] = df_overall.apply(self.embedCustom, axis=1)
        del model_custom
        if verbose:
            print("Custom Vectors Generated.")
        if verbose:    
            print("Loading Pretrained Model..")
        model_pretrained = gensim.models.KeyedVectors.load_word2vec_format(fname_pretrained, binary=False) #false for fasttext & true for googleNews
        if verbose:
            print("Pretrained Model Loaded.")
            print("Starting Pretrained Vectors Generation")
        popo = 0
        df_overall['vector'] = df_overall.apply(self.embed, axis=1)
        del model_pretrained
        if verbose:
            print("Pretrained Vectors Generated")
            print("Pickling Dataframe")
        df_overall.to_pickle('df_overall_fastText_vectors.p')
        if verbose:
            print("Pickling Dataframe Complete")
            print("Concatenating pretrained vectors with custom vectors for generation of combined model")
        Y = pd.get_dummies(df_overall['tags']).fillna(0)
        Y = np.array(Y)
        X = df_overall[["vector"]].fillna(0)
        rows=X.shape[0]
        X=np.array(X)
        pretrainedModelDimms = np.array(X[0][0]).shape[2]
        newarr=np.empty([rows,timesteps,pretrainedModelDimms])
        for i in range(rows):
            if(i%1000 == 0):
                print("row " + str(i))
            if len(X[i][0][0])==0:
                xs=np.zeros([1,timesteps,pretrainedModelDimms])
            else:
                xd=np.stack(X[i][0][0], axis=0)
                xd=xd.swapaxes(0,1)
                xs=pad_sequences(xd, maxlen=timesteps, dtype='float32')
                xs=np.swapaxes(xs,0,1)
            newarr[i]=xs
        X=newarr
        
        #CUSTOM WORD EMBEDDING X AND Y CREATION
        X2 = df_overall[["vector_custom"]].fillna(0)
        rows=X2.shape[0]
        X2=np.array(X2)

        newarr=np.empty([rows,timesteps,vecSize])
        for i in range(rows):
            if len(X2[i][0][0])==0:
                xs=np.zeros([1,timesteps,vecSize])
            else:
                xd=np.stack(X2[i][0][0], axis=0)
                xd=np.swapaxes(xd,0,1)
                xs=pad_sequences(xd, maxlen=vecSize, dtype='float32')
                xs=np.swapaxes(xs,0,1)
            newarr[i]=xs

        X2=newarr
        X=np.swapaxes(X,1,2)
        X2=np.swapaxes(X2,1,2)
        X = np.hstack((X,X2))
        X=np.swapaxes(X,1,2)
        
        if verbose:
            print("X.shape,Y.shape\n",X.shape,Y.shape)
        x_train, x_test, y_train, y_test=train_test_split(X, Y, test_size=testSize, random_state=randomState)
        if verbose:
            print("x_train.shape, x_test.shape, y_train.shape, y_test.shape\n",x_train.shape, x_test.shape, y_train.shape, y_test.shape)
        data_dim = pretrainedModelDimms + vecSize
        num_classes = len(ref.keys())
        
        if verbose:
            print("TRAINING NEURAL NETWORK ON COMBINED DATA")
            print(str(lstm_neurons) + " LSTM neurons ")
        
        K.clear_session()

        model = Sequential()
        model.add(LSTM(lstm_neurons, return_sequences=True,
                       input_shape=(timesteps, data_dim)))  # returns a sequence of vectors of dimension 32
        model.add(LSTM(lstm_neurons, return_sequences=True))  # returns a sequence of vectors of dimension 32
        model.add(LSTM(lstm_neurons))  # return a single vector of dimension 32
        model.add(Dense(num_classes, activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer=keras_optimizer, metrics=['accuracy'])
        import time
        for i in range(keras_iterations):
            if verbose:
                print('Iteration: '+str(i))
            model.fit(x_train, y_train, epochs=1,  batch_size=batch_size, verbose=verbose)#, class_weight="auto"
            score = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=verbose)
            if verbose:
                print("SCORE: {0:.3f}".format(score[1]))
            if i == 20 and SAVE_PROGRESSIVE:
                model.save('model_' + str(lstm_neurons) + '_20_iter.h5')

        fname_sidecar='model_' + str(lstm_neurons) + '.h5'
        model.save(fname_sidecar)
        if verbose:
            print("Ok.")
        return model,fname_sidecar,fname_custom
