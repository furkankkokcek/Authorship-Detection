from string import punctuation
import re
import numpy
import math
import os

traning = [1, 6, 7, 8, 13, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 28, 29, 10, 14, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]
unknowntest=[49, 50, 51, 52, 53, 54, 55, 56, 57, 62, 63]
knowntest=[9, 11, 12, 47, 48, 58, 49, 50, 51, 52, 53, 54, 55, 56, 57, 62, 63]
path = os.getcwd()+"\\data"

c_unigram_hamilton={}
c_bigram_hamilton={}
c_trigram_hamilton={}

c_unigram_madison={}
c_bigram_madison={}
c_trigram_madison={}

total_words_madison=0
total_words_hamilton=0


def strip_punctuation(s):
    #remove all punctutations
    return ''.join(c for c in s if c not in punctuation)


def splitParagraphIntoSentences(paragraph):
    #break a paragraph into sentences and return a list

    sentenceEnders = re.compile('[.!?]')
    sentenceList = sentenceEnders.split(paragraph)
    return sentenceList


def comparotor(value,dictionary):
    for word in dictionary:
        if value < dictionary[word]:
            return word


def calculateProbablity(dictionary,sentence,size):
    sentence = sentence.split(" ")
    sentence.pop(0)
    totalprobablity=0
    for word in sentence:
        currentprobablity=math.log2(dictionary[word]/size)
        totalprobablity+=currentprobablity

    return math.pow(2,totalprobablity)


def bigramgeneratorforhamilton():
    #########Bigram Hamilton Generator#########
    generator_bigram_hamilton = {}
    firstkeys = [key for key, value in c_bigram_hamilton.items() if '<s>' in key.lower()]  # generate first word
    size = sum(value for key, value in c_bigram_hamilton.items() if '<s>' in key.lower())

    for word in firstkeys:
        generator_bigram_hamilton[word] = c_bigram_hamilton[word] / size

    count = 0
    for word in generator_bigram_hamilton:
        generator_bigram_hamilton[word] = count + generator_bigram_hamilton[word]  # interval 0,1
        count = generator_bigram_hamilton[word]

    random_float = numpy.random.uniform(0, 1)
    generatedword = comparotor(random_float, generator_bigram_hamilton)
    bigram_sentence = ""
    generatedword = generatedword.split("|")
    bigram_sentence += generatedword[0]
    generator_bigram_hamilton.clear()

    for i in range(0, 30):
        random_float = numpy.random.uniform(0, 1)
        firstkeys = [key for key, value in c_bigram_hamilton.items() if
                     '|' + generatedword[0] in key.lower() and key.endswith('|' + generatedword[0])]
        size = sum(value for key, value in c_bigram_hamilton.items() if
                   '|' + generatedword[0] in key.lower() and key.endswith('|' + generatedword[0]))
        for word in firstkeys:
            generator_bigram_hamilton[word] = c_bigram_hamilton[word] / size
        count = 0
        for word in generator_bigram_hamilton:
            generator_bigram_hamilton[word] = count + generator_bigram_hamilton[word]  # interval 0,1
            count = generator_bigram_hamilton[word]
        generatedword = comparotor(random_float, generator_bigram_hamilton)
        generatedword = generatedword.split("|")

        if generatedword[0] == "</s>":
            break
        bigram_sentence += " " + generatedword[0]
        generator_bigram_hamilton.clear()

    bigram_sentence = "<s> " + bigram_sentence
    bigram_sentence = bigram_sentence + " </s>"
    print(bigram_sentence)
    bigram_sentence = bigram_sentence.split(" ")

    bigram_probablity = 0
    for i in range(0, len(bigram_sentence) - 2):
        key = bigram_sentence[i + 1] + "|" + bigram_sentence[i]
        if key in c_bigram_hamilton:
            size = sum(c_bigram_hamilton.values())
            bigram_probablity += math.log2(c_bigram_hamilton[key] / size)
        # else:  # smoothing for end of the sentences
        #     bigram_probablity += math.log2(1 / (len(c_bigram_hamilton) + c_unigram_hamilton[bigram_sentence[i]]))
    print(math.pow(2, bigram_probablity))


