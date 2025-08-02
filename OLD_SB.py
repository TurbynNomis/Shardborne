import os
import random

element_chart = {
    "Water": {"strong_against": ["Fire", "Earth"], "weak_against": ["Air", "Ice"]},
    "Fire": {"strong_against": ["Ice", "Metal"], "weak_against": ["Water", "Earth"]},
    "Earth": {"strong_against": ["Fire", "Metal"], "weak_against": ["Water", "Air"]},
    "Air": {"strong_against": ["Earth", "Ice"], "weak_against": ["Metal", "Fire"]},
    "Light": {"strong_against": ["Darkness"], "weak_against": []},
    "Darkness": {"strong_against": ["Light"], "weak_against": []},
    "Metal": {"strong_against": ["Air", "Ice"], "weak_against": ["Fire", "Earth"]},
    "Ice": {"strong_against": ["Water", "Air"], "weak_against": ["Fire", "Metal"]},
}

class Element:
    def __init__(self, name, damage_multiplier, crit_chance_modifier):
        self.name = name
        self.damage_multiplier = damage_multiplier
        self.crit_chance_modifier = crit_chance_modifier

    def get_elemental_advantage(self, opponent_element):
        if opponent_element.name in element_chart[self.name]["strong_against"]:
            return 1.25
        elif opponent_element.name in element_chart[self.name]["weak_against"]:
            return 0.75
        return 1

elements = [
    Element("Water", 1, 0.05),
    Element("Fire", 1, 0.1),
    Element("Earth", 1, 0.05),
    Element("Air", 1, 0.1),
    Element("Light", 1, 0.15),
    Element("Darkness", 1, 0.15),
    Element("Metal", 1, 0.05),
    Element("Ice", 1, 0.1)
]


class Weapon:
    def __init__(self, name, damage_range, crit_chance, crit_multiplier, element, parry_chance=0.3):
        self.name = name
        self.damage_range = damage_range
        self.crit_chance = crit_chance + element.crit_chance_modifier
        self.crit_multiplier = crit_multiplier
        self.element = element
        self.parry_chance = parry_chance

    def get_damage(self, opponent_element):
        base_damage = random.randint(*self.damage_range)
        if random.random() < self.crit_chance:
            print(f"Critical hit with {self.element.name} element!")
            base_damage *= self.crit_multiplier
        elemental_advantage = self.element.get_elemental_advantage(opponent_element)
        return base_damage * elemental_advantage * self.element.damage_multiplier
       
