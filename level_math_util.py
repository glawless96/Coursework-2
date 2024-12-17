import random

class LevelMathUtil:
    def get_target_number(self, level, difficulty):
        number_ranges = {
            1: {  # Level 1: Numbers from 1 to 20
                i: (1 + (i - 1) * 1, 1 + i) for i in range(1, 21)  # Difficulty 1 to 20
            },
            2: {  # Level 2: Numbers from 10 to 50
                i: (10 + (i - 1) * 2, 10 + i * 2) for i in range(1, 21)  # Difficulty 1 to 20
            },
            3: {  # Level 3: Numbers from 30 to 100
                i: (30 + (i - 1) * 3, 30 + i * 3) for i in range(1, 21)  # Difficulty 1 to 20
            },
            4: {  # Level 4: Numbers from 50 to 150
                i: (50 + (i - 1) * 5, 50 + i * 5) for i in range(1, 21)  # Difficulty 1 to 20
            },
            5: {  # Level 5: Numbers from 80 to 200
                i: (80 + (i - 1) * 6, 80 + i * 6) for i in range(1, 21)  # Difficulty 1 to 20
            },
            6: {  # Level 6: Numbers from 100 to 300
                i: (100 + (i - 1) * 10, 100 + i * 10) for i in range(1, 21)  # Difficulty 1 to 20
            }
        }
        print('math utils level',level)
        print('math utils difficulty',difficulty)
        print('math utils number_ranges',number_ranges[level][difficulty])
        range_start, range_end = number_ranges[level][difficulty]
        return random.randint(range_start, range_end)

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
            
