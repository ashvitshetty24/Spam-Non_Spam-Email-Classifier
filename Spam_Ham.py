import math


def cleantext(text):
    text = text.lower()
    text = text.strip()
    for letters in text:
        if letters in """!@#$%^&*()-_+=\|{}[]:;"'<>,./?~`""":
            text = text.replace(letters," ")
    return text


def countwords(text, is_spam, word_count):
    for each_word in text:
        if each_word in word_count:
            if is_spam == 1:
                word_count[each_word][1]=word_count[each_word][1] + 1
            else:
                word_count[each_word][0]=word_count[each_word][0] + 1
        else:
            if is_spam == 1:
                word_count[each_word] = [0,1]
            else:
                word_count[each_word] = [1,0]
    return word_count

def make_percent_list(k, theCount, spams, hams):
    for each_key in theCount:
        theCount[each_key][0] = (theCount[each_key][0] + k)/(2*k+hams)
        theCount[each_key][1] = (theCount[each_key][1] + k)/(2*k+spams)
    return theCount

def vocab_lookup(theCount, text):
    prob_sl_ham = 1
    prob_sl_spam = 1
    for key,values in theCount.items():
        if key in text:
            prob_sl_ham += math.log(values[0])
            prob_sl_spam += math.log(values[1])
        else:
            prob_sl_ham += math.log(1-values[0])
            prob_sl_spam += math.log(1-values[1])
    return math.exp(prob_sl_ham),math.exp(prob_sl_spam)


def naive_bayes_algorithm(prob_sl_ham,prob_sl_spam,prob_ham,prob_spam):
    prob_sl = (prob_sl_spam*prob_spam) / ((prob_sl_spam*prob_spam)+(prob_sl_ham*prob_ham))
    return prob_sl


if __name__ == '__main__':

    spam = 0
    ham = 0
    stop_words=set([])
    word_count = dict()
    fname1 = input("Enter the name of the spam-ham train file:" )
    fname2 = input("Enter the name of the stop-word file:" )
    fname3 = input("Enter the name of the spam-ham test file:" )
    fin_1 = open(fname1, "r")
    fin_2 = open(fname2, "r")
    textline2 = fin_2.readline()
    while textline2 !="\n":
        stop_word = textline2.strip()
        #print(stop_word)
        stop_words.add(stop_word)
        textline2=fin_2.readline()
    #print(stop_words)

    textline1 = fin_1.readline()
    while textline1 != "":
        is_spam = int(textline1[:1])
        if is_spam == 1:
            spam = spam + 1
        else:
            ham = ham + 1
        textline1 = cleantext(textline1[1:])
        words = textline1.split()
        #print("My words: ",words)
        word_set = set(words)
        word_set = word_set.difference(stop_words)
        #print("My words: ", word_set)
        word_count = countwords(word_set, is_spam, word_count)
        textline1 = fin_1.readline()
        #print(word_count)
    vocab = (make_percent_list(0.4, word_count, spam, ham))
    #print(vocab)
    #print("Total Spam",spam)
    #print("Total Non-Spam", ham)
    fin_1.close()


    prob_spam = spam/(spam+ham)
    #print(prob_spam)
    prob_ham = ham/(spam+ham)
    TP=0
    FP=0
    TN=0
    FN=0
    test_spam = 0
    test_ham = 0
    fin_3 = open(fname3, "r")
    textline3 = fin_3.readline()
    while textline3 != "":
        is_spam = int(textline3[:1])
        if is_spam == 1:
            test_spam = test_spam + 1
        else:
            test_ham = test_ham + 1
        textline3 = cleantext(textline3[1:])
        words_test = textline3.split()
        #print("My words: ",words)
        word_test_set = set(words_test)
        word_test_set = word_test_set.difference(stop_words)
        #print("My words: ", word_set)
        prob_sl_ham, prob_sl_spam = vocab_lookup(vocab, word_test_set)
        prob_sl = naive_bayes_algorithm(prob_sl_ham, prob_sl_spam, prob_ham, prob_spam)
        #print(prob_sl)
        if(prob_sl >=0.5 and is_spam == 1):
            TP = TP+1
        elif(prob_sl >=0.5 and is_spam == 0):
            FP = FP+1
        elif(prob_sl <0.5 and is_spam == 0):
            TN=TN+1
        elif (prob_sl <0.5 and is_spam == 1):
            FN=FN+1
        textline3 = fin_3.readline()
    print('Total number of Spam mails in test set:',test_spam)
    print('Total number of Ham mails in test set:',test_ham)
    print('True Positive:',TP,'True Negative:',TN)
    print('False Negative:',FN,'False Positive:',FP)
    accuracy = (TP+TN)/(TP+TN+FP+FN)
    precision = TP/(TP+FP)
    recall = TP/(TP+FN)
    F1_score = 2*(1/((1/precision) + (1/recall)))
    print('Accuracy:',accuracy,'Precision:',precision)
    print('Recall:',recall,'F1 Score:',F1_score)
    fin_2.close()
    fin_3.close()
        
