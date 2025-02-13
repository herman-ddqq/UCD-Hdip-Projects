#!/usr/bin/env python
# coding: utf-8

# # Exercise One - Basic Creature Classes (2.5%)
# ## Task 1 - Class Creature and basic methods

# In[267]:


from random import randint
from termcolor import colored

class Creature:
    def __init__(self, name: str, max_hp: int = 10):
        self.name = name #passed as an argument
        self.max_hp=max_hp #by default = 10
        self.hp=max_hp #same as max_hp in the beginning
        self.abilities={"Attack": 1, "Defence": 5, "Speed": 5} #also default; dictionary

    #checks if HP negative, set it to 0 and says Creature died (fainted); othervise just returns new changed HP value
    def check_life(self):
        if self.hp<=0:
            self.hp=0
            print (colored(f"{self.name} fainted!", 'magenta'))
        return self.hp

    #ATTACK method (see comments)
    def attack(self, target):
        roll = randint(1, 20) #1) determines chance of sucessful attack by random roll first
        sum_defence_speed=target.abilities["Defence"] + target.abilities["Speed"]
        
        if roll < sum_defence_speed: #2) if roll (chance)<defense+speed of target, then attack is unsecessful
            print("Attack missed... ", end="")
            return False, target
        else: #3) else - determine attack "power" (ability Attack +random number 1 to 4)
            attack_roll = self.abilities["Attack"]+randint(1,4)
            target.hp -= attack_roll #4) deduct from HP
            print(f"Attack hits for {colored(attack_roll, 'yellow')} damage! ", end="")
            target.check_life() #5) UPDATE HP
            return True, target

    #auto selection of target from the list; HP should be > 0;othervise no target
    def auto_select(self, target_list):
        for target in target_list:
            if target.hp>0:
                return target
        return None

    #it uses previous method (auto_select) to select target and then calls attack method on target. (basically 2 in 1; old methods combined)
    def turn(self, round_num, target_list):
        target = self.auto_select(target_list)
        if target:
            return self.attack(target)
        return False, None

#my additional function to check if the whole team is dead (need for script)
def all_team_dead(team_list):
    for creature in team_list:
        if creature.hp>0:
            return False #false if at least 1 alive
    return True #by default returns true unleast some are alive


# ## first SCRIPT

# ## Task 2 - subclasses: Goblin, Orc, Warrior
# ## 1) Goblin

# In[269]:


class Goblin (Creature):
    def __init__ (self, name: str):
        super().__init__(name)
        self.max_hp = 15
        self.hp = self.max_hp
        self.abilities = {"Attack": 3, "Defence": 6, "Speed": 6} #goblin has different ablities


# ###class Goblin is subclass of parent (superclass) Creature, so it inherits methods (no need to write them again) and properties (like name, hp), except for the ones I owerwrite different for Goblin (it is max_hp 15 and self.ailities); 
# 
# ###same with Orc (below); BUT Orc has new methods special for him

# ## 2) Orc 

# In[270]:


class Orc(Creature):
    def __init__(self, name: str):
        super().__init__(name)  #orc has different max_hp = 50
        self.max_hp = 50
        self.hp = self.max_hp
        self.abilities = {"Attack": 5, "Defence": 8, "Speed": 3} #and different abilities
    
    #special methods for Orc (so it has inherited from Creature + his own methods)
    def heavy_attack(self, target): 
        if self.abilities["Attack"] == 5 and self.abilities["Defence"] == 8 and self.abilities["Speed"] == 3:
            self.abilities["Attack"] += 5
            self.abilities["Defence"] -= 3
            print(f"{colored(self.name, 'red')} is in rage.")
            
            #after I made changes to attack method, inherited the rest as normal from Creature
            successful_attack, target = super().attack(target)
            return successful_attack, target

    def attack(self, target):
        if self.abilities["Attack"] != 5 or self.abilities["Defence"] != 8:
            print(f"{colored(self.name, 'red')} cooled down!")
            self.abilities["Attack"] = 5
            self.abilities["Defence"] = 8
        return super().attack(target)
    
    def turn(self, round_num, target_list):
        target = self.auto_select(target_list)
        if target:
            if round_num % 4 == 0:
                return self.heavy_attack(target) #heavy every 4th round
            else:
                return self.attack(target) #rounds 1,2,3 - normal attack
        return False, None


