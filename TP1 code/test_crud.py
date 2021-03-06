from email.policy import default
from os import name
from tokenize import group
from crud import CRUD
import unittest
from unittest.mock import patch

import datetime

class TestCRUD(unittest.TestCase):
    def setUp(self):
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_users_file
        self.users_data = {
            "1": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "SpamN": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }
        }
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_groups_file
        self.groups_data = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

    def tearDown(self):
        pass


    @patch("crud.CRUD.read_users_file")    
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_add_new_user_Passes_correct_data_to_modify_users_file(
        self, mock_modify_users_file, mock_modify_groups_file, mock_read_users_file
    ):
        """Description: il faut utiliser les mocks des fonctions "read_users_file",
        "modify_users_file" pour tester que l'information a ajouter pour l'utilisateur a été formée correctement
        par la fonction, e.g. self.modify_users_file(data) -> "data" doit avoir un format et contenu expecté
        il faut utiliser ".assert_called_once_with(expected_data)"

        Note: Ce test a deja ete complete pour vous
        """

        # Ici on mock pour que read_users_file retourne la liste d'utilisateurs
        mock_read_users_file.return_value = self.users_data

        # Les informations du nouvel utilisateur
        new_user_data = {
                "name": "james@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }

        # On effectue une copie de la liste d'utilisateurs
        users_data_final = {}
        users_data_final["1"] = self.users_data["1"]
        users_data_final["2"] = self.users_data["2"]
        # On ajoute les infos du nouvel utilisateur
        users_data_final["0"] = new_user_data

        crud = CRUD()
        crud.add_new_user("james@gmail.com", "2020-08-08")
        # On vérifie que quand on ajoute un nouvel utilisateur, modify_users_file est appelée avec la nouvelle liste mise à jour
        mock_modify_users_file.assert_called_once_with(users_data_final)
          		

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")    
    def test_add_new_group_Passes_correct_data_to_modify_groups_file(
        self, mock_modify_groups_file, mock_read_groups_file
    ):
        """Description: il faut utiliser les mocks des fonctions "read_groups_file",
        "modify_groups_file" (ou selon votre realisation) pour tester que
        l'information a ajouter pour le groupe a été formée correctement par la fonction e.g.
        self.modify_groups_file(data) -> "data" doit avoir un format et contenu attendu
        il faut utiliser ".assert_called_once_with(expected_data)"
        """

        mock_read_groups_file.return_value = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": []
            }
        }

        crud = CRUD()
        name = "group"
        trust = 80
        members = []

        crud.add_new_group(name,trust,members)
  

        groups = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": []
            },
            "1": {
                "name": name,
                "Trust": trust,
                "List_of_members": members
            }
        }
        mock_modify_groups_file.assert_called_once_with(groups)

        
    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_id(self, mock_read_users_file):
        """Description: il faut utiliser le mock de fonction "read_users_file",
        (ou selon votre realisation) pour tester que false (ou bien une exception)
        est retourne par la fonction si ID non-existant est utilisé
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """
        crud = CRUD()
        mock_read_users_file.return_value = {
            "0": {
                "user_email": "test@gmail.com",
                "date": datetime.datetime.now()
            }
        }
        
        #l'utilisateur avec l'id 1 n'existe pas, donc get_user_data retourne faux'
        self.assertFalse(crud.get_user_data(1,"name")) 
        

        
        

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_field(self, mock_read_users_file):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que false (ou bien une exception)
        est retourne par la fonction si champ non-existant est utilisé
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """
        crud = CRUD()
        mock_read_users_file.return_value = {
            "0": {
                "user_email": "test@gmail.com",
                "date": datetime.datetime.now()
            }
        }

        #l'utilisateur avec l'id 0 existe, mais le champ "imaginaryField" n'existe pas, donc get_user_data retourne faux
        self.assertFalse(crud.get_user_data(0,"imaginaryField")) 
        
        

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_users_file
    ):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que une bonne valeur est fournie
        si champ et id valide sont utilises
        il faut utiliser ".assertEqual()""
        """
        
        email = "test@gmail.com"
        mock_read_users_file.return_value = {
            "0":{
                "name": email,
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": datetime.datetime.now(),
                "Date_of_last_seen_message": datetime.datetime.now(),
                "Groups": ["default"]
            }
        }

        crud = CRUD()

        #l'utilisateur 0 et le champ "name" existent, donc get_user_data retourne bien "test@gmail.com"
        self.assertEqual(crud.get_user_data("0","name"),email)

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_id(self, mock_read_groups_file):
        """
        Similaire au test_get_user_data_Returns_false_for_invalid_id mais pour un groupe
        """
        
        id = "1"
        mock_read_groups_file.return_value = {}
        crud = CRUD()

        #le groupe d'id 1 n'existe pas, donc get_group_data retourne faux
        self.assertFalse(crud.get_groups_data(id,"name"))

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_field(
        self, mock_read_groups_file
    ):
        """
        Similaire au test_get_user_data_Returns_false_for_invalid_field mais pour un groupe
        """
        field = "imaginaryField"
        mock_read_groups_file.return_value = {}
        crud = CRUD()
        
        #le groupe d'id 0 (le groupe par défaut) existe, mais le champ "imaginaryField" n'existe pas, 
        # donc get_group_data retourne faux
        self.assertFalse(crud.get_groups_data(0,field))

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_groups_file
    ):
        """
        Similaire au test_get_user_data_Returns_correct_value_if_field_and_id_are_valid mais pour un groupe
        """
        field = "name"
        name = "newGroup"
        mock_read_groups_file.return_value = {
            "1" : {
                "name": name,
                "Trust": 75,
                "List_of_members": []
            }
        }
        crud = CRUD()

        # le groupe d'id 1 et le champ "name" existent, donc get_group_data retourne "newGroup"
        self.assertEqual(crud.get_groups_data(1,field),name)

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_false_for_invalid_user_name(
        self, mock_read_users_file
    ):
       user_email = "test@gmail.com" 
       mock_read_users_file.return_value = {}
       crud = CRUD()

       #l'utilisateur avec le courriel "test@gmail.com" n'existe pas, donc get_user_id retourne faux 
       self.assertFalse(crud.get_user_id(user_email))
        

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_id_for_valid_user_name(self, mock_read_users_file):
        user_email = "test@gmail.com"
        id = "0"
        mock_read_users_file.return_value = {
            "0" : {
                "name": user_email,
                "Trust": 50,
                "List_of_members": []   
            }
        } 
        crud = CRUD()

        #l'utilisateur avec le courriel "test@gmail.com" existe, donc get_user_id revoie son id (0)
        self.assertEqual(crud.get_user_id(user_email),id)

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_false_for_invalid_group_name(
        self, mock_read_groups_file
    ):
        group_name = "imaginaryGroup"
        mock_read_groups_file.return_value = {}
        crud = CRUD()

        #le groupe "imaginaryGroup" n'exsite pas, donc get_group_id retourne faux
        self.assertFalse(crud.get_group_id(group_name))

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_id_for_valid_group_name(self, mock_read_groups_file):
        
        group_name = "validGroup"
        id = "0"
        mock_read_groups_file.return_value = {
            "0": {
                "name": group_name,
                "Trust": 75,
                "List_of_members": []
            }
        }
        crud = CRUD()

        #le groupe "validGroup" existe, donc get_group_id retourne son id (0)
        self.assertEqual(crud.get_group_id(group_name),id)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    # Modify_user_file mock est inutile pour tester False pour update
    def test_update_users_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """

        id = "1"
        mock_read_users_file.return_value = {
            "0":{
                "name":"name",
                "Trust":50,
                "List_of_members":[]
            }
        }
        crud = CRUD()

        #le champ "Trust" existe, mais l'utilisateur d'id 1 n'existe pas, donc update_users doit renvoyer faux
        self.assertFalse(crud.update_users(id,"Trust",75))

        #étant donné que l'utilisateur d'id 1 n'existe pas, modify_users ne doit pas avoir été appellé
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_update_users_Returns_false_for_invalid_field(
        self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """
        
        field = "imaginaryField"
        mock_read_users_file.return_value = {
            "0":{
                "name":"name",
                "Trust":50,
                "List_of_members":[]
            }
        }
        crud = CRUD()

        #l'utilisateur d'id 0 existe, mais pas le champ "imaginary field", donc update_users doit renvoyer faux
        self.assertFalse(crud.update_users("0",field,75))


    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_update_users_Passes_correct_data_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_read_users_file.return_value = {
            "0":{
                "name": "name",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": ["default"]
            }
        }

        crud = CRUD()
        id = "0"
        field = "Trust"
        data = 80
        crud.update_users(id,field,data)

        users = mock_read_users_file.return_value

        #la fonction modify_user_file doit être appellé avec les bonnes valeurs
        mock_modify_users_file.assert_called_once_with(users)
        

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_false_for_invalid_id(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """
        mock_read_groups_file.return_value = {}
        crud = CRUD()
        id = "1"
        field = "Trust"
        data = 75

        #étant donné que le champ "imaginaryField" n'existe pas, update_group doit retourner faux
        self.assertFalse(crud.update_groups(id,field,data)) 


    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_false_for_invalid_field(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """
        mock_read_groups_file.return_value = {}
        crud = CRUD()
        #le groupe d'id 0 existe (groupe par défaut) mais le champ "imaginaryField" n'existe pas, donc update_groups doit retourner faux
        self.assertFalse(crud.update_groups("0","imaginaryField",75))



    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Passes_correct_data_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_read_groups_file.return_value = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": []
            }
        }

        groups = {
            "0": {
                "name": "default",
                "Trust": 75,
                "List_of_members": []
            }
        }

        crud = CRUD()
        crud.update_groups("0","Trust",75)
        
        #update_groups doit appeller modify_groups_file avec les bons paramètres
        mock_modify_groups_file.assert_called_once_with(groups)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = {
            "0":{
                "name": "name",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": ["default"]
            }
        }
        id="1"
        crud = CRUD()
        # le groupe d'id 1 n'existe pas donc remove_user doit retourner faux
        self.assertFalse(crud.remove_user(id))
    

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_Passes_correct_value_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        user_data = {
          "0":{
              "name": "name",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": ["default"]
            }
        }
        
        mock_read_users_file.return_value = user_data
        id="0"
        crud = CRUD()
        crud.remove_user(id)
        #l'utilisateur d'id 0 existe, donc modify_users_file doit être appelé avec les bonnes valeurs
        mock_modify_users_file.assert_called_once_with(user_data)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_group_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = {
            "0":{
                "name": "name",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": ["group1"]
            }
        }
        crud = CRUD()
        #le groupe "group1" existe mais pas l'utilisateur d'id 1, donc remove_user_group doit retourner faux
        self.assertFalse(crud.remove_user_group("1","group1"))

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_group_Returns_false_for_invalid_group(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = {
            "0":{
                "name": "name",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": ["group1"]
            }
        }
        crud = CRUD()
        #l'utilisateur d'id 0 existe mais pas le groupe "groupe2", donc remove_user_group doit retourner faux
        self.assertFalse(crud.remove_user_group("0","group2"))


    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Passes_correct_value_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        
        mock_read_users_file.return_value = {
            "0":{
                "name": "name",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": ["group1"]
            }
        }

        user_data_after_remove = {
            "0":{
                "name": "name",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": []
            }
        }

        crud = CRUD()
        crud.remove_user_group("0","group1")
        #on retire "group1", qui est le seul groupe de l'utilisateur 0, 
        # donc modify_users_file doit être appellé avec un utilisateur qui a une liste de groupes vide
        mock_modify_users_file.assert_called_once_with(user_data_after_remove)


    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_Returns_false_for_invalid_id(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = {}
        crud = CRUD()
        #le group d'id 1 n'existe pas, donc remove_group doit retourner faux
        self.assertFalse(crud.remove_group("1"))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_Passes_correct_value_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
    
        groups = {
            "0":{
                "name":"default",
                "Trust":50,
                "List_of_members":[]
            },
            "1":{
                "name":"group1",
                "Trust":75,
                "List_of_members":[]
            }
        }

        mock_read_groups_file.return_value = groups
        
        crud = CRUD()
        crud.remove_group("1")
        #le groupe d'id 1 existew, donc modify_group_files doit être appelé avec groups
        mock_modify_groups_file.assert_called_once_with(groups)


    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Returns_false_for_invalid_id(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = {}
        crud = CRUD()
        #le groupe d'id 1 n'existe pas, donc remove_group_member doit retourner faux
        self.assertFalse(crud.remove_group_member("1","user1"))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Returns_false_for_invalid_group_member(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = {
            "0":{
                "name":"group",
                "Trust":75,
                "List_of_members":["user1"]
            }
        }
        
        crud = CRUD()
        #le groupe d'id 0 existe mais pas l'utilisateur "user2", donc remove_group_member doit renvoyer faux
        self.assertFalse(crud.remove_group_member("0","user2"))
    

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Passes_correct_value_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = {
            "0":{
                "name":"default",
                "Trust":50,
                "List_of_members":[]
            },
            "1":{
                "name":"group",
                "Trust":75,
                "List_of_members":["user1"]
            }
        }

        groups_after_remove = {
             "0":{
                "name":"default",
                "Trust":50,
                "List_of_members":[]
            },
            "1":{
                "name":"group",
                "Trust":75,
                "List_of_members":[]
            }
        }

        crud = CRUD()
        crud.remove_group_member("1","user1")
        #on retire l'utilisateur user1 (qui est le seul membre de son groupe) du groupe d'id 1, 
        # donc modify_groups_file doit être appelé avec un groupe d'id 1 qui
        #a une liste de membres vide
        mock_modify_groups_file.assert_called_once_with(groups_after_remove)
    
    ###########################################
    #               CUSTOM TEST               #
    ###########################################

    @patch("crud.CRUD.read_users_file")
    def test_get_new_user_id_returns_correct_id(self, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "name",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": []
            }
        }

        crud = CRUD()
        self.assertEqual(crud.get_new_user_id(),"1")

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_add_new_user_Returns_false_for_invalid_email_format(self, mock_read_users_file, mock_modify_users_file):
        crud = CRUD()
        #le format de "invalid_email" n'est pas valide, donc add_new_user doit retourner faux
        self.assertFalse(crud.add_new_user("invalid_email",""))

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_add_new_user_Returns_false_if_email_already_exists(self, mock_read_users_file, mock_modify_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": []
            }
        }
        crud = CRUD()
        #l'utilisateur "test@gmail.com" existe deja, donc add_new_user doit renvoyer faux
        self.assertFalse(crud.add_new_user("test@gmail.com", "2020-08-08"))
    
    
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_add_new_group(self,mock_modify_groups_file, mock_read_groups_file, mock_modify_users_file, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": []
            }
        }

        crud = CRUD()
        #l'utilisateur "fakeUser@gmail.com" n'existe pas, donc add_new_group doit retourner faux
        self.assertFalse(crud.add_new_group("group1", 50, ["fakeUser@gmail.com"]))
    
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Returns_false_for_invalid_email_format(self, mock_modify_users_file, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": []
            }
        }
        crud = CRUD()
        #on remplace le courriel de l'utilisateur par une expression invalide, donc update_users doit retourner faux
        self.assertFalse(crud.update_users("0","name","invalidEmail"))

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Correctly_updates_username(self, mock_modify_users_file, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": []
            }
        }
        new_user_data = {
            "0":{
                "name": "new@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": "",
                "Date_of_last_seen_message": "",
                "Groups": []
            }
        }
        crud = CRUD()
        crud.update_users("0","name","new@gmail.com")
        mock_modify_users_file.assert_called_once_with(new_user_data)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Returns_false_if_Date_of_last_seen_message_is_older_than_previous(self, mock_modify_users_file, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": []
            }
        }
        crud = CRUD()
        #la date passée est plus ancienne que la date du message le plus récent, donc update_users doit retourner faux
        self.assertFalse(crud.update_users("0","Date_of_last_seen_message","1999-08-08"))

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Correctly_updates_Date_of_last_seen_message(self, mock_modify_users_file, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": []
            }
        }
        
        crud = CRUD()
        date = "2042-08-08"
        unix_date = crud.convert_to_unix(date)

        new_user_data = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message":  unix_date,
                "Groups": []
            }
        }
        #modify_users_file doit être appelé avec la nouvelle valeur de Date_of_last_seen_message 
        crud.update_users("0","Date_of_last_seen_message","2042-08-08")
        mock_modify_users_file.assert_called_once_with(new_user_data)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Returns_false_if_Date_of_first_seen_message_is_newer_than_previous(self, mock_modify_users_file, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": []
            }
        } 
        crud = CRUD()
        #la date passée est plus récente que la date du message le plus ancien, donc update_users doit retourner faux
        self.assertFalse(crud.update_users("0","Date_of_first_seen_message","2042-08-08"))

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Correctly_updates_Date_of_first_seen_message(self, mock_modify_users_file, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": []
            }
        }

        crud =CRUD()
        date = "1999-08-08"
        unix_date = crud.convert_to_unix(date)

        new_user_data = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": unix_date,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": []
            }
        }
        crud.update_users("0","Date_of_first_seen_message","1999-08-08")
        #modify_users_file doit être appelé avec la nouvelle valeur de Date_of_first_seen_message
        mock_modify_users_file.assert_called_once_with(new_user_data)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Returns_false_if_new_trust_is_lower_than_zero(self, mock_modify_users_file, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": []
            }
        }
        crud = CRUD()
        #la valeur passée est inférieur à la valeur minimum permise pour Trust, donc update_users doit retourner faux
        self.assertFalse(crud.update_users("0","Trust",-1))

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Returns_false_if_new_trust_is_higher_than_one_hundred(self, mock_modify_users_file, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": []
            }
        }
        crud = CRUD()
        #la valeur passée est supérieure à la valeur maximum permise pour Trust, donc update_users doit retourner faux
        self.assertFalse(crud.update_users("0","Trust",101))

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Correctly_updates_trust(self, mock_modify_users_file, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": []
            }
        }

        new_user_data = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 75,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": []
            }
        }

        crud = CRUD()
        crud.update_users("0","Trust",75)
        #modify_users doit être apellé avec la nouvelle valeur de Trust
        mock_modify_users_file.assert_called_once_with(new_user_data)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Returns_false_if_SpamN_lower_than_zero(self, mock_modify_users_file, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": []
            }
        }
        crud = CRUD()
        #la valeur passée est inférieure à la valeur minimum permise pour SpamN, donc update_users doit retourner faux 
        self.assertFalse(crud.update_users("0","SpamN",-1))

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Correctly_updates_SpamN(self, mock_modify_users_file, mock_read_users_file):
        mock_read_users_file.return_value = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": []
            }
        }
        
        new_user_data = {
            "0":{
                "name": "test@gmail.com",
                "Trust": 50,
                "SpamN": 50,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": []
            }
        }
        crud = CRUD()
        crud.update_users("0","SpamN",50)
        #modify_users_file doit être appelé avec la nouvelle valeur de SpamN
        mock_modify_users_file.assert_called_once_with(new_user_data)