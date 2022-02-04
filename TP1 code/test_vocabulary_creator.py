from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch

class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        self.mails = {"dataset":[{"mail":{"Subject":"loW", "Body":"HiGh", "Spam":"true"}}]}  # données pour mocker "return_value" du "load_dict"
        self.mails_false = {"dataset":[{"mail":{"Subject":"loW", "Body":"HiGh", "Spam":"false"}}]}  # données pour mocker "return_value" du "load_dict"
        self.clean_subject_spam = [{"o"}, {"r"}, {"b"}]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_spam = [{"o"}, {"r"}, {"b"}]  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_ham = [{"o"}, {"r"}, {"b"}]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_ham = [{"o"}, {"r"}, {"b"}]  # données pour mocker "return_value" du "clean_text"
        self.vocab_expected = {}  # vocabulaire avec les valeurs de la probabilité calculées correctement

    def tearDown(self):
        pass

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.VocabularyCreator.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_spam_Returns_vocabulary_with_correct_values(
        self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        """Description: Tester qu'un vocabulaire avec les probabilités calculées
        correctement va être retourné. Il faut mocker les fonctions "load dict"
         (utiliser self.mails comme une simulation de valeur de retour),"clean text"
         (cette fonction va être appelée quelques fois, pour chaque appel on
         va simuler une valeur de retour differente, pour cela il faut utiliser
         side_effect (voir l'exemple dans l'énonce)) et
         "write_data_to_vocab_file" qui va simuler "return True" au lieu
         d'écrire au fichier "vocabulary.json".
         if faut utiliser self.assertEqual(appel_a_create_vocab(), self.vocab_expected)
        """
        vocabulary = VocabularyCreator()
        mock_load_dict.return_value = self.mails
        list_of_values = [self.clean_subject_ham, self.clean_subject_spam, self.clean_body_ham, self.clean_body_spam]

        def side_effect(self):
            return list_of_values.pop()
        mock_clean_text.side_effect = side_effect
        print("Test 1 executed")
        mock_write_data_to_vocab_file.return_value = True
        self.assertEqual(vocabulary.create_vocab(), True)
    
    ###########################################
    #               CUSTOM TEST               #
    ###########################################

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.VocabularyCreator.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_spam_false_Returns_vocabulary_with_correct_values(
        self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        vocabulary = VocabularyCreator()
        mock_load_dict.return_value = self.mails_false
        list_of_values = [self.clean_subject_ham, self.clean_subject_spam, self.clean_body_ham, self.clean_body_spam]

        def side_effect(self):
            return list_of_values.pop()
        mock_clean_text.side_effect = side_effect
        print("Test 2 executed")
        mock_write_data_to_vocab_file.return_value = True
        self.assertEqual(vocabulary.create_vocab(), True)