class ShopItem:
    def __init__(self, name, base_cost, description, apply_effect, stock=1):
        self.name = name
        self.base_cost = base_cost
        self.description = description
        self.apply_effect = apply_effect
        self.stock = stock
       
    @property
    def cost(self):
        level_factor = 1
        return int(self.base_cost * level_factor)
   
    @staticmethod    
    def get_random_shop_items(player_level):
        item_library = [
            ShopItem("REJUVENATION SPELL", 40, f"\n{'-'*10}\nAn arcane spell that is lost for eternity, once forged by a Priest a long time ago, the spell soon became forgotten by it scarcity. Legends say that it makes the one who reads younger, and thy wounds would close. \n(restores full HP)\n{'='*20}\n", lambda player: setattr(player, 'hp', min(player.max_hp, player.hp + 1000000)), stock=2),
            ShopItem("THE WISE MASTER'S BLESSING", 35, f"\n{'-'*10}\nOnce the Magic waters of the Wise Master touch pilgrims skins, they would have awakened in their vision towards elements and have their full potential to use their bodies as source of energy for supernatural powers of nature. \n(restores full Mana)\n{'='*20}\n", lambda player: setattr(player, 'mana', min(player.max_mana, player.mana + 1000000)), stock=2),
            ShopItem("BERSERK'S MOTIVATION", 55, f"\n{'-'*10}\nAn aura which is given by words of a Wise Man, the ones chosen to receive the motivation shall receive a piece of the power of those who use their strength against the evil in the world. The chosen ones shall be responsible with the discerniment to do the good instead of evil. \n(Increases damage by 5)\n{'-'*20}\n", lambda player: setattr(player.weapon, 'damage_range', (player.weapon.damage_range[0] + 5, player.weapon.damage_range[1] + 5)), stock=2),
            ShopItem("WARRIOR'S KNOWLEDGE", 45, f"\n{'-'*10}\nA autobiography of an old warrior which participated of The Great War, the warrior passes his strategies and some of the art to battle, giving knowledge to battle counter enemies and know their weak spots. \n(Increases critical damage chance by 5%)\n{'='*20}\n", lambda player: setattr(player.weapon, 'crit_chance', (player.weapon.crit_chance + 0.05)), stock=2),
            ShopItem("PERSONAL REPORT OF THE KING'S GUARD", 45, f"\n{'-'*10}\nOne of the journals of the King's personal guard. He was a skillful shieldman, in his books he has shown his battles to protect the king and strategies to use any weapon as a skillful shield with ability and class. \n(Increases parry chance by 5%)\n{'='*20}\n", lambda player: setattr(player.weapon, 'parry_chance', (player.weapon.parry_chance + 0.05)), stock=2),
            ShopItem("ARSENAL SHIFTER", 50, f"\n{'-'*10}\nA mysterious rune which seems to behave weird when approached to any weapon. Arcane books say that the rune does have abilities to identify weapons and change the form of the weapon to anything that it wants. \n(Rerolls weapon)\n{'='*20}\n", lambda player: setattr(player, 'weapon', (player.choose_random_weapon())), stock=1),
            ShopItem("ELEMENT SHIFTER", 50, f"\n{'-'*10}\nA rune which cannot be touched with proper ways. It is very unstable when interacted with anything which is alive, it can flush a strange power where it overflows the nature of the ones who touch it, and changes it to the nature that the rune wants. \n(Rerolls element)\n{'='*20}\n", lambda player: setattr(player, 'element', (random.choice(elements))), stock=1),
            ShopItem("SHARD OF THE TITAN'S CORE", 75, f"\n{'-'*10}\nMade from an unknown source, a core of a titan promises eternal life to anyone who possesses them. Titans were extremely dangerous fighters in The Great War. They would destroy kingdoms in stomps if they were not stopped by sorcerers of the time. When a Titan dies, its core explodes with a radius of kilometers, destroying everything on its way. mostly of the shards end up being destroyed by the power of the explosion, which is why makes it so rare.\n(Increases maximum health by 20%)\n{'='*20}\n", lambda player: setattr(player, 'max_hp', int(player.max_hp * 1.2)), stock=1),
            ShopItem("ESSENCE OF THE MOON", 60, f"\n{'-'*10}\nCollected from small dusts that fall over from the sky every millenium. The dust, if treated right, can have the extremely powerful liquid which maximizes the body of anyone who consumes its contact with their nature. People who drak the essence felt like they were transcending to another level of connection with their nature.\n(Increases maximum health by 20%)\n{'='*20}\n", lambda player: setattr(player, 'max_mana', int(player.max_mana * 1.35)), stock=1)
        ]
       
        return random.sample(item_library, 5)
   
    @staticmethod
    def shop(player):
        clear_screen()
        print(f"{'='*20}\nWelcome to the Shop, feel free to look around and buy what you need for your journey!\n{'='*20}\n")
        items_for_sale = ShopItem.get_random_shop_items(player.level)
       
        while True:
            for i, item in enumerate(items_for_sale):
                print(f"{i+1}. {item.name} - {item.cost} Coins || Stock: {item.stock} {item.description}")
            print(f"6. Exit Shop\n")
           
            print(f"{'='*20}\nYour Coins: {player.coins}\nYour HP: {player.hp}/{player.max_hp} || Your mana: {player.mana}/{player.max_mana}\nYour weapon: {player.weapon.name} || Your element: {player.element.name}\n{'='*20}\n")
            choice = input("Select an item to buy (1-5) or 6 to leave: ")
           
            if choice.isdigit() and 1 <= int(choice) <= 5:
                selected_item = items_for_sale[int(choice)-1]
                if player.coins >= selected_item.cost:
                    if selected_item.stock > 0:
                        player.coins -= selected_item.cost
                        selected_item.apply_effect(player)
                        selected_item.stock -= 1
                        print(f"You purchased {selected_item.name}!")
                    else:
                        print("Sory, this item is out of stock...")
                        print()
                else:
                    print("Not enough coins to buy!")
                    print()
            elif choice == "6":
                break
            else:
                print("Invalid choice, select a valid option.")
                print()

