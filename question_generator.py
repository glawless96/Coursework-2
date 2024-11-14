# question.py
import random

class Question:
    def __init__(self):
        self.target_sum = 0
        self.num1 = 0
        self.num2 = 0
        self.slots = [(100, 200, "X"), (200, 200, "Y")]
    
    def generate_question(self, collected_numbers):
        print('random smaple ',collected_numbers)
        self.num1, self.num2 = random.sample(collected_numbers, 2)
        self.target_sum = self.num1 + self.num2
        print('target -sum ',self.target_sum)
        # Create slots to place numbers
        self.slots = [(100, 200, "X"), (200, 200, "Y")]

    def get_slots(self):
        return self.slots

    def set_slot_value(self, slot_index, value):
        self.slots[slot_index] = (self.slots[slot_index][0], self.slots[slot_index][1], value)

    def check_solution(self):
        try:
            x = int(self.slots[0][2]) if self.slots[0][2] != "X" else 0
            y = int(self.slots[1][2]) if self.slots[1][2] != "Y" else 0
            return x + y == self.target_sum
        except ValueError:
            return False
