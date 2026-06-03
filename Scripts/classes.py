class Character:
    def __init__(self, name: str):
        self.name = name
        self.alive = True
        self.stats: dict[str, int] = {
            "BASE_ATK": 0,
            "BASE_DEF": 0,
            "BASE_HP": 0,
            "BASE_SPD": 0,
            "BASE_CRIT_RATE": 0,
            "BASE_CRIT_DMG": 0,
            "BASE_ALL_DMG_DEALT": 100,      # in % remember to divide by 100 and turn into int when working with all_dmg

            "GEAR_ATK": 0,
            "GEAR_DEF": 0,
            "GEAR_HP": 0,
            "GEAR_SPD": 0,
            "GEAR_CRIT_RATE": 0,
            "GEAR_CRIT_DMG": 0,
            "GEAR_ALL_DMG_DEALT": 0,

            # stats in % used as a multiplyier and dividing then by 100 and turning into int !! A_D_D MUST BE additive
            "ATK_BUFF": 100,
            "DEF_BUFF": 100,
            "HP_BUFF": 100,
            "SPD_BUFF": 100,
            "CRIT_RATE_BUFF": 100,
            "CRIT_DMG_BUFF": 100,
            "ALL_DMG_DEALT_BUFF": 0,

            "CURRENT_HP": 0,
            "MAX_HP": 0,
        }
        self.skills: list[Skill] = []
        self.status_effects: list[StatusEffect] = []

    def Initialize_HP(self) -> None:
        self.stats["MAX_HP"] = (self.stats["BASE_HP"] + self.stats["GEAR_HP"]) * int(self.stats["HP_BUFF"] / 100)

    def Get_ATK(self) -> int:
        return (self.stats["BASE_ATK"] + self.stats["GEAR_ATK"]) * int(self.stats["ATK_BUFF"] / 100)

    def Get_DEF(self) -> int:
        return(self.stats["BASE_DEF"] + self.stats["GEAR_DEF"]) * int(self.stats["DEF_BUFF"] / 100)

    def Get_HP(self) -> int:
        return self.stats["CURRENT_HP"]

    def Get_SPD(self) -> int:
        return (self.stats["BASE_SPD"] + self.stats["GEAR_SPD"]) * int(self.stats["SPD_BUFF"] / 100)

    def Get_ADD(self) -> int:           # Addidtive as its a percateage in its core
        return self.stats["BASE_ALL_DMG_DEALT"] + self.stats["GEAR_ALL_DMG_DEALT"] + self.stats["ALL_DMG_DEALT_BUFF"]

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
        self.base_damage = base_damage
        # 0-? in % value so we DIVIDE by 100, represents the multiplier for ATK for each hit
        self.modifier = modifier / 100

    def Take_Effect(self):
        pass

class Player(Character):
    def __init__(self, name: str):
        super().__init__(name)
        self.Initialize_HP()
        # Currently wearing that or using that.
        # Fixed number of slots => Head, Torso, Legs, MainHand, OffHand
        self.eq: list[Equipment] = []
        # Every item in the inventory - eq
        self.backpack: list[Item] = []

class Enemy(Character):
    pass

class Item:
    def __init__(self, name):
        self.name = name

# ARMOR TYPES AND WEAPON + OFFHAND
class Equipment(Item):
    def __init__(self, name, atk, deff, hp, spd, crit_dmg, crit_rt, dmg_amp):
        super().__init__(name)
        self.ATK = atk
        self.DEF = deff
        self.HP = hp
        self.SPD = spd
        self.CRIT_DMG = crit_dmg
        self.CRIT_RATE = crit_rt
        self.ALL_DMG_DEALT = dmg_amp

# POTIONS AND SOME OTHER SHIT
class Usable(Item):
   def __init__(self, name):
       super().__init__(name)

class CombatSystem:
    turn = 1

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
        defender.stats["CURRENT_HP"] -= dmg
        if not CombatSystem.Character_Alive(defender):
            defender.Die()

    @staticmethod
    def Calculate_Gear_Stats(player: Player) -> None:
        ATK = sum(item.ATK for item in player.eq)
        DEF = sum(item.DEF for item in player.eq)
        HP = sum(item.HP for item in player.eq)
        SPD = sum(item.SPD for item in player.eq)
        CRIT_DMG = sum(item.CRIT_DMG for item in player.eq)
        CRIT_RATE = sum(item.CRIT_RATE for item in player.eq)
        ALL_DMG_DEALT = sum(item.ALL_DMG_DEALT for item in player.eq)

        lista = {"ATK": ATK,
                 "DEF": DEF,
                 "HP": HP,
                 "SPD": SPD,
                 "CRIT_DMG": CRIT_DMG,
                 "CRIT_RATE": CRIT_RATE,
                 "ALL_DMG_DEALT": ALL_DMG_DEALT,
                 }

        for key, value in lista.items():
            player.stats[f"GEAR_{key}"] = value

# TO DO
    @staticmethod
    def Round_Run(player: Player, enemies: list[Enemy]) -> None:
        if CombatSystem.turn == 1:
            CombatSystem.Calculate_Gear_Stats(player)

        # 1. Status Effects
        for effect in player.status_effects:
            effect.Take_Effect()
        for enemy in enemies:
            for effect in enemy.status_effects:
                effect.Take_Effect()

        CombatSystem.Next_Turn()

    @staticmethod
    def Next_Turn():
        CombatSystem.turn += 1
