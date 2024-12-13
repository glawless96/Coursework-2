class HelpTexts:
    def __init__(self, operator, target_number, level, difficulty):
        self.operator = operator
        self.target_number = target_number
        self.level = level
        self.difficulty = difficulty
        self.helptext = self.get_start_screen_help_text()
    
    def get_start_screen_help_text(self):
        if self.operator == "+":
            return get_addition_help_text()
        elif self.operator == "-":
            return get_subtraction_help_text()
        elif self.operator == "*":
            return get_multiplication_help_text()
        elif self.operator == "/":
            return get_division_help_text()
        else:
            return         
    
def get_addition_help_text():
    help_text_messages = []
    help_text_messages.append("Addition means putting things together.")
    help_text_messages.append("It is represented by + symbol.")
    example = "Example : 2 + 3 = 5"
    helptext = HelpText("Addition (+)", help_text_messages, example)
    return helptext

def get_subtraction_help_text():
    help_text_messages = []
    help_text_messages.append("Subtraction means taking something away.")
    help_text_messages.append("It is represented by - symbol.")
    example = "Example : 5 - 3 = 2"
    helptext = HelpText("Subtraction (−)", help_text_messages, example)
    return helptext

def get_multiplication_help_text():
    help_text_messages = []
    help_text_messages.append("Multiplication means adding the same number many times.")
    help_text_messages.append("It is represented by x symbol.")
    example = "Example : 2 x 3 = 6"
    helptext = HelpText("Multiplication (×)", help_text_messages, example)
    return helptext

def get_division_help_text():
    help_text_messages = []
    help_text_messages.append("Division means sharing or splitting things into equal parts.")
    help_text_messages.append("It is represented by ÷ symbol.")
    example = "Example : 6 ÷ 3 = 2"
    helptext = HelpText("Division (÷)", help_text_messages, example)
    return helptext
    



class HelpText:
    def __init__(self, title, messages, examples):
        self.title = title
        self.messages = messages
        self.examples = examples