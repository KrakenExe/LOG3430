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
    n_entries = 16.0
    CACC_test_set = []

    # valeurs qui mettent la variable associée à vrai / faux
    H_true_value = 15
    H_false_value = 25
    U_true_value = 25
    U_false_value = 75
    G_true_value = 75
    G_false_value = 25

    minor_clause_entry = 0b000 #représente les entrées des clauses mineures. On l'incrémente de 1 à chaque itération

    # P en clause majeure
    for i in range(8):
        entry_as_string = str(minor_clause_entry)
        H = H_true_value if entry_as_string[0]=='1' else H_false_value
        U = U_true_value if entry_as_string[1]=='1' else U_false_value
        G = G_true_value if entry_as_string[2]=='1' else G_false_value
        if spam_classification_1(True,H,U,G) != spam_classification_1(True,H,U,G):
            CACC_test_set.append([True,H,U,G])
            break
        minor_clause_entry+=1
    print(CACC_test_set)    

CACC()