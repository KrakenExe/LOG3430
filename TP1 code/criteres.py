from email_analyzer import EmailAnalyzer
from vocabulary_creator import VocabularyCreator
from renege import RENEGE



def classification_spam_1(is_spam,time_between_first_and_last,user_trust,group_trust):
    P = is_spam
    H = True if time_between_first_and_last<20 else False
    U = True if user_trust<50 else False
    G = True if group_trust>=5 else False

    S = P and ((H and U) or (U and not G))
    return S

def classification_spam_2(is_spam,time_between_first_and_last,user_trust,group_trust):
    P = is_spam
    H = True if time_between_first_and_last<20 else False
    U = True if user_trust<50 else False
    G = True if group_trust>=5 else False

    S = P and H and U or P and U and not G
    return S 