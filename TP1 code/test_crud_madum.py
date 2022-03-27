




from unittest.mock import patch
from crud import CRUD
import unittest


class TestCRUDMadum(unittest.TestCase):


    def setUp(self):
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_users_file
        self.users_data = {
            "0": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            },
            "1": {
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
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "1": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

    def tearDown(self):
        pass

    # def test_rapporteur(self):
    #     crud = CRUD()
    #     crud.add_new_group("test_madum", 50, ["alex@gmail.com", "mark@mail.com"])
    #     group_name = crud.get_groups_data(len(crud.groups_data) - 1, "name")
    #     self.assertEqual("test_madum", group_name)

    # @patch("crud.CRUD.read_users_file")
    # @patch("crud.CRUD.read_groups_file")
    # def test_constructeur(self, mock_read_groups_file, mock_read_users_file):
    #     mock_read_groups_file.return_value = self.groups_data
    #     mock_read_users_file.return_value = self.users_data
    #     crud = CRUD()
    #     self.assertDictEqual(crud.groups_data, self.groups_data)

# Permutation des transformateurs
# 1) remove_group_member,add_new_group,update_groups,remove_group
# 2) add_new_group,remove_group_member,update_groups,remove_group
# 3) update_groups,remove_group_member,add_new_group,remove_group
# 4) remove_group_member,update_groups,add_new_group,remove_group
# 5) add_new_group,update_groups,remove_group_member,remove_group
# 6) update_groups,add_new_group,remove_group_member,remove_group
# 7) update_groups,add_new_group,remove_group,remove_group_member
# 8) add_new_group,update_groups,remove_group,remove_group_member
# 9) remove_group,update_groups,add_new_group,remove_group_member
# 10) update_groups,remove_group,add_new_group,remove_group_member
# 11) add_new_group,remove_group,update_groups,remove_group_member
# 12) remove_group,add_new_group,update_groups,remove_group_member
# 13) remove_group,remove_group_member,update_groups,add_new_group
# 14) remove_group_member,remove_group,update_groups,add_new_group
# 15) update_groups,remove_group,remove_group_member,add_new_group
# 16) remove_group,update_groups,remove_group_member,add_new_group
# 17) remove_group_member,update_groups,remove_group,add_new_group
# 18) update_groups,remove_group_member,remove_group,add_new_group
# 19) add_new_group,remove_group_member,remove_group,update_groups
# 20) remove_group_member,add_new_group,remove_group,update_groups
# 21) remove_group,add_new_group,remove_group_member,update_groups
# 22) add_new_group,remove_group,remove_group_member,update_groups
# 23) remove_group_member,remove_group,add_new_group,update_groups
# 24) remove_group,remove_group_member,add_new_group,update_groups

# Branches
# update_groups
#       field == name
#       field == Trust
#       field == List_of_members

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence1_branche1(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        ################################
        ## Branche 1 (field == Trust) ##
        ################################
        result = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "test_madum",
                "Trust": 75,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        crud.remove_group_member(0, "alex@gmail.com")
        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        crud.update_groups(2, "Trust", 75)
        crud.remove_group(1)
        self.assertDictEqual(crud.groups_data, result)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence1_branche2(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        ###############################
        ## Branche 2 (field == name) ##
        ###############################
        result = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "hello",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        crud.remove_group_member(0, "alex@gmail.com")
        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        crud.update_groups(2, "name", "hello")
        crud.remove_group(1)
        self.assertDictEqual(crud.groups_data, result)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence1_branche3(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        ##########################################
        ## Branche 3 (field == List_of_members) ##
        ##########################################
        result = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "test_madum",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
        }

        crud.remove_group_member(0, "alex@gmail.com")
        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        crud.update_groups(2, "List_of_members", ["mark@mail.com"])
        crud.remove_group(1)
        self.assertDictEqual(crud.groups_data, result)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence2_branche1(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        ##########################################
        ## Branche 1 (field == Trust) ##
        ##########################################
        result = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "test_madum",
                "Trust": 75,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        crud.remove_group_member(0, "alex@gmail.com")
        crud.update_groups(2, "Trust", 75)
        crud.remove_group(1)
        self.assertDictEqual(crud.groups_data, result)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence2_branche2(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        ##########################################
        ## Branche 2 (field == name) ##
        ##########################################
        result = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "hello",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        crud.remove_group_member(0, "alex@gmail.com")
        crud.update_groups(2, "name", "hello")
        crud.remove_group(1)
        self.assertDictEqual(crud.groups_data, result)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence2_branche3(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        ##########################################
        ## Branche 3 (field == List_of_members) ##
        ##########################################
        result = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "test_madum",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
        }

        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        crud.remove_group_member(0, "alex@gmail.com")
        crud.update_groups(2, "List_of_members", ["mark@mail.com"])
        crud.remove_group(1)
        self.assertDictEqual(crud.groups_data, result)


# À partir de la séquence 3, nous avons changer la méthode de test pour réduire le nombre de cas de test.
# Nous testons dans les 3 branches de update_groups() à l'intérieur du même cas de test.


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence3(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "1": {
                "name": "hello",
                "Trust": 75,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "test_madum",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        # Branche 1
        crud.update_groups(1, "Trust", 75)
        # Branche 2
        crud.update_groups(1, "name", "hello")
        # Branche 3
        crud.update_groups(1, "List_of_members", ["mark@mail.com", "alex@gmail.com"])
        crud.remove_group_member(1, "alex@gmail.com")
        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        crud.remove_group(0)
        self.assertDictEqual(crud.groups_data, result)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence4(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "1": {
                "name": "hello",
                "Trust": 75,
                "List_of_members": ["mark@mail.com", "alex@gmail.com"],
            },
            "2": {
                "name": "test_madum",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        crud.remove_group_member(0, "mark@mail.com")
        # Branche 1
        crud.update_groups(1, "Trust", 75)
        # Branche 2
        crud.update_groups(1, "name", "hello")
        # Branche 3
        crud.update_groups(1, "List_of_members", ["mark@mail.com", "alex@gmail.com"])
        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        crud.remove_group(0)
        self.assertDictEqual(crud.groups_data, result)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence5(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "1": {
                "name": "hello",
                "Trust": 75,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "test_madum",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        # Branche 1
        crud.update_groups(1, "Trust", 75)
        # Branche 2
        crud.update_groups(1, "name", "hello")
        # Branche 3
        crud.update_groups(1, "List_of_members", ["mark@mail.com", "alex@gmail.com"])
        crud.remove_group_member(1, "alex@gmail.com")
        crud.remove_group(0)
        self.assertDictEqual(crud.groups_data, result)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence6(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "1": {
                "name": "hello",
                "Trust": 75,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "test_madum",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        # Branche 1
        crud.update_groups(1, "Trust", 75)
        # Branche 2
        crud.update_groups(1, "name", "hello")
        # Branche 3
        crud.update_groups(1, "List_of_members", ["mark@mail.com", "alex@gmail.com"])
        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        crud.remove_group_member(1, "alex@gmail.com")
        crud.remove_group(0)
        self.assertDictEqual(crud.groups_data, result)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence7(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "1": {
                "name": "hello",
                "Trust": 75,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "test_madum",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        # Branche 1
        crud.update_groups(1, "Trust", 75)
        # Branche 2
        crud.update_groups(1, "name", "hello")
        # Branche 3
        crud.update_groups(1, "List_of_members", ["mark@mail.com", "alex@gmail.com"])
        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        crud.remove_group(0)
        crud.remove_group_member(1, "alex@gmail.com")
        self.assertDictEqual(crud.groups_data, result)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence8(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "1": {
                "name": "hello",
                "Trust": 75,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "test_madum",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }
        
        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        # Branche 1
        crud.update_groups(1, "Trust", 75)
        # Branche 2
        crud.update_groups(1, "name", "hello")
        # Branche 3
        crud.update_groups(1, "List_of_members", ["mark@mail.com", "alex@gmail.com"])
        crud.remove_group(0)
        crud.remove_group_member(1, "alex@gmail.com")
        self.assertDictEqual(crud.groups_data, result)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence9(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "0": {
                "name": "Samuel",
                "Trust": 80,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "1": {
                "name": "test_madum",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            }, 
        }

        crud.remove_group(1)
        # Branche 1
        crud.update_groups(0, "Trust", 80)
        # Branche 2
        crud.update_groups(0, "name", "Samuel")
        # Branche 3
        crud.update_groups(0, "List_of_members", ["mark@mail.com", "bob@gmail.com"] )
        crud.add_new_group("test_madum", 50, ["alex@gmail.com"])
        crud.remove_group_member(0, ["bob@gmail.com"])
        self.assertDictEqual(crud.groups_data, result)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence10(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "0": {
                "name": "Duck",
                "Trust": 75,
                "List_of_members": ["alex@gmail.com"],
            },
            "1": {
                "name": "test_allo",
                "Trust": 60,
                "List_of_members": ["alex@gmail.com"],
            }, 
        }

        # Branche 1
        crud.update_groups(1, "Trust", 60)
        # Branche 2
        crud.update_groups(1, "name", "test_allo")
        # Branche 3
        crud.update_groups(1, "List_of_members", ["bob@gmail.com"])
        crud.remove_group(0)
        crud.add_new_group("Duck", 75, ["alex@gmail.com"])
        crud.remove_group_member(1, ["bob@gmail.com"])
        self.assertDictEqual(crud.groups_data, result)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence11(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "1": {
                "name": "test123",
                "Trust": 60,
                "List_of_members": ["alex@gmail.com"],
            }, 
            "2": {
                "name": "Maxime",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        crud.add_new_group("Maxime", 50, ["alex@gmail.com"])
        crud.remove_group(0)
        # Branche 1
        crud.update_groups(1, "Trust", 60)
        # Branche 2
        crud.update_groups(1, "name", "test123")
        # Branche 3
        crud.update_groups(1, "List_of_members", ["bob@gmail.com"])
        crud.remove_group_member(1, ["bob@gmail.com"])
        self.assertDictEqual(crud.groups_data, result)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence12(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "0": {
                "name": "Bob",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
            "1": {
                "name": "default",
                "Trust": 70,
                "List_of_members": ["alex@gmail.com"],
            }, 
        }

        crud.remove_group(0)
        crud.add_new_group("Bob", 50, ["mark@mail.com"])
        # Branche 1
        crud.update_groups(1, "Trust", 70)
        # Branche 2
        crud.update_groups(1, "name", "default")
        # Branche 3
        crud.update_groups(1, "List_of_members", ["sam@gmail.com"])
        crud.remove_group_member(1, ["sam@gmail.com"])
        self.assertDictEqual(crud.groups_data, result)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence13(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "0": {
                "name": "test_madum",
                "Trust": 45,
                "List_of_members": ["mark@mail.com", "alex@gmail.com"],
            }, 
            "1": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        crud.remove_group(1)
        crud.remove_group_member(0, "alex@gmail.com")
        # Branche 1
        crud.update_groups(0, "Trust", 45)
        # Branche 2
        crud.update_groups(0, "name", "test_madum")
        # Branche 3
        crud.update_groups(0, "List_of_members", ["mark@mail.com", "alex@gmail.com"])
        crud.add_new_group("friends", 90, ["alex@gmail.com"])
        self.assertDictEqual(crud.groups_data, result)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence14(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "0": {
                "name": "default",
                "Trust": 85,
                "List_of_members": ["alex@gmail.com"],
            }, 
            "1": {
                "name": "strangers",
                "Trust": 5,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        crud.remove_group_member(0, "alex@gmail.com")
        crud.remove_group(1)
        # Branche 1
        crud.update_groups(0, "Trust", 85)
        # Branche 2
        crud.update_groups(0, "name", "default")
        # Branche 3
        crud.update_groups(0, "List_of_members", ["alex@gmail.com"])
        crud.add_new_group("strangers", 5, ["alex@gmail.com", "mark@mail.com"])
        self.assertDictEqual(crud.groups_data, result)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence15(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "0": {
                "name": "Alex",
                "Trust": 45,
                "List_of_members": ["alex@gmail.com"],
            }, 
            "1": {
                "name": "Someone",
                "Trust": 15,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        # Branche 1
        crud.update_groups(0, "Trust", 45)
        # Branche 2
        crud.update_groups(0, "name", "Alex")
        # Branche 3
        crud.update_groups(0, "List_of_members", ["alex@gmail.com", "mark@mail.com"])
        crud.remove_group(1)
        crud.remove_group_member(0, "mark@mail.com")
        crud.add_new_group("Someone", 15, ["alex@gmail.com", "mark@mail.com"])
        self.assertDictEqual(crud.groups_data, result)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_transformateurs_sequence16(self, mock_read_groups_file, mock_read_users_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        result = {
            "0": {
                "name": "Cedric",
                "Trust": 20,
                "List_of_members": ["alex@gmail.com"],
            }, 
            "1": {
                "name": "Poly",
                "Trust": 95,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        crud.remove_group(1)
        # Branche 1
        crud.update_groups(0, "Trust", 20)
        # Branche 2
        crud.update_groups(0, "name", "Cedric")
        # Branche 3
        crud.update_groups(0, "List_of_members", ["alex@gmail.com", "mark@mail.com"])
        crud.remove_group_member(0, "mark@mail.com")
        crud.add_new_group("Poly", 95, ["alex@gmail.com", "mark@mail.com"])
        self.assertDictEqual(crud.groups_data, result)

# def test_transformateurs_sequence17(self):
#     crud = CRUD()
#     crud.remove_group_member()
#     crud.update_groups()
#     crud.update_groups()
#     crud.update_groups()
#     crud.remove_group()
#     crud.add_new_group()
#     self.assertListEqual()

# def test_transformateurs_sequence18(self):
#     crud = CRUD()
#     crud.update_groups()
#     crud.update_groups()
#     crud.update_groups()
#     crud.remove_group_member()
#     crud.remove_group()
#     crud.add_new_group()
#     self.assertListEqual()

# def test_transformateurs_sequence19(self):
#     crud = CRUD()
#     crud.add_new_group()
#     crud.remove_group_member()
#     crud.remove_group()
#     crud.update_groups()
#     crud.update_groups()
#     crud.update_groups()
#     self.assertListEqual()

# def test_transformateurs_sequence20(self):
#     crud = CRUD()
#     crud.remove_group_member()
#     crud.add_new_group()
#     crud.remove_group()
#     crud.update_groups()
#     crud.update_groups()
#     crud.update_groups()
#     self.assertListEqual()

# def test_transformateurs_sequence21(self):
#     crud = CRUD()
#     crud.remove_group()
#     crud.add_new_group()
#     crud.remove_group_member()
#     crud.update_groups()
#     crud.update_groups()
#     crud.update_groups()
#     self.assertListEqual()

# def test_transformateurs_sequence22(self):
#     crud = CRUD()
#     crud.add_new_group()
#     crud.remove_group()
#     crud.remove_group_member()
#     crud.update_groups()
#     crud.update_groups()
#     crud.update_groups()
#     self.assertListEqual()

# def test_transformateurs_sequence23(self):
#     crud = CRUD()
#     crud.remove_group_member()
#     crud.remove_group()
#     crud.add_new_group()
#     crud.update_groups()
#     crud.update_groups()
#     crud.update_groups()
#     self.assertListEqual()

# def test_transformateurs_sequence24(self):
#     crud = CRUD()
#     crud.remove_group()
#     crud.remove_group_member()
#     crud.add_new_group()
#     crud.update_groups()
#     crud.update_groups()
#     crud.update_groups()
#     self.assertListEqual()

    
