from email_analyzer import EmailAnalyzer
from vocabulary_creator import VocabularyCreator
from renege import RENEGE
import re



def spam_classification_1(P,H,U,G):
    H = True if H<20 else False
    U = True if U<50 else False
    G = True if G>=50 else False
    S = P and ((H and U) or (U and not G))
    return S

def spam_classification_2(P,H,U,G):
    H = True if H<20 else False
    U = True if U<50 else False
    G = True if G>=50 else False
    S = P and H and U or P and U and not G
    return S

def CACC():
    N_MINOR_CLAUSE_COMBINATIONS = 8
    N_CLAUSES = 4
    CACC_test_set = []

    # valeurs qui mettent la variable associée à vrai / faux dans les fonctions spam_classification (valeur à [0] = faux, [1] = vrai)
    P_VALUES = [False,True]
    H_VALUES = [25,15]
    U_VALUES = [75,25]
    G_VALUES = [25,75]

    #index pour l'affichage du jeu de test
    P_INDEX = 0
    H_INDEX = 1
    U_INDEX = 2
    G_INDEX = 3

    for i in range(N_CLAUSES):

        for j in range(N_MINOR_CLAUSE_COMBINATIONS):
            entry_as_binary = int(bin(j),2)

            # permet d'obtenir les valeurs des bits en 1ere, 2eme et 3eme position dans entry_as_binary, qui représentent les entrées des 3 clauses mineures
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
                    break
    print("jeu de test pour le critère CACC:\n")
    for i in range(len(CACC_test_set)):
        output = "d{index} = <(P={P}, H={H}, U={U}, G={G}),({result})>"
        S = spam_classification_1(CACC_test_set[i][P_INDEX],CACC_test_set[i][H_INDEX],CACC_test_set[i][U_INDEX],CACC_test_set[i][G_INDEX])
        print(output.format(index=i+1,P=CACC_test_set[i][P_INDEX],H=CACC_test_set[i][H_INDEX],U=CACC_test_set[i][U_INDEX],G=CACC_test_set[i][G_INDEX],result=S))
      
        
CACC()