def bigramgeneratorformadison():
    #########Bigram Madison Generator#########
    generator_bigram_madison = {}
    firstkeys = [key for key, value in c_bigram_madison.items() if '<s>' in key.lower()]  # generate first word
    size = sum(value for key, value in c_bigram_madison.items() if '<s>' in key.lower())

    for word in firstkeys:
        generator_bigram_madison[word] = c_bigram_madison[word] / size

    count = 0
    for word in generator_bigram_madison:
        generator_bigram_madison[word] = count + generator_bigram_madison[word]  # interval 0,1
        count = generator_bigram_madison[word]

    random_float = numpy.random.uniform(0, 1)
    generatedword = comparotor(random_float, generator_bigram_madison)
    bigram_sentence = ""
    generatedword = generatedword.split("|")
    bigram_sentence += generatedword[0]
    generator_bigram_madison.clear()

    for i in range(0, 30):
        random_float = numpy.random.uniform(0, 1)
        firstkeys = [key for key, value in c_bigram_madison.items() if
                     '|' + generatedword[0] in key.lower() and key.endswith('|' + generatedword[0])]
        size = sum(value for key, value in c_bigram_madison.items() if
                   '|' + generatedword[0] in key.lower() and key.endswith('|' + generatedword[0]))
        for word in firstkeys:
            generator_bigram_madison[word] = c_bigram_madison[word] / size
        count = 0
        for word in generator_bigram_madison:
            generator_bigram_madison[word] = count + generator_bigram_madison[word]  # interval 0,1
            count = generator_bigram_madison[word]
        generatedword = comparotor(random_float, generator_bigram_madison)
        generatedword = generatedword.split("|")

        if generatedword[0] == "</s>":
            break
        bigram_sentence += " " + generatedword[0]
        generator_bigram_madison.clear()

    bigram_sentence = "<s> " + bigram_sentence
    bigram_sentence = bigram_sentence + " </s>"
    print(bigram_sentence)
    bigram_sentence = bigram_sentence.split(" ")

    bigram_probablity = 0
    for i in range(0, len(bigram_sentence) - 2):
        key = bigram_sentence[i + 1] + "|" + bigram_sentence[i]
        if key in c_bigram_madison:
            size = sum(c_bigram_madison.values())
            bigram_probablity += math.log2(c_bigram_madison[key] / size)
        # else:  # smoothing for end of the sentences
        #     bigram_probablity += math.log2(1 / (len(c_bigram_madison) + c_unigram_madison[bigram_sentence[i]]))
    print(math.pow(2, bigram_probablity))