class Player:
    def __init__(self, max_hp, max_mana):
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mana = max_mana
        self.mana = max_mana
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 100
        self.coins = 0
        self.element = random.choice(elements)
        self.weapon = self.choose_random_weapon()
        self.has_parried = False

    def choose_random_weapon(self):
        weapons = [
            Weapon("Sword", (10, 20), 0.1, 2, self.element, parry_chance=0.25),
            Weapon("Axe", (15, 25), 0.15, 1.5, self.element, parry_chance=0.25),
            Weapon("Spear", (5, 20), 0.3, 1.75, self.element, parry_chance=0.30),
            Weapon("Shield", (5, 10), 0.1, 1.5, self.element, parry_chance=0.55),
            Weapon("Bow", (10, 20), 0.25, 1.25, self.element, parry_chance=0.15),
            Weapon("Daggers", (5, 15), 0.3, 1.5, self.element, parry_chance=0.15),
            Weapon("Battle axe", (15, 25), 0.15, 2, self.element, parry_chance=0.35),
            Weapon("Great sword", (15, 25), 0.1, 2.5, self.element, parry_chance=0.35),
            Weapon("War Hammer", (15, 25), 0.15, 1.5, self.element, parry_chance=0.35),
            Weapon("Short sword", (10, 20), 0.15, 2, self.element, parry_chance=0.15),
            Weapon("Mace", (5, 15), 0.2, 1.75, self.element, parry_chance=0.25)
        ]
        return random.choice(weapons)
       
    def take_damage(self, damage_amount, enemy):
        elemental_modifier = enemy.element.get_elemental_advantage(self.element)
        final_damage = damage_amount * elemental_modifier
        self.hp = max(0, self.hp - final_damage)
        print(f"You took {final_damage:.2f} damage from {enemy.name}. Current HP: {self.hp}/{self.max_hp}")
        if self.hp == 0:
            print("Player has been defeated!")

    def heal(self):
        if random.random() < 0.75:
            heal_amount = int(self.max_hp * 0.35)
            self.hp = min(self.max_hp, self.hp + heal_amount)
            print(f"Healing attempt Successful!")
            print(f"You healed {heal_amount} HP. Current HP: {self.hp}/{self.max_hp}")
        else:
            print(f"Healing attempt failed.")

    def regenerate_hp_and_mana(self, hp_regen_percentage=None, mana_regen_percentage=None):
        if hp_regen_percentage is None:
            hp_regen_percentage = max(0.10, 0.80 - (0.10 * (self.level - 1)))
        hp_regen_amount = int(self.max_hp * hp_regen_percentage)
        self.hp = min(self.max_hp, self.hp + hp_regen_amount)
        print(f"Regenerated {hp_regen_amount} HP. Current HP: {self.hp}/{self.max_hp}")
        if mana_regen_percentage is None:
            mana_regen_percentage = max(0.10, 0.50 - (0.05 * (self.level - 1)))
        mana_regen_amount = int(self.max_mana * mana_regen_percentage)
        self.mana = min(self.max_mana, self.mana + mana_regen_amount)
        print(f"Regenerated {mana_regen_amount} Mana. Current Mana: {self.mana}/{self.max_mana}")

    def gain_xp(self, xp_amount):
        self.xp += xp_amount
        print(f"Gained {xp_amount} XP. Current XP: {self.xp}/{self.xp_to_next_level}")
        if self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp = int(self.max_hp * 1.25)
        self.max_mana = int(self.max_mana * 1.25)
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        print(f"Level up! You are now level {self.level}. Max HP: {self.max_hp}, Max Mana: {self.max_mana}")
        ShopItem.shop(self)

    def attack(self, enemy_element):
        base_damage = random.randint(*self.weapon.damage_range)
        if random.random() < self.weapon.crit_chance:
            print(f"Critical hit!")
            base_damage *= self.weapon.crit_multiplier
        elemental_modifier = self.element.get_elemental_advantage(enemy_element)
        total_damage = base_damage * elemental_modifier * self.weapon.element.damage_multiplier
        return total_damage
       
    def parry(self):
        if self.has_parried:
            print("You already attempted to parry this turn!")
            return False
       
        if self.weapon.name == "Shield":
            mana_cost = 5
        else:
            mana_cost = 10
        if self.mana < mana_cost:
            print("Not enough mana to parry!")
            print()
            return False
       
        self.mana -= mana_cost
        self.has_parried = True
        parry_sucess = random.random() < self.weapon.parry_chance
        if parry_sucess:
            print(f"Parry successful! You blocked the enemy's attack using {self.weapon.name}.")
            print()
            return True
        else:
            print(f"Parry failed! You did not block the enemy's attack")
            print()
           