# ###in turn method - still need to return False, None. Logically I have only 2 outcomes - attack successful or not (and it is included in attack method) but still need to return smth just to avoid mistakes
# 
# ###it was a bit hard to understand that I need to return not only the result of attack (True/False), but also target (hp updated); and where I need it (in custom method - heavy attack; and where no need- in attack method which is Superclass method, already has it)

# ## Battle script Goblin vs Orc (this time - function);
# ###testing Orc and Goblin here. I used existing SCRIPT from Task 1, just made  function out of it this time and modified a bit.
# 


# ## 3) Warrior 

# In[272]:


class Warrior(Creature):
    def __init__(self, name: str):
        super().__init__(name)
        self.max_hp = 50
        self.hp = self.max_hp
        self.abilities = {"Attack": 5, "Defence": 10, "Speed": 4}
        self.shield_up_ON = False #by default not uses shield

    def shield_up(self):
        if not self.shield_up_ON: #do not use this method if it's True (if it's already using shield)
            self.abilities["Attack"] -= 4
            self.abilities["Defence"] += 4
            self.shield_up_ON = True
            print(f"{colored(self.name, 'red')} takes a defensive stance.", end="")
    
    def shield_down(self):
        if self.shield_up_ON:#put down shield only if it was up
            self.abilities["Attack"] += 4
            self.abilities["Defence"] -= 4
            self.shield_up_ON = False
            print(f"{colored(self.name, 'red')}'s stance returns to normal.", end="")
    
    def turn(self, round_num, target_list):
        target = self.auto_select(target_list)
        if target:
            #ROUND1 - attack + shield_up
            if round_num % 4 == 1: 
                successful_attack, target = self.attack(target)
                self.shield_up()
                return successful_attack, target


            #ROUND 2,3 - only attack
            elif round_num % 4 == 2 or round_num % 4 == 3:  
                successful_attack, target = self.attack(target)
                return successful_attack, target

            #ROUND4 - shield_down + attack
            elif round_num % 4 == 0: 
                self.shield_down()
                successful_attack, target = self.attack(target)
                return successful_attack, target
        return False, None #or false if unsuccessfult attack



# ## Task 3 - Classes: Archer, Fighter


# In[274]:


class Archer(Creature):
    def __init__(self, name: str):
        super().__init__(name)
        self.max_hp = 30
        self.hp = self.max_hp
        self.abilities = {"Attack": 7, "Defence": 9, "Speed": 8}
        self.original_attack = 7
        self.original_defence = 9

    def power_shot(self, target):
        print(f"{colored(self.name, 'red')} shoots {colored(target.name, 'red')}...")
        

        roll_1 = randint(1, 20)
        roll_2 = randint(1, 20)
        attack_roll = max(roll_1, roll_2)
        
        #speed bonus
        if self.abilities["Speed"] > target.abilities["Speed"]:
            attack_roll += self.abilities["Speed"] - target.abilities["Speed"]
        
        #change if original values
        if self.abilities["Attack"] == self.original_attack:
            self.abilities["Attack"] += 3
            self.abilities["Defence"] -= 3
            print(f"{colored(self.name, 'red')}'s attack rises.")
            print(f"{colored(self.name, 'red')}'s defence reduced.")
        
        #check if attack worked
        sum_defence_speed = target.abilities["Defence"] + target.abilities["Speed"]
        if attack_roll >= sum_defence_speed:
            damage = randint(1, 8) + self.abilities["Attack"]
            print(f"Power shot hits for {colored(damage, 'yellow')} damage!")
            target.hp -= damage
            target.check_life()
            return True, target
        else:
            print("Power shot missed...")
            return False, target

    def attack(self, target):
        #reset to original if was modified
        if self.abilities["Attack"] != self.original_attack:
            print(f"{colored(self.name, 'red')} abilities return to normal.")
            self.abilities["Attack"] = self.original_attack
            self.abilities["Defence"] = self.original_defence
        return super().attack(target)

    def auto_select(self, target_list):
        alive_targets = [t for t in target_list if t.hp > 0]
        if not alive_targets:
            return None
        return min(alive_targets, key=lambda x: x.hp)

    def turn(self, round_num, target_list):
        target = self.auto_select(target_list)
        if target:
            if round_num % 4 == 1:
                print(f"{colored(self.name, 'red')} attacks {colored(target.name, 'red')}. ", end="")
                return self.attack(target)
            else:
                return self.power_shot(target)
        return False, None