def trigramgeneratorforhamilton():
    generator_trigram_hamilton = {}
    firstkeys = [key for key, value in c_trigram_hamilton.items() if '<s> <s>' in key.lower()]  # generate first word
    size = sum(value for key, value in c_trigram_hamilton.items() if '<s> <s>' in key.lower())
    for word in firstkeys:
        generator_trigram_hamilton[word] = c_trigram_hamilton[word] / size

    count = 0
    for word in generator_trigram_hamilton:
        generator_trigram_hamilton[word] = count + generator_trigram_hamilton[word]  # interval 0,1
        count = generator_trigram_hamilton[word]

    # generating first word of trigram
    random_float = numpy.random.uniform(0, 1)
    generatedword = comparotor(random_float, generator_trigram_hamilton)
    trigram_sentence = ""
    generatedword = generatedword.split("|")
    trigram_sentence += generatedword[1] + " " + generatedword[0]
    generator_trigram_hamilton.clear()

    firstkeys = [key for key, value in c_trigram_hamilton.items() if
                 '|' + '<s> ' + generatedword[0] in key.lower() and key.endswith('|' + '<s> ' + generatedword[0])]
    size = sum(value for key, value in c_trigram_hamilton.items() if
               '|' + '<s> ' + generatedword[0] in key.lower() and key.endswith('|' + '<s> ' + generatedword[0]))

    for word in firstkeys:
        generator_trigram_hamilton[word] = c_trigram_hamilton[word] / size

    count = 0
    for word in generator_trigram_hamilton:
        generator_trigram_hamilton[word] = count + generator_trigram_hamilton[word]  # interval 0,1
        count = generator_trigram_hamilton[word]
    # generating second word of trigram
    random_float = numpy.random.uniform(0, 1)
    generatedword = comparotor(random_float, generator_trigram_hamilton)
    generatedword = generatedword.split("|")
    trigram_sentence += " " + generatedword[0]
    generator_trigram_hamilton.clear()
    firstword = generatedword[1].split(" ")
    firstword = firstword[1]
    secondword = generatedword[0]
    for i in range(0, 30):
        firstkeys = [key for key, value in c_trigram_hamilton.items() if
                     '|' + firstword + " " + secondword in key.lower() and key.endswith(
                         '|' + firstword + " " + secondword)]
        size = sum(value for key, value in c_trigram_hamilton.items() if
                   '|' + firstword + " " + secondword in key.lower() and key.endswith(
                       '|' + firstword + " " + secondword))
        for word in firstkeys:
            generator_trigram_hamilton[word] = c_trigram_hamilton[word] / size
        count = 0
        for word in generator_trigram_hamilton:
            generator_trigram_hamilton[word] = count + generator_trigram_hamilton[word]  # interval 0,1
            count = generator_trigram_hamilton[word]
        random_float = numpy.random.uniform(0, 1)
        generatedword = comparotor(random_float, generator_trigram_hamilton)
        generatedword = generatedword.split("|")
        trigram_sentence += " " + generatedword[0]

        secondword = generatedword[0]
        firstword = generatedword[1].split(" ")
        firstword = firstword[1]
        if secondword == "</s>":
            break
        generator_trigram_hamilton.clear()

    print(trigram_sentence)
    trigram_sentence = trigram_sentence.split(" ")

    trigram_probablity = 0
    for i in range(2, len(trigram_sentence)):
        key = trigram_sentence[i] + "|" + trigram_sentence[i - 2] + " " + trigram_sentence[i - 1]
        if key in c_trigram_hamilton:
            size = sum(c_trigram_hamilton.values())
            trigram_probablity += math.log2(c_trigram_hamilton[key] / size)

    print(math.pow(2, trigram_probablity))