class Enemy:
   
    def __init__(self, name, hp, element, coin_loot_range):
        self.name = name
        self.hp = hp
        self.base_hp = hp
        self.element = element
        self.coin_loot_range = coin_loot_range

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        print(f"{self.name} took {damage:.2f} damage. Current HP: {self.hp}/{self.base_hp}")

def create_random_enemy(player_level, modifiers):
    base_hp = random.randint(30, 60) + (player_level * 10) * modifiers["enemy_strength"]
   
    coin_loot_range = (random.randint(5, 15), random.randint(16, 30))

    enemy_names = ["Goblin", "Slime", "Cristal Wisp", "Dark Creature", "Cursed Tree", "Corrupted Pilgrim", "Necromancer", "Cyphon", "Death's Servant"]
    name = random.choice(enemy_names)

    element = random.choice(elements)

    return Enemy(name=name, hp=base_hp, element=element, coin_loot_range=coin_loot_range)

def player_attack(player, enemy):
        base_damage = random.randint(*player.weapon.damage_range)
        element_advantage = player.element.get_elemental_advantage(enemy.element)
        total_damage = base_damage * element_advantage * player.element.damage_multiplier
        return total_damage
   
def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
   
def handle_victory(player, enemy, score):
    xp_gained = enemy.base_hp // 2
    player.gain_xp(xp_gained)
    coins_found = random.randint(*enemy.coin_loot_range)
    player.coins += coins_found
    print(f"You defeated {enemy.name}!")
    print(f"Gained {xp_gained} XP and found {coins_found} coins!")
    print(f"{'-'*20}")

def cast_magic_action(player, enemy):
    magic_cost = 10
    if player.mana >= magic_cost:
        damage = calculate_magic_damage(player)
        enemy.take_damage(damage)
        player.mana -= magic_cost
        print(f"You cast {player.element.name} magic and dealt {damage:.2f} damage to {enemy.name}!")
    else:
        print("Not enough magic points!")
        print(f"{'-'*20}")
       
def enemy_turn(player, enemy, modifiers):
    base_damage = random.randint(5, 15) * modifiers["enemy_strength"]
    elemental_advantage = enemy.element.get_elemental_advantage(player.element)
    total_damage = base_damage * elemental_advantage

    if not player.has_parried:
        parry_choice = input("Do you want to parry the enemy's attack? (Costs 10 mana; 5 if Shield. || Yes/no): ").lower()
        clear_screen()
        if parry_choice == "yes" and player.parry():
            return

    player.take_damage(total_damage, enemy)

def calculate_magic_damage(player):
    base_damage = random.randint(15, 30) + int(player.level * 1.2)
    damage_multiplier = player.element.damage_multiplier
    return base_damage * damage_multiplier
   
def attempt_flee(player, score):
    flee_chance = 0.25
    if random.random() < flee_chance:
        print("You successfully fled the battle!")
        player.regenerate_hp_and_mana()
        print(f"You lost 1 point of score for fleeing. Current score: {score}")
        return True, score - 1
    else:
        print("Flee attempt failed! The enemy gets a turn.")
        return False, score
       
