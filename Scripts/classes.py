class Character:
    def __init__(self, name: str):
        self.name = name
        self.alive = True
        self.stats: dict[str, int] = {
            "ATK": 0,
            "DEF": 0,
            "HP": 0,
            "SPD": 0,
            "CRIT_RATE": 0,
            "CRIT_DMG": 0,

            "MAX_HP": 0,
            "CURRENT_HP": 0,

            "ALL_DMG_DEALT": 0,
            "ATK_BOOST": 0,
            "DEF_BOOST": 0,
            "HP_BOOST": 0,
            "SPD_BOOST": 0,

        }
        self.skills: list[Skill] = []
        self.status_effects: list[StatusEffect] = []

    def Initialize_HP(self) -> None:
        self.stats["MAX_HP"] = self.stats["HP"] + self.stats["HP_BOOST"]
        self.stats["CURRENT_HP"] = self.stats["MAX_HP"]

    def Get_ATK(self) -> int:
        return self.stats["ATK"] + self.stats["ATK_BOOST"]

    def Get_DEF(self) -> int:
        return self.stats["DEF"] + self.stats["DEF_BOOST"]

    def Get_HP(self) -> int:
        return self.stats["CURRENT_HP"]

    def Get_SPD(self) -> int:
        return self.stats["SPD"] + self.stats["SPD_BOOST"]

    def Get_ADD(self) -> int:
        return self.stats["ALL_DMG_DEALT"]

    def Die(self) -> None:
        pass


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
    def __init__(self, name: str, base_damage: int, modifier: int, player: Character):
        self.name = name
        # base dmg will be changing once with the player stats one the init by a percantage of its base
        self.base_damage = base_damage + player.Get_ATK() // 10
        # 0-? in % value so we // by 100, represents the multiplier for ATK for each hit
        self.modifier = modifier / 100

    def Take_Effect(self):
        pass

class Player(Character):
    def __init__(self, name: str):
        super().__init__(name)
        self.inventory: list[Equipment] = []

class Enemy(Character):
    pass

class Item:
    def __init__(self, name):
        self.name = name

class Equipment(Item):
    pass

class Usable(Item):
    pass

class CombatSystem:
    turn = 0

    @staticmethod
    def Character_Alive(character: Character) -> bool:
        if character.Get_HP() <= 0:
            character.alive = False
            return False
        return True

    @staticmethod
    def Deal_Dmg(attacker: Character, defender: Character, skill: Skill) -> None:
        base_dmg = (skill.base_damage + int(attacker.Get_ATK() * skill.modifier)) - defender.Get_DEF()
        dmg = base_dmg * attacker.Get_ADD()
        # Deal dmg
        defender.stats["HP"] -= dmg
        if not CombatSystem.Character_Alive(defender):
            defender.Die()

# TO DO
    @staticmethod
    def Round_Run(player: Character, enemies: list[Character]) -> None:
        # 1. Status Effects
        for effect in player.status_effects:
            effect.Take_Effect()

    @staticmethod
    def Next_Turn():
        CombatSystem.turn += 1