def trigramgeneratorformadison():
    generator_trigram_madison = {}
    firstkeys = [key for key, value in c_trigram_madison.items() if '<s> <s>' in key.lower()]  # generate first word
    size = sum(value for key, value in c_trigram_madison.items() if '<s> <s>' in key.lower())
    for word in firstkeys:
        generator_trigram_madison[word] = c_trigram_madison[word] / size

    count = 0
    for word in generator_trigram_madison:
        generator_trigram_madison[word] = count + generator_trigram_madison[word]  # interval 0,1
        count = generator_trigram_madison[word]

    # generating first word of trigram
    random_float = numpy.random.uniform(0, 1)
    generatedword = comparotor(random_float, generator_trigram_madison)
    trigram_sentence = ""
    generatedword = generatedword.split("|")
    trigram_sentence += generatedword[1] + " " + generatedword[0]
    generator_trigram_madison.clear()

    firstkeys = [key for key, value in c_trigram_madison.items() if
                 '|' + '<s> ' + generatedword[0] in key.lower() and key.endswith('|' + '<s> ' + generatedword[0])]
    size = sum(value for key, value in c_trigram_madison.items() if
               '|' + '<s> ' + generatedword[0] in key.lower() and key.endswith('|' + '<s> ' + generatedword[0]))

    for word in firstkeys:
        generator_trigram_madison[word] = c_trigram_madison[word] / size

    count = 0
    for word in generator_trigram_madison:
        generator_trigram_madison[word] = count + generator_trigram_madison[word]  # interval 0,1
        count = generator_trigram_madison[word]
    # generating second word of trigram
    random_float = numpy.random.uniform(0, 1)
    generatedword = comparotor(random_float, generator_trigram_madison)
    generatedword = generatedword.split("|")
    trigram_sentence += " " + generatedword[0]
    generator_trigram_madison.clear()
    firstword = generatedword[1].split(" ")
    firstword = firstword[1]
    secondword = generatedword[0]
    for i in range(0, 30):
        firstkeys = [key for key, value in c_trigram_madison.items() if
                     '|' + firstword + " " + secondword in key.lower() and key.endswith(
                         '|' + firstword + " " + secondword)]
        size = sum(value for key, value in c_trigram_madison.items() if
                   '|' + firstword + " " + secondword in key.lower() and key.endswith(
                       '|' + firstword + " " + secondword))
        for word in firstkeys:
            generator_trigram_madison[word] = c_trigram_madison[word] / size
        count = 0
        for word in generator_trigram_madison:
            generator_trigram_madison[word] = count + generator_trigram_madison[word]  # interval 0,1
            count = generator_trigram_madison[word]
        random_float = numpy.random.uniform(0, 1)
        generatedword = comparotor(random_float, generator_trigram_madison)
        generatedword = generatedword.split("|")
        trigram_sentence += " " + generatedword[0]

        secondword = generatedword[0]
        firstword = generatedword[1].split(" ")
        firstword = firstword[1]
        if secondword == "</s>":
            break
        generator_trigram_madison.clear()

    print(trigram_sentence)
    trigram_sentence = trigram_sentence.split(" ")

    trigram_probablity = 0
    for i in range(2, len(trigram_sentence)):
        key = trigram_sentence[i] + "|" + trigram_sentence[i - 2] + " " + trigram_sentence[i - 1]
        if key in c_trigram_madison:
            size = sum(c_trigram_madison.values())
            trigram_probablity += math.log2(c_trigram_madison[key] / size)

    print(math.pow(2, trigram_probablity))


def loop_add(dict_data):
    for key in dict_data:
        dict_data[key]+=1


###################################################TASK-1##########################################################
for filename in traning: #reading all essays in given directory
    with open(path+"\\"+str(filename)+".txt", "r") as file:
        #print(file.name)
        firstline = file.readline()
        firstline=firstline.split(" ")
        if firstline[0] == "HAMILTON":
            all = splitParagraphIntoSentences(file.readline())
            for sentence in all:
                words=strip_punctuation(sentence)
                words=words.lower()
                words=words.strip()
                words=words.split()
                words.insert(0, "<s>")
                words.append("</s>")
                words.insert(0, "<s>")
                words.append("</s>")
                if len(words) > 4:
                    for word in words:#unigram counts
                        total_words_hamilton+=1
                        if word in c_unigram_hamilton:
                            c_unigram_hamilton[word]+=1
                        else:
                            c_unigram_hamilton[word]=1

                    for i in range(2,len(words)-1):#bigram counts
                        key=words[i]+"|"+words[i-1]
                        if key in c_bigram_hamilton:
                            c_bigram_hamilton[key]+=1
                        else:
                            c_bigram_hamilton[key]=1



                    for i in range(2,len(words)-1):#trigram count
                        key=words[i]+"|"+words[i-2]+" "+words[i-1]
                        if key in c_trigram_hamilton:
                            c_trigram_hamilton[key]+=1
                        else:
                            c_trigram_hamilton[key]=1


        elif firstline[0] == "MADISON":
            all = splitParagraphIntoSentences(file.readline())
            for sentence in all:
                words = strip_punctuation(sentence)
                words = words.lower()
                words = words.strip()
                words = words.split()
                words.insert(0, "<s>")
                words.append("</s>")
                words.insert(0, "<s>")
                words.append("</s>")
                if len(words) > 4:
                    for word in words:  # unigram counts
                        total_words_madison += 1
                        if word in c_unigram_madison:
                            c_unigram_madison[word] += 1
                        else:
                            c_unigram_madison[word] = 1

                    for i in range(2, len(words) - 1):  # bigram counts
                        key = words[i] + "|" + words[i - 1]
                        if key in c_bigram_madison:
                            c_bigram_madison[key] += 1
                        else:
                            c_bigram_madison[key] = 1

                    for i in range(2, len(words) - 1):  # trigram count
                        key = words[i] + "|" + words[i - 2] + " " + words[i - 1]
                        if key in c_trigram_madison:
                            c_trigram_madison[key] += 1
                        else:
                            c_trigram_madison[key] = 1

