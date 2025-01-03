class ScreenData():
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.game_title = 'Forest Maze Adventure'

class CharacterData():
    def __init__(self):
        self.front_image = "data\\images\\player_character\\player_character.png"
        self.right_image = "data\\images\\player_character\\player_character.png"
        self.back_image = "data\\images\\player_character\\player_character.png"
        self.left_image = "data\\images\\player_character\\player_character.png"

class HealthData():
    def __init__(self):
        self.maxHealth = 3
        self.health_image = "data\\images\\player_character\\heart.png"

class EnemyData():
    def __init__(self):
        self.enemy_image_1 = "data\\images\\monsters\\1_en.png"
        self.enemy_image_2 = "data\\images\\monsters\\2_en.png"
        self.enemy_image_3 = "data\\images\\monsters\\3_en.png"
        self.enemy_image_4 = "data\\images\\monsters\\4_en.png"
        self.enemy_image_5 = "data\\images\\monsters\\5_en.png"
        self.enemy_image_6 = "data\\images\\monsters\\6_en.png"
        self.enemy_image_7 = "data\\images\\monsters\\7_en.png"

class MazeData():
    def __init__(self):
        self.top_wall = "data\\images\\maze\\top_wall.png"
        self.top_right_wall = "data\\images\\maze\\top_right_wall.png"
        self.right_wall = "data\\images\\maze\\right_wall.png"
        self.bottom_right_wall = "data\\images\\maze\\bottom_right_wall.png"
        self.bottom_wall = "data\\images\\maze\\bottom_wall.png"
        self.bottom_left_wall = "data\\images\\maze\\bottom_left_wall.png"
        self.left_wall = "data\\images\\maze\\left_wall.png"
        self.top_left_wall = "data\\images\\maze\\top_left_wall.png"
        self.path_image = "data\\images\\maze\\path.png"
        self.inner_wall = "data\\images\\maze\\inner_wall.png"

        self.wall_image = "data\\images\\maze\\maze_wall.png"
        self.end_maze_image = "data\\images\\maze\\portal.png"  
        self.cell_size = 50

class StartScreenData():
    def __init__(self):
        self.new_button = "New Game"
        self.contiune_button = "Continue..."
        self.quit_button = "Exit"
        self.background_image = "data\\images\\bg\\StartScreen_Background.jpg"

class ColorData():
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.blue = (0, 0, 255)
        self.dark_blue = (0, 0, 128)
        self.red = (255, 0, 0)
        self.dark_red = (128, 0, 0)

class HeaderData():
    def __init__(self):
        self.height = 100
        self.width = 1270 

class HeaderQuestions():
    def __init__(self):
        self.addition_question = 'Get two numbers whose addition is : '
        self.subtraction_question = 'Get two numbers whose difference is : '
        self.multiplication_question = 'Get two numbers whose product is : '
        self.division_question = 'Get two numbers whose division is : '

class CollectiablesImages():
    def __init__(self):
        self.image = 'data\\images\\collectables\\collectable.png'

class AnimationImages():
    def __init__(self):
        self.apple_image = 'data\\images\\animation_fruits\\apple.PNG'

class MathOperationImages():
    def __init__(self):
        self.addition_image =  'data\\images\\math_symbols\\addition.png'
        self.subtraction_image = 'data\\images\\math_symbols\\subtraction.png'
        self.division_image = 'data\\images\\math_symbols\\division.png'
        self.multiplication_image = 'data\\images\\math_symbols\\multiplication.png'
        self.equals_image = 'data\\images\\math_symbols\\equals.png'