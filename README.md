
# Forest of Formulas: Apprentice Alchemist Trial

Welcome to **Forest of Formulas**, a thrilling educational puzzle game where you step into the shoes of an apprentice alchemist! Test your mathematical and problem-solving skills to overcome magical challenges and prove your worth as an alchemist.

---

## 🧙 Game Premise

You are an apprentice alchemist who has ventured into the **Forest of Formulas**, a mystical place where numbers are the building blocks of life. To pass your final alchemy trial, you must:

1. **Collect Essence Numbers**: Gather the numerical essences hidden throughout the forest, guarded by mischievous creatures called **Number Snatchers**. 
2. **Create Magical Formulas**: Use the collected numbers to concoct formulas that summon enchanted plants and animals, which will help you progress.

Conquer all **four mathematical trials**—addition, subtraction, multiplication, and division—to escape the forest and become a full-fledged alchemist!

---

## 🎮 Gameplay Overview


### **Section 1: Collecting Numbers**
- Navigate the forest to collect **Essence Numbers** scattered across the terrain.
- **Number Snatchers** will chase and attempt to steal your numbers. Dodge them using skillful movement!
- You have limited time to gather all the numbers needed to proceed.

### **Section 2: Concocting Formulas**
- Drag and drop the collected numbers into an alchemical grid.
- Solve puzzles by forming the correct equations (e.g., 3 + 5 = 8) to create magical plants or animals.
- Use your creations to clear obstacles and advance to the next trial.

### **Progression**
- Levels become more challenging as you venture deeper into the forest.
- Successfully complete all four levels to escape the forest and earn the title of **Master Alchemist**!

---

## 📂 File Descriptions

### **Main Files**
- `game.py`: The primary game script. Run this file to start the game.

### **Data Folder**
- **`/data/`**: Houses all visual and audio assets.
  - `player_character/`: Contains character.
  - `monsters/`: Contains enemy.
  - `collectables/`: Contains items.
  - `bg/`: Background images for each level.
  - `sounds/`: Sound effects and background music for an immersive experience.

### **Game Logic Files**
- `player.py`: Implements core game mechanics, such as movement, number collection, and collision detection.
- `maze.py`: Handles the drag-and-drop formula-building system and checks for correct equations.
- `levels.py`: Defines the level structure, including objectives, enemy behavior, and progression logic.

### **Utilities**
- `button.py`: Provides helper functions for creating buttons.
- `static.py`: Provides functions to store the static data.

### **UI Files**
- `head_up_display.py`: Implements user interface components, such as score displays, timers, and level progress indicators.

---

## 🕹️ Controls

- **Arrow Keys/WASD**: Move the apprentice.
- **Mouse**: Drag and drop numbers to solve formulas.
- **Spacebar**: Pause the game.

---

## 💡 Tips for Success

1. **Time is of the essence**: Focus on collecting numbers quickly before time runs out!
2. **Plan your formulas**: Think ahead about the numbers you need for the alchemical grid.
3. **Avoid Number Snatchers**: Learn their movement patterns to dodge them effectively.

---

## 🚀 How to Play

1. Ensure you have **Python 3.x** and **Pygame** installed.
2. Download the game files and extract them to a folder.
3. Open a terminal/command prompt, navigate to the game folder, and run:
   ```bash
   python main.py
   ```
4. Enjoy the journey through the Forest of Formulas!

---

## 🛠️ Troubleshooting

- **Issue**: The game won't start.
  - **Solution**: Ensure Python and Pygame are installed. Run `pip install pygame` to install Pygame.
- **Issue**: Graphics or sounds are missing.
  - **Solution**: Verify the `assets/` folder is in the correct location and contains all necessary files.

---

Thank you for playing **Forest of Formulas**! We hope you enjoy your journey to becoming a Master Alchemist. 🌿✨