class Fighter(Creature):
    def __init__(self, name: str):
        super().__init__(name, max_hp=50)
        self.abilities = {"Attack": 5, "Defence": 8, "Speed": 5}

    def auto_select(self, target_list):
        alive_targets = [t for t in target_list if t.hp > 0]
        if not alive_targets:
            return None
        return max(alive_targets, key=lambda x: x.hp)

    def turn(self, round_num, target_list):
        target = self.auto_select(target_list)
        if target:
            successful = False
            original_attack = self.abilities["Attack"]
            
            #first attack - normal
            print(f"{colored(self.name, 'red')} attacks {colored(target.name, 'red')}. ", end="")
            success, target = self.attack(target)
            successful = successful or success
            
            if target and target.hp > 0:
                print(f"{colored(self.name, 'red')}'s unleashes a flurry of strikes.")
                #next two attacks have -3 penalty
                self.abilities["Attack"] -= 3
                for _ in range(2):
                    if target and target.hp > 0:
                        target = self.auto_select(target_list)
                        if target:
                            print(f"{colored(self.name, 'red')} attacks {colored(target.name, 'red')}. ", end="")
                            success, target = self.attack(target)
                            successful = successful or success
            
            #reset attack
            self.abilities["Attack"] = original_attack
            return successful, target
        return False, None


# ## Archer vs Fighter

# In[275]:

# # Exercise Two - More complex enemies (2.5%)
# ## Task 1: OrcGeneral

# In[276]:


class OrcGeneral(Orc, Warrior):
    def __init__(self, name: str):
        Orc.__init__(self, name)
        self.max_hp = 80 
        self.hp = self.max_hp
        self.abilities = {"Attack": 5, "Defence": 8, "Speed": 3}
        self.shield_up_ON = False
        self.in_rage = False
    
    def attack(self, target):
        return super().attack(target)
    
    def heavy_attack(self, target):
        if target:
            print(f"{colored(self.name, 'red')} is in rage.")
            success, target = super().attack(target)
            return success, target
        return False, None
        
    def turn(self, round_num, target_list):
        target = self.auto_select(target_list)
        if not target:
            return False, None

        if round_num % 4 == 1:
            #round 1 - attack and shield up
            print(f"{colored(self.name, 'red')} attacks {colored(target.name, 'red')}. ", end="")
            success, target = self.attack(target)
            self.shield_up()
            return success, target
        
        elif round_num % 4 == 2:
            #round 2 - normal attack
            print(f"{colored(self.name, 'red')} attacks {colored(target.name, 'red')}. ", end="")
            return self.attack(target)
        
        elif round_num % 4 == 3:
            #round 3 shield down first, then attack
            self.shield_down()
            print(f"{colored(self.name, 'red')} attacks {colored(target.name, 'red')}. ", end="")
            return self.attack(target)
        
        else:  #round_num % 4 == 0
            #round 4 - Heavy attack
            print(f"{colored(self.name, 'red')} attacks {colored(target.name, 'red')}. ", end="")
            return self.heavy_attack(target)


# ## Task 2: GoblinKing

# In[277]:


class GoblinKing(Goblin, Archer):
    def __init__(self, name: str):
        Goblin.__init__(self, name)
        Archer.__init__(self, name)
        self.max_hp = 50
        self.hp = self.max_hp
        self.abilities = {"Attack": 3, "Defence": 6, "Speed": 6}

    def turn(self, round_num, target_list):
        return Archer.turn(self, round_num, target_list)


