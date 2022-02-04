import json

from email_analyzer import EmailAnalyzer

import unittest
from unittest.mock import patch


class TestEmailAnalyzer(unittest.TestCase):
    def setUp(self):
        self.subject = "orb"
        self.body = "orb"
        self.clean_subject = []  # données pour mocker "return_value" du "clean_text"
        self.clean_body = []  # données pour mocker "return_value" du "clean_text"
        self.spam_ham_body_prob_true = (
            1,
            0,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.spam_ham_subject_prob_true = (
            1,
            0,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.spam_ham_body_prob_false = (
            0,
            1,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.spam_ham_subject_prob_false = (
            0,
            1,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.vocab = (
            {"p_body_ham": [{"o"}, {"r"}],
             "p_body_spam": [{"Hello"}, {"r"}],
             "p_sub_ham": [{"o"}, {"r"}],
             "p_sub_spam": [{"Hello"}, {"r"}]
            }
        )  # vocabulaire avec les valeurs de la probabilité pour mocker "return_value" du "load_dict"
        self.spam_ham_body_prob_expected = 0.021944444444444444, 0.015092592592592591  # valeurs des probabilités attendues
        self.spam_ham_subject_prob_expected = 0.021944444444444444, 0.015092592592592591  # valeurs des probabilités attendues

    def tearDown(self):
        pass

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_subject_prob")
    def test_is_spam_Returns_True_if_spam_prob_is_higher(
        self, mock_spam_ham_subject_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être True si probabilité spam > probabilité ham
        """
        email = EmailAnalyzer()
        mock_spam_ham_subject_prob.return_value = self.spam_ham_body_prob_true
        mock_spam_ham_body_prob.return_value = self.spam_ham_subject_prob_true
        mock_clean_text.return_value = self.clean_subject
        mock_clean_text.return_value = self.clean_body
        print("Test 1 executed")
        self.assertEqual(email.is_spam(self.subject, self.body), True)

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_subject_prob")
    def test_is_spam_Returns_False_if_spam_prob_is_lower(
        self, mock_spam_ham_subject_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être False si probabilité spam < probabilité ham
        """
        email = EmailAnalyzer()
        mock_spam_ham_subject_prob.return_value = self.spam_ham_body_prob_false
        mock_spam_ham_body_prob.return_value = self.spam_ham_subject_prob_false
        mock_clean_text.return_value = self.clean_subject
        mock_clean_text.return_value = self.clean_body
        print("Test 2 executed")
        self.assertEqual(email.is_spam(self.subject, self.body), False)
        

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_spam_ham_body_prob_Returns_expected_probability(self, mock_load_dict):
        """
        Il faut mocker la fonction "load_dict"
        Il faut vérifier que probabilité est calculée correctement en fonction du "body"
        """
        email = EmailAnalyzer()
        mock_load_dict.return_value = self.vocab
        print("Test 3 executed")
        self.assertEqual(email.spam_ham_body_prob(self.body), self.spam_ham_body_prob_expected)

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_subject_spam_ham_prob_Returns_expected_probability(self, mock_load_dict):
        """
        Il faut mocker la fonction "load_dict"
        il faut vérifier que probabilité est calculée correctement en fonction du "sujet"
        """
        email = EmailAnalyzer()
        mock_load_dict.return_value = self.vocab
        print("Test 4 executed")
        self.assertEqual(email.spam_ham_subject_prob(self.body), self.spam_ham_subject_prob_expected)

    ###########################################
    #               CUSTOM TEST               #
    ###########################################
    