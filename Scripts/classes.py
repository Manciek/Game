class Character:
    def __init__(self, name: str):
        self.name = name
        self.stats: dict[str, int] = {
            "ATK": 0,
            "DEF": 0,
            "HP": 0,
            "SPD": 0,
            "CRIT_RATE": 0,
            "CRIT_DMG": 0,
            "ALL_DMG_DEALT": 0,
        }
        self.skills: list[Skill] = []
        self.status_effects: list[StatusEffect] = []

    def Get_Stat(self, stat: str) -> int:
        return self.stats[stat]

class StatusEffect:
    def __init__(self, name: str, stackable: bool, stacks: int, duration: int, owner: Character):
        self.name = name
        self.stackable = stackable
        self.stacks = stacks
        self.duration = duration
        self.owner = owner

    def Take_Effect(self):
        pass

    def Remove_Stack(self):
        pass

    def Expire(self):
        pass

class Skill:
    def __init__(self, name: str, base_damage: int, modifier: int):
        self.name = name
        self.base_damage = base_damage
        self.modifier = modifier

    def Take_Effect(self):
        pass

class Player(Character):
    def __init__(self, name: str):
        super().__init__(name)
        self.inventory: list[Equipment] = []

class Enemy(Character):
    pass

class Item:
    pass

class Equipment(Item):
    pass

class Usable(Item):
    pass

class CombatSystem:
    turn = 0

    @staticmethod
    def Round_Run(player: Character, enemies: list[Character]):
        # 1. Status Effects
        for effect in player.status_effects:
            effect.Take_Effect()

    @staticmethod
    def Deal_Dmg(attacker: Character, defender: Character, skill: Skill):
        dmg = (skill.base_damage + attacker.Get_Stat("ATK")*skill.modifier//100) - defender.Get_Stat("DEF")
        # Deal dmg

    @staticmethod
    def Next_Turn():
        CombatSystem.turn += 1