def main_menu():
    while True:
        print("\nWelcome to the Game!\n")
        print(f"{'-'*20}")
        print('Version: 0.6.3: "Shopping the Strategy" Update')
        print('press "3" for more info about the Update!')
        print(f"{'-'*20}")
        print("1. Start Game")
        print("2. Exit")
        print("3. Update history")
        print("4. Future updates")

        choice = input("Enter your choice (1, 2, 3, or 4): ")
       
        if choice == "1":
            difficulty = choose_difficulty()
            start_game(difficulty)
        elif choice == "2":
            clear_screen()
            print("Thanks for playing!")
            break
        elif choice == "3":
            show_update_history()
        elif choice == "4":
            show_future_updates()
        else:
            print("Invalid choice, please try again.")

difficulty_levels = {
    "Training": {"enemy_strength": 0.5, "player_regen": 0.15},
    "Odyssey": {"enemy_strength": 1.0, "player_regen": 0.10},
    "Arena": {"enemy_strength": 1.5, "player_regen": 0.05},
    "Bounty Hunt": {"enemy_strength": 1.75, "player_regen": 0.05},
    "War": {"enemy_strength": 2.0, "player_regen": 0.03},
}

def choose_difficulty():
    clear_screen()  
    print("\nSelect a difficulty level:\n")
    print(f"1. TRAINING\n**A small forest for starters, where the enemies are under certain control of the kingdom. Great for training and skill development towards strategies.**\n-- 50% weaker enemies than usual, 15% of HP regen per battle\n\n{'='*10}\n")
    print(f"2. ODYSSEY\n**An adventure out of the kingdom bounds. Where adventurers may experience battles and discover legends from the outside**\n--Usual enemy strength, 10% of HP regen per battle\n\n{'='*10}\n")
    print(f"3. ARENA\n**A famous area for villagers in the Kingdom, where brave warriors join battles and fight enemies that were captured from the wild woods and trained for public battle entretainment.**\n--50% stronger enemies than usual, 5% of HP regen per battle\n\n{'='*10}\n")
    print(f"4. BOUNTY HUNT\n**Where Warriors accept the challenge to take offers and go in the hunt for the most dangerous enemies close to the kingdom surroundings. Warriors may jeopardize their lives into high skilled fights with strategy and well knowing actions for better fights**\n--75% stronger enemies than usual, 5% of HP regen per battle\n\n{'='*10}\n")
    print(f"5. WAR\n**The peace in the world collapses, kingdoms and outsiders are all at war against each other. All fighters are fully equipped and prepared. Warriors must have the finest art of war to battle against their enemies and survive the chaotic lands of doom**\n--100% stronger enemies than usual, 3% of HP regen per Battle\n\n{'='*10}\n")
   
    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        return "Training"
    elif choice == "2":
        return "Odyssey"
    elif choice == "3":
        return "Arena"
    elif choice == "4":
        return "Bounty Hunt"
    elif choice == "5":
        return "War"
    else:
        print("Invalid choice, defaulting to Normal.")
        return "Normal"
       
def print_status(player, enemy, score, difficulty):
    print(f"Difficulty: {difficulty}")
    print(f"Score: {score}\n{'-'*20}")
    print(f"Player HP: {player.hp}/{player.max_hp} | Mana: {player.mana}/{player.max_mana} | Level: {player.level} | XP: {player.xp}/{player.xp_to_next_level} | Coins: {player.coins}")
    print(f"Player Weapon: {player.weapon.name} (Parry Chance: {player.weapon.parry_chance * 100:.2f}%) | Element: {player.element.name}")
    print(f"Enemy: {enemy.name} | HP: {enemy.hp}/{enemy.base_hp} | Element: {enemy.element.name}")
    print(f"{'-'*20}")

