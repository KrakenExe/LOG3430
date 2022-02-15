from email_analyzer import EmailAnalyzer
from vocabulary_creator import VocabularyCreator
from renege import RENEGE



def spam_classification_1(is_spam,time_between_first_and_last,user_trust,group_trust):
    P = is_spam
    H = True if time_between_first_and_last<20 else False
    U = True if user_trust<50 else False
    G = True if group_trust>=50 else False

    S = P and ((H and U) or (U and not G))
    return S

def spam_classification_2(is_spam,time_between_first_and_last,user_trust,group_trust):
    P = is_spam
    H = True if time_between_first_and_last<20 else False
    U = True if user_trust<50 else False
    G = True if group_trust>=50 else False

    S = P and H and U or P and U and not G
    return S

def CACC():
    N_MINOR_CLAUSE_COMBINATIONS = 8
    N_CLAUSES = 4
    CACC_test_set = []
    # valeurs qui mettent la variable associée à vrai / faux dans les fonctions spam_classification
    H_TRUE_VALUE = 15
    H_FALSE_VALUE = 25
    U_TRUE_VALUE = 25
    U_FALSE_VALUE = 75
    G_TRUE_VALUE = 75
    G_FALSE_VALUE = 25
    P_VALUES = [False,True]
    H_VALUES = [25,15]
    U_VALUES = [75,25]
    G_VALUES = [25,75]

    for i in range(N_CLAUSES):

        for j in range(N_MINOR_CLAUSE_COMBINATIONS):
            entry_as_binary = int(bin(j),2)
            minor_clause_1 = (entry_as_binary >> 2) & 1
            minor_clause_2 = (entry_as_binary >> 1) & 1
            minor_clause_3 = (entry_as_binary >> 0) & 1
            # si P est la clause majeure
            if i==0:
                major_clause_true = spam_classification_1(P_VALUES[1],H_VALUES[minor_clause_1],U_VALUES[minor_clause_2],G_VALUES[minor_clause_3])
                major_clause_false = spam_classification_1(P_VALUES[0],H_VALUES[minor_clause_1],U_VALUES[minor_clause_2],G_VALUES[minor_clause_3])
                if major_clause_true != major_clause_false:
                    CACC_test_set.append([P_VALUES[1],H_VALUES[minor_clause_1],U_VALUES[minor_clause_2],G_VALUES[minor_clause_3]])
                    CACC_test_set.append([P_VALUES[0],H_VALUES[minor_clause_1],U_VALUES[minor_clause_2],G_VALUES[minor_clause_3]])
                    break
            # si H est la clause majeure
            elif i==1:
                major_clause_true = spam_classification_1(P_VALUES[minor_clause_1],H_VALUES[1],U_VALUES[minor_clause_2],G_VALUES[minor_clause_3])
                major_clause_false = spam_classification_1(P_VALUES[minor_clause_1],H_VALUES[0],U_VALUES[minor_clause_2],G_VALUES[minor_clause_3])
                if major_clause_true != major_clause_false:
                    CACC_test_set.append([P_VALUES[minor_clause_1],H_VALUES[1],U_VALUES[minor_clause_2],G_VALUES[minor_clause_3]])
                    CACC_test_set.append([P_VALUES[minor_clause_1],H_VALUES[0],U_VALUES[minor_clause_2],G_VALUES[minor_clause_3]])
                    break
            # si U est la clause majeure
            elif i==2:
                major_clause_true = spam_classification_1(P_VALUES[minor_clause_1],H_VALUES[minor_clause_2],U_VALUES[1],G_VALUES[minor_clause_3])
                major_clause_false = spam_classification_1(P_VALUES[minor_clause_1],H_VALUES[minor_clause_2],U_VALUES[0],G_VALUES[minor_clause_3])
                if major_clause_true != major_clause_false:
                    CACC_test_set.append([P_VALUES[minor_clause_1],H_VALUES[minor_clause_2],U_VALUES[1],G_VALUES[minor_clause_3]])
                    CACC_test_set.append([P_VALUES[minor_clause_1],H_VALUES[minor_clause_2],U_VALUES[0],G_VALUES[minor_clause_3]])
                    break
            # si G est la clause majeure 
            elif i==3:
                major_clause_true = spam_classification_1(P_VALUES[minor_clause_1],H_VALUES[minor_clause_2],U_VALUES[minor_clause_3],G_VALUES[1])
                major_clause_false = spam_classification_1(P_VALUES[minor_clause_1],H_VALUES[minor_clause_2],U_VALUES[minor_clause_3],G_VALUES[0])
                if major_clause_true != major_clause_false:
                    CACC_test_set.append([P_VALUES[minor_clause_1],H_VALUES[minor_clause_2],U_VALUES[minor_clause_3],G_VALUES[1]])
                    CACC_test_set.append([P_VALUES[minor_clause_1],H_VALUES[minor_clause_2],U_VALUES[minor_clause_3],G_VALUES[0]])
    print(CACC_test_set)
        
CACC()