###################################################TASK-1##########################################################

###################################################TASK-2##########################################################

generator_unigram_hamilton=dict(c_unigram_hamilton)
generator_unigram_madison=dict(c_unigram_madison)

del generator_unigram_hamilton["<s>"]
del generator_unigram_madison["<s>"]

#########Unigram Hamilton Generator#########

size=sum(generator_unigram_hamilton.values())
for word in generator_unigram_hamilton:
    generator_unigram_hamilton[word]=generator_unigram_hamilton[word]/size#calculating probablities

count=0
for word in generator_unigram_hamilton:
    generator_unigram_hamilton[word]=count+generator_unigram_hamilton[word]#interval 0,1
    count=generator_unigram_hamilton[word]

unigram_sentence=""
for i in range(0,30):#generating hamilton's unigram sentences.
    random_float = numpy.random.uniform(0,1)
    new_word=comparotor(random_float,generator_unigram_hamilton)
    if new_word=="</s>":
        unigram_sentence=unigram_sentence+" </s>"
        break
    unigram_sentence= unigram_sentence+" "+new_word

print(unigram_sentence)
print(calculateProbablity(c_unigram_hamilton,unigram_sentence,size))

#########Unigram Madison Generator#########

size=sum(generator_unigram_madison.values())
for word in generator_unigram_madison:
    generator_unigram_madison[word]=generator_unigram_madison[word]/size#calculating probablities

count=0
for word in generator_unigram_madison:
    generator_unigram_madison[word]=count+generator_unigram_madison[word]#interval 0,1
    count=generator_unigram_madison[word]

unigram_sentence=""
for i in range(0,30):#generating madison's unigram sentences.
    random_float = numpy.random.uniform(0,1)
    new_word=comparotor(random_float,generator_unigram_madison)
    if new_word=="</s>":
        unigram_sentence=unigram_sentence+" </s>"
        break
    unigram_sentence= unigram_sentence+" "+new_word

print(unigram_sentence)
print(calculateProbablity(c_unigram_madison,unigram_sentence,size))

##############Bigram Generating###################

bigramgeneratorforhamilton()
bigramgeneratorformadison()

##############Trigram Generating##################

trigramgeneratorforhamilton()
trigramgeneratorformadison()

###################################################TASK-2##########################################################

###################################################TASK-3##########################################################
#############Authorship Detection##########################

#Copy corpus for smoothing