def start_game(difficulty):
    modifiers = difficulty_levels[difficulty]
    player = Player(max_hp=100, max_mana=50)
    score = 0

    while player.hp > 0:
        clear_screen()
        enemy = create_random_enemy(player.level, modifiers)
        print(f"A {enemy.name} appears with {enemy.hp} HP and {enemy.element.name} element!")
        print(f"{'-'*20}")

        while enemy.hp > 0 and player.hp > 0:
            player.has_parried = False
            print_status(player, enemy, score, difficulty)
            print("\nChoose your action:")
            print("1. Attack")
            print("2. Cast Magic")
            print("3. Heal")
            print("4. Flee")

            action = input("Enter your choice (1, 2, 3, or 4): ")
            print()
            print()
            clear_screen()
            print_status(player, enemy, score, difficulty)
            print()
           
            if action == "1":
                damage = player.attack(enemy.element)
                enemy.take_damage(damage)
                print(f"You dealt {damage:.2f} damage to {enemy.name}!")
            elif action == "2":
                cast_magic_action(player, enemy)
            elif action == "3":
                player.heal()
            elif action == "4":
                flee_sucess, score = attempt_flee(player, score)
                if flee_sucess:
                    input("Press Enter to continue")
                    break
            else:
                print("Invalid action. Try again.")
           
            if enemy.hp > 0:
                enemy_turn(player, enemy, modifiers)
                print(f"{'-'*20}")

        if player.hp > 0 and action != "4":
            score += 1
            handle_victory(player, enemy, score)
            player.regenerate_hp_and_mana(modifiers["player_regen"])
   
    print()
    print(f"Game Over! Final Score: {score}")
    print("""
   
    """)

def show_update_history():
    clear_screen()
    print("""
    **0.1 - Base Game**
    - Creation of the game base
   
    0.1.1 -
    - Creation of magic, elements, weapons, and enemies
   
    0.1.2
    - Temporary removal of magics and elements for code debugging
   
    0.1.3
    - Loop system creation for survival
    - level, and XP system added
   
    0.1.4
    - Player can take elemental damage from enemies
    - Enemies get more difficult each player level
   
    0.1.5
    - Magic and XP system fully restored
    - Coin System usage in development
   
    0.1.6
    - Update history created
    - code cleaned up
   
    **0.2 - "The Magic update"**
    - Minor bug fixes
    - tweaks to magical damage
   
    0.2.2
    - Fixed damage clone issue with magic attacks
   
    **0.3 - "Clean Up" Update**
    - Major bugs fixes, not much changes in actual gameplay
   
    **0.4 - "Hero Path" Update**
    - creation of difficulty for levels, play at the difficulty you want!
    - Player regen per battle transition tweaked
    - print action smoothed for read
    - now screen refreshes every time you defeat an enemy for better read
    - UI changed, and max HP for enemy bug fix
   
    0.4.6
    - version 0.4 tweak
    - removal of main sources of bugs and created new commands
    - new method for enemy display
    - player damage buff
    - player heal buff (75% of chance to heal instead of 60%)
   
    **0.5 - "Fight Or Flight" Update**
    - creation of parry system
    - added mana regen when entering a new battle (Normal regen is 50% of the max amount)
    - creation of flee system (25% of chance to flee from the enemy, players will skip it and lose a point)
    - added new weapons (spear, shield, bow, short sword, great sword, Battle axe, war hammer, daggers, spear)
    - added new enemies
    - UI patch (now you can see the parry chance of the weapon that you have)
   
    0.5.1
    - Creation of names to the updates
   
    0.5.2
    - minor elemental damage fix
   
    **0.5.6 Healing Patch**
    - When healing is successful, 35% of their max HP is healed
    - Code cleanup
    - Screen Refresh system somewhat changed, you can see the UI during the transition to other screens
   
    **0.6 - "Shopping the Strategy" Update**
    - Creation of the Shop (every level up you will access the shop and will be able to buy many things as your money can pay). Make your strategy!
   
    0.6.1
    - Correction of several minor bugs and errors of previous updates
   
    **0.6.2 - "Unique Colors" patch**
    - Personification of most display actions (Shop items and difficulty choice)
    - more complex print commands
   
    0.6.3
    - correction of other minor bugs
    - correction of damage calculation and display system
    """)
    print()
    main_menu()

def show_future_updates():
    clear_screen()
    print("""
    0.7 - "Bright Path" Update
    - creation of portfolios for the game in general and its versions (starting from 0.6)
   
    0.8 - "Heavy weight" Update
    - Weapon speed mechanic
   
    0.9 - "Around the World" Update
    - Locations
    - specific enemies in locations
   
    0.10 - "Better go Fast!" Update
    - chance of hit and miss attacks
    - shop tweak
   
    0.11 - "Weapon Zen" Update
    - more attacks for weapons
    - variable chances of hitting and damage depending of weapon and types of
      attack
    """)
    main_menu()

if __name__ == "__main__":
    main_menu()