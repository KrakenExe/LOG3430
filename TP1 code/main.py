import json
from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer
from criteres import Criteres
import os



def evaluate(clean_option):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    analyzer = EmailAnalyzer()
    with open("test_set.json") as email_file:
        new_emails = json.load(email_file)

    i = 0
    email_count = len(new_emails["dataset"])

    print("Evaluating emails ")
    for e_mail in new_emails["dataset"]:
        i += 1
        print("\rEmail " + str(i) + "/" + str(email_count), end="")

        new_email = e_mail["mail"]
        subject = new_email["Subject"]
        body = new_email["Body"]
        spam = new_email["Spam"]

        if ((analyzer.is_spam(subject, body,clean_option))) and (spam == "true"):
            tp += 1
        if (not (analyzer.is_spam(subject, body, clean_option))) and (spam == "false"):
            tn += 1
        if ((analyzer.is_spam(subject, body, clean_option))) and (spam == "false"):
            fp += 1
        if (not (analyzer.is_spam(subject, body, clean_option))) and (spam == "true"):
            fn += 1
        total += 1
    
    print("")
    print("\nAccuracy: ", round((tp + tn) / (tp + tn + fp + fn), 2))
    print("Precision: ", round(tp / (tp + fp), 2))
    print("Recall: ", round(tp / (tp + fn), 2))
    return True

def tp2():
    S_expr_DNF = "(P AND H AND U) OR (P AND U AND NOT G)"
    not_S_expr_DNF = "NOT P OR (G AND NOT H) OR NOT U"
    criteres = Criteres()
    print("\n#########################################################################")
    print("jeux de test pour les critères CACC, GICC et IC")
    print("#########################################################################")
    criteres.CACC()
    criteres.GICC()
    criteres.print_test_set(criteres.truth_table_S(S_expr_DNF), criteres.truth_table_S(not_S_expr_DNF))

if __name__ == "__main__":

    #os.chdir("C:/Users/lasal/Desktop/LOG3430/TP1 code")

    # 1. Creation de vocabulaire.
    vocab = VocabularyCreator()
    vocab.create_vocab(1,0)

    # 2. Classification des emails et initialisation des utilisateurs et des groupes.
    renege = RENEGE()
    renege.classify_emails()

    #3. Evaluation de performance du modele avec la fonction evaluate()
    evaluate(0)

    #4.
    tp2()