for filename in knowntest: #reading all test essays(9,11,12,47,48,58) in given directory for authorship detection
    with open(path+"\\"+str(filename)+".txt", "r") as file:
        smoothedbigramhamilton = dict(c_bigram_hamilton)
        smoothedbigrammadison = dict(c_bigram_madison)
        smoothedtrigramhamilton = dict(c_trigram_hamilton)
        smoothedtrigrammadison = dict(c_trigram_madison)
        print(file.name)
        firstline = file.readline()
        all = splitParagraphIntoSentences(file.readline())
        probablityhamilton = 0
        count = 0
        probablitymadison = 0
        count2 = 0
        probablitytrigramhamilton = 0
        count3 = 0
        probablitytrigrammadison = 0
        count4 = 0
        for sentence in all:
            words = strip_punctuation(sentence)
            words = words.lower()
            words = words.strip()
            words = words.split()
            words.insert(0, "<s>")
            words.append("</s>")
            words.insert(0, "<s>")
            words.append("</s>")
            if len(words) > 4:
                for i in range(2, len(words) - 1):  #BIGRAM PART OF AUTHORSHIP DETECTION
                    key = words[i] + "|" + words[i - 1]
                    if key in smoothedbigramhamilton:
                        probablityhamilton+=math.log2((smoothedbigramhamilton[key])/
                                              (sum(smoothedbigramhamilton.values())))
                        count+=1
                        #get probablity
                    else:
                        loop_add(smoothedbigramhamilton)
                        smoothedbigramhamilton[key]=1
                        probablityhamilton+=math.log2((smoothedbigramhamilton[key])/
                                              (sum(smoothedbigramhamilton.values())))
                        count+=1
                        #make add-one smoothing
                    if key in smoothedbigrammadison:
                        probablitymadison += math.log2((smoothedbigrammadison[key]) /
                                                (sum(smoothedbigrammadison.values()) ))
                        count2 += 1
                        #get probablity
                    else:
                        loop_add(smoothedbigrammadison)
                        smoothedbigrammadison[key] = 1
                        probablitymadison += math.log2((smoothedbigrammadison[key]) /
                                                (sum(smoothedbigrammadison.values()) ))
                        count2 += 1
                        #make add-one smoothing

                  # TRIGRAM PART OF AUTHORSHIP DETECTION
                    key = words[i] + "|" + words[i - 2] + " " + words[i - 1]
                    if key in smoothedtrigramhamilton:
                        probablitytrigramhamilton += math.log2((smoothedtrigramhamilton[key]) /
                                                               (sum(smoothedtrigramhamilton.values()) ))
                        count3 += 1
                        # get probablity
                    else:
                        loop_add(smoothedtrigramhamilton)
                        smoothedtrigramhamilton[key] = 1
                        probablitytrigramhamilton += math.log2((smoothedtrigramhamilton[key]) /
                                                               (sum(smoothedtrigramhamilton.values())))
                        count3 += 1
                        # make add-one smoothing
                    if key in smoothedtrigrammadison:
                        probablitytrigrammadison += math.log2((smoothedtrigrammadison[key]) /
                                                              (sum(smoothedtrigrammadison.values())))
                        count4 += 1
                        # get probablity
                    else:
                        loop_add(smoothedtrigrammadison)
                        smoothedtrigrammadison[key] = 1
                        probablitytrigrammadison += math.log2((smoothedtrigrammadison[key]) /
                                                              (sum(smoothedtrigrammadison.values())))
                        count4 += 1
                        # make add-one smoothing




        if probablityhamilton>probablitymadison:
            print("This essay belongs to HAMILTON according to bigram model")
            perplexity=(probablityhamilton / count)
            perplexity*=(-1)
            perplexity=math.pow(2, perplexity)
            print("Perplexity:", perplexity)
        else:
            print("This essay belongs to MADISON according to bigram model")
            perplexity = (probablitymadison / count2)
            perplexity *= (-1)
            perplexity = math.pow(2, perplexity)
            print("Perplexity:", perplexity)
        if probablitytrigramhamilton>probablitytrigrammadison:
            print("This essay belongs to HAMILTON according to trigram model")
            perplexity = (probablitytrigramhamilton / count3)
            perplexity *= (-1)
            perplexity = math.pow(2, perplexity)
            print("Perplexity:", perplexity)
        else:
            print("This essay belongs to MADISON according to trigram model")
            perplexity = (probablitytrigrammadison / count4)
            perplexity *= (-1)
            perplexity = math.pow(2, perplexity)
            print("Perplexity:", perplexity)



