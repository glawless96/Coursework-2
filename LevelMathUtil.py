import random

class LevelMathUtil:
    #AC1
    def set_level_difficulty():
        level = random.randint(1, 5)
        if level == 1:
             print("Difficulty level: Easy")
        elif level == 2:
             print("Difficulty level: Normal")
        elif level == 3:
            print("Difficulty level: Hard")
        elif level == 4:
            print("Difficulty level: Very Hard")
        elif level == 5:
            print("Difficulty level: Nightmare")
        return level

    #AC2
    def get_target_number(level):
        range = {1:{1:(2,3),2:(3,5),3:(4,6),4:(6,7),5:(7,9)},
                 2:{1:(10,13),2:(13,15),3:(15,20),4:(20,25),5:(25,30)},
                 3:{1:(30,33),2:(33,35),3:(35,40),4:(40,45),5:(45,50)},
                 4:{1:(50,53),2:(53,55),3:(55,60),4:(60,70),5:(70,80)},
                 5:{1:(80,83),2:(83,85),3:(85,90),4:(90,95),5:(95,100)},
        }
        difficulty = LevelMathUtil.set_level_difficulty()
        number_range = range[level][difficulty]
        return random.randint(number_range[0],number_range[1])

    #AC3
    def set_math_operator():
        operator = {1:"+",
                    2:"-",
                    3:"*",
                    4:"/",}
        operator_random = random.randint(1,4)
        return operator[operator_random]