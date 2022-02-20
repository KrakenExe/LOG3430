from ast import Break, For
# from asyncio.windows_events import NULL
from email_analyzer import EmailAnalyzer
from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from enum import Enum


N_MINOR_CLAUSE_COMBINATIONS = 8
N_CLAUSES = 4

# valeurs qui mettent la variable associée à vrai / faux dans les fonctions spam_classification (valeur à [0] = faux, [1] = vrai)
P_VALUES = [False,True]
H_VALUES = [25,15]
U_VALUES = [75,25]
G_VALUES = [25,75]
FALSE_INDEX = 0
TRUE_INDEX = 1

#index pour l'affichage du jeu de test
P_INDEX = 0
H_INDEX = 1
U_INDEX = 2
G_INDEX = 3



class Coverage_Type(Enum):
    CACC = 0
    GICC = 1

class Criteres:

    def spam_classification_1(self,P,H,U,G):
        H = True if H<20 else False
        U = True if U<50 else False
        G = True if G>=50 else False
        S = P and ((H and U) or (U and not G))
        return S

    def spam_classification_2(self,P,H,U,G):
        H = True if H<20 else False
        U = True if U<50 else False
        G = True if G>=50 else False
        S = P and H and U or P and U and not G
        return S

    def iterate_minor_clauses(self,coverage_type):

        test_set = []
        
        for i in range(N_CLAUSES):

            predicate_was_false = False
            predicate_was_true =  False

            for j in range(N_MINOR_CLAUSE_COMBINATIONS):
                entry_as_binary = int(bin(j),2)

                # permet d'obtenir les valeurs des bits en 1ere, 2eme et 3eme position dans entry_as_binary, qui représentent les entrées des 3 clauses mineures
                minor_clause_1 = (entry_as_binary >> 2) & 1 
                minor_clause_2 = (entry_as_binary >> 1) & 1
                minor_clause_3 = (entry_as_binary >> 0) & 1

                P_value_first_call = P_VALUES[FALSE_INDEX] if i==P_INDEX else P_VALUES[minor_clause_1]
                P_value_second_call = P_VALUES[TRUE_INDEX] if i==P_INDEX else P_VALUES[minor_clause_1]
                H_value_first_call = H_VALUES[TRUE_INDEX] if i==H_INDEX else (H_VALUES[minor_clause_1] if i==P_INDEX else H_VALUES[minor_clause_2])
                H_value_second_call = H_VALUES[FALSE_INDEX] if i==H_INDEX else (H_VALUES[minor_clause_1] if i==P_INDEX else H_VALUES[minor_clause_2])
                U_value_first_call = U_VALUES[FALSE_INDEX] if i==U_INDEX else (U_VALUES[minor_clause_3] if i==G_INDEX else U_VALUES[minor_clause_2]) 
                U_value_second_call = U_VALUES[TRUE_INDEX] if i==U_INDEX else (U_VALUES[minor_clause_3] if i==G_INDEX else U_VALUES[minor_clause_2])
                G_value_first_call = G_VALUES[FALSE_INDEX] if i==G_INDEX else U_VALUES[minor_clause_3]
                G_value_second_call = G_VALUES[TRUE_INDEX] if i==G_INDEX else U_VALUES[minor_clause_3]

                first_call_input = [P_value_first_call,H_value_first_call,U_value_first_call,G_value_first_call]
                second_call_input = [P_value_second_call,H_value_second_call,U_value_second_call,G_value_second_call]

                first_call_result = self.spam_classification_1(P_value_first_call,H_value_first_call,U_value_first_call,G_value_first_call)
                second_call_result = self.spam_classification_1(P_value_second_call,H_value_second_call,U_value_second_call,G_value_second_call)

                CACC_criteria_met = coverage_type==Coverage_Type.CACC and first_call_result != second_call_result
                GICC_criteria_met = coverage_type==Coverage_Type.GICC and first_call_result == second_call_result 

                if CACC_criteria_met and first_call_input not in test_set:
                    test_set.append(first_call_input)
                
                if CACC_criteria_met and second_call_input not in test_set:
                    test_set.append(second_call_input)

                

                if GICC_criteria_met and first_call_result and not predicate_was_true:

                    if first_call_input not in test_set:
                        test_set.append(first_call_input)

                    if second_call_input not in test_set:
                        test_set.append(second_call_input)

                    predicate_was_true = True

                if GICC_criteria_met and not first_call_result and not predicate_was_false:    

                    if first_call_input not in test_set:
                        test_set.append(first_call_input)

                    if second_call_input not in test_set:
                        test_set.append(second_call_input)

                    predicate_was_false = True

                if predicate_was_true and predicate_was_false or CACC_criteria_met:
                    break


    

        print("\njeu de test pour le critère {coverage}:\n".format(coverage=coverage_type.name))
        for i in range(len(test_set)):
            output = "d{index} = <(P={P}, H={H}, U={U}, G={G}),({result})>"
            S = self.spam_classification_1(test_set[i][P_INDEX],test_set[i][H_INDEX],test_set[i][U_INDEX],test_set[i][G_INDEX])
            print(output.format(index=i+1,P=test_set[i][P_INDEX],H=test_set[i][H_INDEX],U=test_set[i][U_INDEX],G=test_set[i][G_INDEX],result=S))
        print()


    def CACC(self):
        self.iterate_minor_clauses(Coverage_Type.CACC)

    def GICC(self):
        self.iterate_minor_clauses(Coverage_Type.GICC)
        print("\n#########################################################################\n")




    #######################
    #                     #
    #  Implémentation IC  #            
    #                     #
    #######################

    def print_test_set(self,test_set_IC, test_set_not_IC):
        print("Jeu de test qui satisfait le critère IC pour le prédicat S:")
        output = "d{index} = <(P={P}, H={H}, U={U}, G={G}), ({result})>"
        print(output.format(index=1, P=P_VALUES[test_set_IC[0]], H=H_VALUES[test_set_IC[1]], U=U_VALUES[test_set_IC[2]], G=G_VALUES[test_set_IC[3]], result=bool(test_set_IC[4])))
        print(output.format(index=2, P=P_VALUES[test_set_not_IC[0]], H=H_VALUES[test_set_not_IC[1]], U=U_VALUES[test_set_not_IC[2]], G=G_VALUES[test_set_not_IC[3]], result=bool(test_set_not_IC[4])))

    def replaceBooleanOps(self,expression):
        expression = expression.replace("and","&")
        expression = expression.replace("xor","^")
        expression = expression.replace("or","|")
        expression = expression.replace("not ","~")
        return expression

    def truth_table_S(self,expression):
        print("Expression DNF:")
        expression = expression.lower()
        implicants = [s.strip() for s in expression.split("or")]
        implicants_bitwise = [self.replaceBooleanOps(s) for s in implicants]
        implicants = [s.upper() for s in implicants]
        expression_bitwise = self.replaceBooleanOps(expression)
        test_set_IC = []
        if len(implicants) > 2:
            print(f" NOT S = {expression.upper()}")
            print("\nTable de vérité prédicat NOT S:")
            print("  -----------------------------------------------------")
            print(f"  | P | H | U | G | {implicants[0]} | {implicants[1]} | {implicants[2]} | S |")
            print("  -----------------------------------------------------")
            for p in range(0,2):
                for h in range(0,2):
                    for u in range(0,2):
                        for g in range(0,2):
                            s = eval(expression_bitwise) & 0x01
                            i1 = eval(implicants_bitwise[0]) & 0x01
                            i2 = eval(implicants_bitwise[1]) & 0x01
                            i3 = eval(implicants_bitwise[2]) & 0x01
                            if i1 & i2 & i3:
                                test_set_IC = [p, h, u, g, s]
                            print(f"  | {str(p)} | {str(h)} | {str(u)} | {str(g)} |   {str(i1)}   |       {str(i2)}       |   {str(i3)}   | {str(s)} |" )
                            print("  -----------------------------------------------------")
        else:   
            print(f" S = {expression.upper()}")
            print("\nTable de vérité prédicat S:")
            print("  -------------------------------------------------------------")
            print(f"  | P | H | U | G | {implicants[0]} | {implicants[1]} | S |")
            print("  -------------------------------------------------------------")
            for p in range(0,2):
                for h in range(0,2):
                    for u in range(0,2):
                        for g in range(0,2):
                            s = eval(expression_bitwise) & 0x01
                            i1 = eval(implicants_bitwise[0]) & 0x01
                            i2 = eval(implicants_bitwise[1]) & 0x01
                            if i1 & i2:
                                test_set_IC = [p, h, u, g, s]
                            print(f"  | {str(p)} | {str(h)} | {str(u)} | {str(g)} |        {str(i1)}        |          {str(i2)}          | {str(s)} |" )
                            print("  -------------------------------------------------------------")
    
        print("\n#########################################################################\n")
        return test_set_IC


    



