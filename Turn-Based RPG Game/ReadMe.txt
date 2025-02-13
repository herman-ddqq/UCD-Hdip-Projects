# Turn-Based RPG Game

## Overview
This project is a **turn-based role-playing game (RPG)** implemented in Python, following Object-Oriented Programming (OOP) principles. The game includes different creatures, each with unique abilities and battle strategies. Players can engage in strategic combat using attack moves, special abilities, and magic.

## Features
- **Multiple Creature Classes**
  - `Creature` (Base class for all creatures)
  - `Goblin`, `Orc`, `Warrior`, `Archer`, `Fighter`, `Wizard`, etc.
- **Battle Mechanics**
  - Turn-based combat system with attack rolls and damage calculations
  - Unique battle strategies for different classes
  - Randomized attack success and damage values
- **Player-Controlled Wizard**
  - Casts spells like **Firebolt**, **Heal**, **Fire Storm**, etc.
  - Manages **Mana Points (MP)**
  - Selects targets for attacks and healing
- **AI-Controlled Enemies**
  - `Orc General`, `Goblin King`, `Boss` with unique attack patterns
  - Adaptive targeting and attack strategies
- **Dynamic Battle System**
  - Speed-based turn order
  - Health monitoring and auto-removal of defeated characters
  - Strategic use of attack, defense, and special abilities

## Installation & Execution
### Prerequisites
- Python 3.x
- Jupyter Notebook (for development and testing)
- Required libraries: `random`, `matplotlib`, `termcolor`

### Running the Game
```bash
python game.py
```
Or, if using Jupyter Notebook:
```python
%run game.py
```
### Controls & Gameplay
1. Start the game and view your **Wizard's stats** (HP, MP, Spells).
2. Choose an **action** each turn:
   - **Attack (F)**: Standard attack
   - **Recharge Mana (R)**: Restores MP
   - **Spells**:
     - (1) Heal
     - (2) Firebolt
     - (3) Mass Heal
     - (4) Fire Storm
3. Select a **target** (ally or enemy) when using spells or attacks.
4. The game continues until **all enemies or all allies are defeated**.
5. Option to **quit** anytime.

## Software Design
- Uses **Object-Oriented Programming (OOP)**
  - Inheritance for different creature types
  - Encapsulation for attributes and abilities
- **Modular Code Structure**
  - Separate Python files for each class
  - Functions for attack rolls, damage calculations, and UI prompts
- **Error Handling & Input Validation**
  - Prevents invalid moves and ensures smooth gameplay

## Future Improvements
- More creature classes and abilities
- Enhanced AI with better attack decision-making
- Additional spells and abilities for the Wizard

---
Developed by Herman Dolhyi as part of **UCD HDip in Computer Science** coursework.

