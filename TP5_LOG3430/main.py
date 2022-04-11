import json
from text_cleaner import TextCleaning
from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer

def evaluate(jsonText):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    analyzer = EmailAnalyzer()
    with open(jsonText) as email_file:
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

        if ((analyzer.is_spam(subject, body))) and (spam == "true"):
            tp += 1
        if (not (analyzer.is_spam(subject, body))) and (spam == "false"):
            tn += 1
        if ((analyzer.is_spam(subject, body))) and (spam == "false"):
            fp += 1
        if (not (analyzer.is_spam(subject, body))) and (spam == "true"):
            fn += 1
        total += 1
    
    print("")
    print("\nAccuracy: ", round((tp + tn) / (tp + tn + fp + fn), 2))
    print("Precision: ", round(tp / (tp + fp), 2))
    print("Recall: ", round(tp / (tp + fn), 2))

    precision = round(tp / (tp + fp), 2)
    recall = round(tp / (tp + fn), 2)
    f1_score = 2 * ((recall * precision)/(recall + precision))
    print("F1Score: ", end = ' ')
    print(f1_score)
    return f1_score

if __name__ == "__main__":

    # 1. Creation de vocabulaire.
    vocab = VocabularyCreator()
    vocab.create_vocab()

    # 2. Classification des emails et initialisation des utilisateurs et des groupes.
    renege = RENEGE()
    renege.classify_emails()

    #3. Evaluation de performance du modele avec la fonction evaluate()
    evaluate("test_set.json")

