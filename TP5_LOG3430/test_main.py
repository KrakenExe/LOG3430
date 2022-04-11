import json

import unittest
import random
from unittest.mock import patch

from main import evaluate
from text_cleaner import TextCleaning


class TestMain(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_nettoyage_train(self):
        """
        Test pour nettoyage du body du train set
        """
        clean = TextCleaning()
        with open("train_set.json") as email_file:
            train_emails = json.load(email_file)

        i = 0

        #Cleaning body
        for e_mail in train_emails["dataset"]:
            i += 1
            new_email = e_mail["mail"]
            body = clean.clean_text(new_email["Body"])
            train_emails["Body"] = body

        #Creating new json file
        with open("train_clean.json", "w") as  email_file:
            json.dump(train_emails, email_file)
        
        scoreOfTrainSet = evaluate("train_set.json")
        scoreOfTrainClean = evaluate("train_clean.json")
        self.assertEqual(scoreOfTrainSet, scoreOfTrainClean)

    def test_nettoyage_test(self):
        """
        Test pour nettoyage du body du test set
        """
        clean = TextCleaning()
        with open("test_set.json") as email_file:
            test_emails = json.load(email_file)

        i = 0

        #Cleaning body
        for e_mail in test_emails["dataset"]:
            i += 1
            new_email = e_mail["mail"]
            body = clean.clean_text(new_email["Body"])
            test_emails["Body"] = body

        #Creating new json file
        with open("test_clean.json", "w") as  email_file:
            json.dump(test_emails, email_file)
        
        scoreOfTestSet = evaluate("test_set.json")
        scoreOfTestClean = evaluate("test_set.json")
        self.assertEqual(scoreOfTestSet, scoreOfTestClean)

    def test_permutation_train(self):
        """
        Test pour permutation du body du train set
        """
        with open("train_set.json") as email_file:
            train_emails = json.load(email_file)

        i = 0

        #Cleaning body
        for e_mail in train_emails["dataset"]:
            i += 1
            new_email = e_mail["mail"]
            body = new_email["Body"]
            newBody = body.split()
            middleOfBody = int((len(newBody)-1)/2)
            j = 0
            #Random permutation
            if len(newBody) - 1 >= 0:
                while j < 10:
                    
                    length = middleOfBody
                    randomNumber = random.randint(0,length)
                    temp = newBody[0]
                    newBody[0] = newBody[randomNumber]
                    newBody[randomNumber] = temp
                    j += 1
            newJoinBody = " ".join(newBody)
            train_emails["Body"] = newJoinBody

        #Creating new json file
        with open("train_shuffle.json", "w") as  email_file:
            json.dump(train_emails, email_file)
        
        scoreOfTrainSet = evaluate("train_set.json")
        scoreOfTrainClean = evaluate("train_shuffle.json")
        self.assertEqual(scoreOfTrainSet, scoreOfTrainClean)

    def test_permutation_test(self):
        """
        Test pour permutation du body du test set
        """
        with open("test_set.json") as email_file:
            test_emails = json.load(email_file)

        i = 0

        #Cleaning body
        for e_mail in test_emails["dataset"]:
            i += 1
            new_email = e_mail["mail"]
            body = new_email["Body"]
            newBody = body.split()
            middleOfBody = int((len(newBody)-1)/2)
            j = 0
            #Random permutation
            if len(newBody) - 1 >= 0:
                while j < 10:
                    
                    length = middleOfBody
                    randomNumber = random.randint(0,length)
                    temp = newBody[0]
                    newBody[0] = newBody[randomNumber]
                    newBody[randomNumber] = temp
                    j += 1
            newJoinBody = " ".join(newBody)
            test_emails["Body"] = newJoinBody

        #Creating new json file
        with open("test_shuffle.json", "w") as  email_file:
            json.dump(test_emails, email_file)
        
        scoreOfTestSet = evaluate("test_set.json")
        scoreOfTestnClean = evaluate("test_shuffle.json")
        self.assertEqual(scoreOfTestSet, scoreOfTestnClean)

    def test_tripler_train(self):
        """
        Test pour tripler mail du train set (Ca va planter dans evaluate parce que notre newArray commence par [{"dataset":}] et a cause de [ ca n'arrive pas a le voir)
        Notre solution: On a copier coller 3 fois manuellement dans le fichier json generer
        """
        with open("train_set.json") as email_file:
            train_emails = json.load(email_file)

        newArray = []
        j = 0
        while j < 3:
            newArray.append(train_emails)
            j += 1

        #Creating new json file
        with open("train700x3.json", "w") as  email_file:
            json.dump(newArray, email_file)
        
        scoreOfTrainSet = evaluate("train_set.json")
        scoreOfTrainClean = evaluate("train700x3.json")
        self.assertEqual(scoreOfTrainSet, scoreOfTrainClean)

    def test_tripler_test(self):
        """
        Test pour tripler mail du test set (Ca va planter dans evaluate parce que notre newArray commence par [{"dataset":}] et a cause de [ ca n'arrive pas a le voir)
        Notre solution: On a copier coller 3 fois manuellement dans le fichier json generer
        """
        with open("test_set.json") as email_file:
            test_emails = json.load(email_file)

        newArray = []
        j = 0
        while j < 3:
            newArray.append(test_emails)
            j += 1

        #Creating new json file
        with open("test300x3.json", "w") as  email_file:
            json.dump(newArray, email_file)
        
        scoreOfTestSet = evaluate("test_set.json")
        scoreOfTestClean = evaluate("test300x3.json")
        self.assertEqual(scoreOfTestSet, scoreOfTestClean)

    def test_duplication_train(self):
        """
        Test pour duplication du body du train set
        """
        with open("train_set.json") as email_file:
            train_emails = json.load(email_file)
        i = 0

        for e_mail in train_emails["dataset"]:
            i += 1
            new_email = e_mail["mail"]
            body = new_email["Body"]
            splitBody = body.split()
            newArray = []
            length = len(splitBody) - 1
            j = 0
            if length >= 0:
                k = 0
                while j < 2:
                    while k < length:
                        newArray.extend([splitBody[k]])
                        k += 1
                    j += 1
            joinedBody = " ".join(newArray)
            train_emails["Body"] = joinedBody

        #Creating new json file
        with open("train_words.json", "w") as  email_file:
            json.dump(train_emails, email_file)
        
        scoreOfTrainSet = evaluate("train_set.json")
        scoreOfTrainClean = evaluate("train_words.json")
        self.assertEqual(scoreOfTrainSet, scoreOfTrainClean)

    def test_duplication_test(self):
        """
        Test pour duplication du body du test set.
        """
        with open("test_set.json") as email_file:
            test_emails = json.load(email_file)
        i = 0

        for e_mail in test_emails["dataset"]:
            i += 1
            new_email = e_mail["mail"]
            body = new_email["Body"]
            splitBody = body.split()
            newArray = []
            length = len(splitBody) - 1
            j = 0
            if length >= 0:
                k = 0
                while j < 2:
                    while k < length:
                        newArray.extend([splitBody[k]])
                        k += 1
                    j += 1
            joinedBody = " ".join(newArray)
            test_emails["Body"] = joinedBody

        #Creating new json file
        with open("test_words.json", "w") as  email_file:
            json.dump(test_emails, email_file)
        
        scoreOfTestSet = evaluate("test_set.json")
        scoreOfTestClean = evaluate("test_words.json")
        self.assertEqual(scoreOfTestSet, scoreOfTestClean)

    