# ## Task 3:class Boss

# In[278]:


class Boss(Orc):
    def __init__(self, name: str):
        Orc.__init__(self, name)
        self.max_hp = 200
        self.hp = self.max_hp
        self.abilities = {"Attack": 5, "Defence": 8, "Speed": 5}

    def heavy_attack(self, target):
        if target:
            print(f"{colored(self.name, 'red')} is in rage.")
            success, target = super().attack(target)
            return success, target
        return False, None
    
    def auto_select(self, target_list, mode="Weak"):
        alive_targets = [t for t in target_list if t.hp > 0]
        if not alive_targets:
            return None
            
        if mode == "Weak":
            return min(alive_targets, key=lambda x: x.hp)
        elif mode == "Strong":
            return max(alive_targets, key=lambda x: x.hp)
        else:
            from random import choice
            return choice(alive_targets)
        
    def turn(self, round_num, target_list):
        if round_num == 1:
            #three attacks in round 1
            target = self.auto_select(target_list, "Weak")
            if target:
                print(f"{colored(self.name, 'red')} attacks {colored(target.name, 'red')}. ", end="")
                success1, _ = self.attack(target)
            
                #two random attacks
                for _ in range(2):
                    target = self.auto_select(target_list, "Random")
                    if target:
                        print(f"{colored(self.name, 'red')} attacks {colored(target.name, 'red')}. ", end="")
                        success2, target = self.attack(target)
                return success1 or success2, target
        else:
            #single heavy attack in rounds 2,3,4
            target = self.auto_select(target_list, "Strong")
            if target:
                print(f"{colored(self.name, 'red')} attacks {colored(target.name, 'red')}. ", end="")
                return self.heavy_attack(target)
        return False, None


# ## Boss vs OrcGeneral

# In[279]:

# # Exercise Three - The Wizard (1%)
# ## Task 1: Wizard Class
# 

# In[280]:


class Wizard(Creature):
    def __init__(self, name: str, max_hp: int = 20):
        super().__init__(name, max_hp)
        self.abilities = {"Attack": 3, "Defence": 5, "Speed": 5, "Arcana": 10}
        self.mana = 100

    def attack(self, target):
        print("Mana: +20!")
        print(f"{self.name} attacks {target.name}.")
        success, target = super().attack(target)
        self.mana = min(self.mana + 20, 100)
        if self.mana == 100:
            print("Mana is full")
        return success, target

    def recharge(self):
        print(f"{self.name} channels magical energy...")
        self.mana = min(self.mana + 30, 100)
        print("Mana: +30!")
        if self.mana == 100:
            print("Mana is full")

    def fire_bolt(self, target):
        if self.mana >= 15:
            self.mana -= 15
            print(f"{self.name} fires a fire bolt at {target.name}...")
            
            attack_roll = randint(1, 20) + (self.abilities["Arcana"] // 2)
            if attack_roll >= target.abilities["Defence"] + target.abilities["Speed"]:
                damage = randint(1, self.abilities["Arcana"])
                target.hp -= damage
                target.check_life()
                print(f"Fire bolt hits for {damage} fire damage!")
                
                self.mana = min(self.mana + 10, 100)
                if self.mana == 100:
                    print("Mana is full")
                return True, target
            else:
                print("Fire bolt missed...")
                return False, target
        else:
            print("Not enough mana for fire bolt!")
            return False, target

    def heal(self, target):
        if self.mana >= 20:
            self.mana -= 20
            print("Mana: -20")
            healing = randint(0, 8) + (self.abilities["Arcana"] // 2)
            old_hp = target.hp
            target.hp = min(target.hp + healing, target.max_hp)
            print(f"{self.name} heals {target.name} for {healing} HP!")
        else:
            print("Not enough mana to heal!")

    def mass_heal(self, allies):
        if self.mana >= 30:
            self.mana -= 30
            print("Mana: -30")
            for ally in allies:
                healing = randint(0, 10) + self.abilities["Arcana"]
                old_hp = ally.hp
                ally.hp = min(ally.hp + healing, ally.max_hp)
                print(f"{self.name} heals {ally.name} for {healing} HP!")
        else:
            print("Not enough mana for mass heal!")

    def fire_storm(self, enemies):
        if self.mana >= 50:
            self.mana -= 50
            print("Mana: -50")
            for enemy in enemies:
                attack_roll = randint(1, 20) + self.abilities["Speed"]
                damage = randint(5, 20) + self.abilities["Arcana"]
                if attack_roll < enemy.abilities["Defence"]:
                    damage //= 2
                enemy.hp -= damage
                enemy.check_life()
                print(f"Fire Storm deals {damage} fire damage to {enemy.name}!")
        else:
            print("Not enough mana for fire storm!")

    def select_target(self, target_list):
        while True:
            print("\nSelect target:")
            #show targets
            for i, target in enumerate(target_list, 1):
                print(f"{i}: {target.name}, HP: {target.hp}/{target.max_hp}")
            
            try:
                choice = input("Enter choice: ")
                choice_num = int(choice)
                if 1 <= choice_num <= len(target_list):
                    return target_list[choice_num - 1]
                else:
                    print("Invalid choice. Please enter a number between 1 and", len(target_list))
            except ValueError:
                print("Please enter a valid number!")


# # Exercise Four - Battle in the Middle Earth (4%)
# ## Task 1: Battle Class
# 

# In[282]:


class Battle:
    def __init__(self):
        
        #enemies
        self.enemies = [
            GoblinKing("Goblin King"),
            OrcGeneral("Orc General"),
            Goblin("Goblin"),
            Orc("Orc")
        ]
        
        #allies
        self.allies = [
            Fighter("Aragorn"),
            Archer("Legolas"),
            Warrior("Boromir"),
            Creature("Gollum")
        ]
        
        #wizard (PLAYER)
        self.wizard = Wizard("Gandalf")

        #boss
        self.boss = Boss("Boss")
        self.boss_appeared = False

    def check_boss_condition(self):
        alive_enemies = [e for e in self.enemies if e.hp > 0]
        if len(alive_enemies) == 1 and not self.boss_appeared:
            print(f"\n{colored('The BOSS is here and ready to fight!', 'red')}")
            self.enemies.append(self.boss)
            self.boss_appeared = True

    def start(self):
        round_num = 1
        
        while True:
            print(f"\n{colored(f'Round {round_num}:', 'blue')}")
            print("========================================================")

            
            all_creatures = []
            for creature in self.allies + self.enemies:
                if creature.hp > 0:
                    all_creatures.append(creature)
            
            all_creatures.sort(key=lambda x: x.abilities["Speed"], reverse=True)
            
            for creature in all_creatures:
                if creature.hp <= 0:
                    continue
                    
                if creature in self.allies:
                    targets = self.enemies
                else:
                    targets = self.allies
                
                success, target = creature.turn(round_num, targets)
                
                alive_enemies = [e for e in self.enemies if e.hp > 0]
                alive_allies = [a for a in self.allies if a.hp > 0]
                
                if not alive_enemies:
                    print(f"\n{colored('GOOD team wins!', 'green')}")
                    return
                    
                if not alive_allies:
                    print(f"\n{colored('EVIL team wins... (All allies are dead)', 'red')}")
                    return
                    
                if self.wizard.hp <= 0:
                    print(f"\n{colored('EVIL team wins... (The Wizard is dead)', 'red')}")
                    return
                
                self.check_boss_condition()
            
            print("\n========================================================")
            print(f"End of round {round_num}.")
            print("========================================================")
            round_num += 1



# ## Task 2: Player turn
# 

# In[284]:

def player_turn(wizard, allies, enemies):
    #player status
    print("========================================================")
    print(f"Player: {colored(wizard.name, 'green')} HP: {wizard.hp}/{wizard.max_hp} Mana: {wizard.mana}/100")
    
    #allies
    print("\nAllies:")
    for ally in allies:
        if ally.hp > 0:
            print(f"{colored(ally.name, 'green')} HP: {ally.hp}/{ally.max_hp}")
    print("========================================================")

    #menu
    print("\n========================================================")
    print("\nActions. ", end="")
    print("F: Attack ", end="")
    print("R: Recharge Mana", end="")
    print("\nSpells. ", end="")
    print("1: Heal ", end="")
    print("2: Firebolt ", end="")
    print("3: Mass Heal ", end="")
    print("4: Fire Storm ")
    print("\nTo Quit game type: Quit ", end="")
    print("========================================================")

    while True:
        try:
            action = input("\nEnter action: ").strip().lower()
            
            if action == 'quit':
                print("Exiting game")
                return True
            
            if action == 'f':
                living_enemies = [e for e in enemies if e.hp > 0]
                target = wizard.select_target(living_enemies)
                if target:
                    wizard.attack(target)
                    return False
                
            elif action == 'r':
                wizard.recharge()
                return False
                
            elif action == '1':  #heal
                living_allies = [a for a in allies + [wizard] if a.hp > 0]
                target = wizard.select_target(living_allies)
                if target:
                    wizard.heal(target)
                    return False
                
            elif action == '2':  #firebolt
                living_enemies = [e for e in enemies if e.hp > 0]
                target = wizard.select_target(living_enemies)
                if target:
                    wizard.fire_bolt(target)
                    return False
                
            elif action == '3':  #mass Heal
                living_allies = [a for a in allies if a.hp > 0]
                wizard.mass_heal(living_allies)
                return False
                
            elif action == '4':  #fire Storm
                living_enemies = [e for e in enemies if e.hp > 0]
                wizard.fire_storm(living_enemies)
                return False
                
            else:
                print("Invalid action. Please try again.")
                
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")

def final_battle():
    battle_instance = Battle()
    round_num = 1
    max_rounds = 20
    
    
    while round_num <= max_rounds:
        print(f"\n{colored(f'Round {round_num}:', 'blue')}")
        print("========================================================")
        
        #player turn
        if battle_instance.wizard.hp > 0:
            quit_game = player_turn(
                battle_instance.wizard, 
                [a for a in battle_instance.allies if a != battle_instance.wizard], 
                [e for e in battle_instance.enemies if e.hp > 0]
            )
            if quit_game:
                print("Player ended the game.")
                return
            
        #sort by speed
        all_creatures = []
        for creature in battle_instance.allies + battle_instance.enemies:
            if creature.hp > 0:
                all_creatures.append(creature)
        
        all_creatures.sort(key=lambda x: x.abilities["Speed"], reverse=True)
        
        #each creature's turn
        for creature in all_creatures:
            if creature.hp <= 0 or creature == battle_instance.wizard:
                continue
                
            #computer turn
            if creature in battle_instance.allies:
                targets = battle_instance.enemies
            else:
                targets = battle_instance.allies
            
            print(f"\n{colored(creature.name, 'green' if creature in battle_instance.allies else 'red')}'s turn:")
            success, target = creature.turn(round_num, targets)
    
        #check win/lose
        if all_team_dead(battle_instance.enemies):
            print(colored("\nGOOD team wins!", "green"))
            #reset
            battle_instance = Battle()
            round_num = 0
            
        elif all_team_dead(battle_instance.allies):
            print(colored("\nDefeat. (All allies are dead)", "red"))
            #reset
            battle_instance = Battle()
            round_num = 0
            
        elif battle_instance.wizard.hp <= 0:
            print(colored("\nDefeat. (The Wizard is dead)", "red"))
            #reset
            battle_instance = Battle()
            round_num = 0
        
        #boss here or no
        battle_instance.check_boss_condition()
        
        print("\n========================================================")
        print(f"End of round {round_num}.")
        print("========================================================")
        round_num += 1
    
    if round_num > max_rounds:
        print(colored("\nBattle ended in a draw (max rounds reached)", "yellow"))

final_battle()

### my problem - I forgot to include Wizard in the list of all creatures (who play) so his turn never came and game wasn't interactive
### if i understand correctly Player makes turn - allies make turn and then enemies make turn.

