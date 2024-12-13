import random

class LevelMathUtil:
    # def __init__(self, level, difficulty):
    #     self.target_number = self.get_target_number(level, difficulty) 
           
    #AC2
    def get_target_number(self, level, difficulty):
        number_range = {
            1: {1: (2, 3), 2: (3, 4), 3: (5, 6), 4: (6, 7), 5: (7, 9), 6: (9, 11), 7: (11, 13), 8: (13, 15), 9: (15, 17), 10: (17, 20)}, # 0 - 20
            2: {1: (10, 13), 2: (13, 15), 3: (15, 20), 4: (20, 25), 5: (25, 30)},
            3: {1: (30, 33), 2: (33, 35), 3: (35, 40), 4: (40, 45), 5: (45, 50)},
            4: {1: (50, 53), 2: (53, 55), 3: (55, 60), 4: (60, 70), 5: (70, 80)},
            5: {1: (80, 83), 2: (83, 85), 3: (85, 90), 4: (90, 95), 5: (95, 100)},
        }
        
        number_range = number_range[level][difficulty]
        return random.randint(number_range[0], number_range[1])

    #AC3
    def set_math_operator(self, level, difficulty):
        operator = {
                        1: "+",
                        2: "-", 
                        3: "*", 
                        4: "/"
                    }

        if level == 1:
            if difficulty < 10:
                return "+"
            else:
                return operator[random.randint(1, 2)]
        elif level == 2:
            if difficulty < 6:
                return "+"
            elif difficulty < 12:
                return "-"
            else:
                return operator[random.randint(1, 3)]
        elif level == 3:
            if difficulty < 5:
                return "+"
            elif difficulty < 10:
                return "-"
            elif difficulty < 15:
                return "*"
            else:
                return operator[random.randint(1, 4)]
        else:
            return operator[random.randint(1, 4)]

    
    def get_addition_solutions_set(self, target_number):
        solutions = []
        for i in range(target_number + 1):
            result = target_number - i
            solutions.append(result)
            solutions.append(i)
        
        return solutions
            
        # def helper(target, current_combination, start, results):
        #     if target == 0:
        #         results.append(current_combination[:])
        #         return
        #     for i in range(start, target + 1):
        #         current_combination.append(i)
        #         helper(target - i, current_combination, i, results)
        #         current_combination.pop()
        
        # results = []
        # helper(target_number, [], 1, results)

        # unique_numbers = sorted({num for combination in results for num in combination})

        # return unique_numbers
    
    def get_subtraction_solution_set(self, target_number):
        solutions = []
        
        for i in range(1, target_number + 10):
            result = target_number - i
            solutions.append(i)
            solutions.append(result)
        
        return solutions
    
    def get_multiplication_solutions_set(self, target_number):
        solutions = []
        for i in range(1, int(target_number**0.5) + 1):
            if target_number % i == 0:
                solutions.append(i)
                solutions.append(target_number // i)
        return solutions
    
    def get_division_solutions_set(self, target_number):
        solutions = []
        for i in range(1, target_number + 1):
            if target_number % i == 0:
                solutions.append(i)
                solutions.append(target_number / i)
        
        return solutions
    
    def get_all_possible_solutions(self, target_number, operator):
        if operator == '+':
            return self.get_addition_solutions_set(target_number)
        elif operator == '-':
            return self.get_subtraction_solution_set(target_number)
        elif operator == '*':
            return self.get_multiplication_solutions_set(target_number)
        elif operator == '/':
            return self.get_division_solutions_set(target_number) 
        else:
            print('Default operator')
            return []
            
