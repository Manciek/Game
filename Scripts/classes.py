from enum import Enum

# Equipable
class GearType(Enum):
    WEAPON = 0
    CHESTPLATE = 1
    OFFHAND = 2
    HELMET = 3
    LEGGINGS = 4

class GearRarity(Enum):
    LEGENDARY = 0
    MYTHIC = 1
    RARE = 2
    UNCOMMON = 3
    COMMON = 4

# Usable
class UsableType(Enum):
    POTION = 10
    MATERIAL = 11


class Character:
    def __init__(self, name: str):
        self.name = name
        self.alive = True
        self.stats: dict[str, int] = {
            "BASE_ATK": 0,
            "BASE_DEF": 0,
            "BASE_HP": 0,
            "BASE_SPD": 0,
            "BASE_CRIT_RATE": 0,            # 0-1 but in % so can go over 100 but wont do shit
            "BASE_CRIT_DMG": 100,           # in % so div 100

            "GEAR_ATK": 0,
            "GEAR_DEF": 0,
            "GEAR_HP": 0,
            "GEAR_SPD": 0,
            "GEAR_CRIT_RATE": 0,
            "GEAR_CRIT_DMG": 0,
            "GEAR_LIFESTEAL": 0,
            "GEAR_ALL_DMG_DEALT": 0,

            # stats from buffs in %
            "ATK_BUFF": 100,
            "DEF_BUFF": 100,
            "HP_BUFF": 100,
            "SPD_BUFF": 100,
            "CRIT_RATE_BUFF": 0,
            "CRIT_DMG_BUFF": 100,
            "LIFESTEAL_BUFF": 0,
            "ALL_DMG_DEALT_BUFF": 0,

            "LEVEL": 0,
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
        return self.stats["GEAR_ALL_DMG_DEALT"] + self.stats["ALL_DMG_DEALT_BUFF"]

    def Get_CRIT_RATE(self) -> int:
        return min(self.stats["BASE_CRIT_RATE"] + self.stats["GEAR_CRIT_RATE"] + self.stats["CRIT_RATE_BUFF"], 100)

    def Get_CRIT_DMG(self) -> float:
        return (self.stats["BASE_CRIT_DMG"] + self.stats["GEAR_CRIT_DMG"] + self.stats["CRIT_DMG_BUFF"]) / 100

    def Get_LIFESTEAL(self) -> float:
        return (self.stats["GEAR_LIFESTEAL"] + self.stats["LIFESTEAL_BUFF"]) / 100

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
        # Currently wearing that or using that.
        self.eq: dict[GearType, Gear | None] = {}
        # Every item in the inventory - eq (ID : ITEM)
        self.gears: dict[int, Gear] = {}
        self.usables: dict[str, tuple[int, Usable]] = {}

    def PrintInventory(self) -> None:
        print("\nEquipped items: ")
        if len(self.eq) == 0:
            print("None items equipped")
        else:
            for g_type, gear in self.eq.items():
                print(f"Type: {g_type} -> {gear}")
        print("\nInventory of Gears: ")
        if len(self.gears) == 0:
            print("No gears in the inventory")
        else:
            for gear in self.gears.values():
                print(gear)
        print("\nInventory of Usables: ")
        if len(self.usables) == 0:
            print("No usales/materials/etc in the inventory")
        else:
            for amount, item in self.usables.values():
                print(f"Item: {item} -> {amount}")

    def PrintStats(self) -> None:
        for stat, v in self.stats.items():
            print(f"STAT: {stat} -> {v}")

class Enemy(Character):
    pass

class Item:
    _next_item_id = 1

    def __init__(self, name: str, item_type: GearType | UsableType):
        self.name = name
        self.item_type = item_type

    def __str__(self):
        return f"Item name: {self.name} -> type: {self.item_type}"

# ARMOR TYPES AND WEAPON + OFFHAND
class Gear(Item):
    def __init__(self, name: str, item_type: GearType, rarity: GearRarity, atk: int, deff: int, hp: int, spd: int, crit_dmg: int, crit_rt: int, lifesteal: int, dmg_amp: int):
        super().__init__(name, item_type)
        self.stats = {
            "ATK": atk,
            "DEF": deff,
            "HP": hp,
            "SPD": spd,
            "CRIT_DMG": crit_dmg,
            "CRIT_RATE": crit_rt,
            "LIFESTEAL": lifesteal,
            "ALL_DMG_DEALT": dmg_amp,
        }
        self.id = Item._next_item_id
        self.rarity = rarity
        Item._next_item_id += 1

    def __str__(self):
        base = super().__str__()
        return f"{base} -> rarity: {self.rarity} -> id: {self.id}"

# POTIONS AND SOME OTHER SHIT
class Usable(Item):
    def __init__(self, name: str, item_type: UsableType, max_amount: int):
        super().__init__(name, item_type)
        self.max_amount = max_amount

    def __str__(self):
        base = super().__str__()
        return f"{base} -> max: {self.max_amount}"

    def Happen(self):
        pass


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

# TO DO
    @staticmethod
    def Round_Run(player: Player, enemies: list[Enemy]) -> None:
        if CombatSystem.turn == 1:
            player.Initialize_HP()

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

class LobbySystem:
    @staticmethod
    def EquipGear(gear: Gear, player: Player) -> None:
        # Remove current gear slot
        LobbySystem.RemoveGear(gear.item_type, player)

        # Equip the new gear and Delete from gear inventory the newly equipped gear
        if gear.id in player.gears.keys():
            player.eq[gear.item_type] = gear
            player.gears.pop(gear.id)
        LobbySystem.Calculate_Gear_Stats(player)

    @staticmethod
    def RemoveGear(gear_type: GearType, player: Player):
        gear = player.eq.pop(gear_type, None)
        if gear is None:
            print(f"No gear of type: {gear_type} equipped.\n")
            return
        LobbySystem.AddToInv([(gear, 1)], player)
        LobbySystem.Calculate_Gear_Stats(player)

    @staticmethod
    def AddToInv(items: list[tuple[Item, int]], player: Player):
        for item, amount in items:
            if item.item_type in GearType:
                player.gears[item.id] = item
            elif item.item_type in UsableType:
                if item.name in player.usables:
                    player.usables[item.name] = (player.usables[item.name][0] + amount, item)
                else:
                    player.usables[item.name] = (amount, item)
                if player.usables[item.name][0] > player.usables[item.name][1].max_amount:
                    player.usables[item.name] = (player.usables[item.name][1].max_amount, item)
                    print("Exceeded the max amount so the excess was removed automatically")
            else:
                print(f"Unknown item type: {item.name}, {item.item_type}")

    @staticmethod
    def Calculate_Gear_Stats(player: Player) -> None:
        ATK = sum(item.stats["ATK"] for item in player.eq.values() if item is not None)
        DEF = sum(item.stats["DEF"] for item in player.eq.values() if item is not None)
        HP = sum(item.stats["HP"] for item in player.eq.values() if item is not None)
        SPD = sum(item.stats["SPD"] for item in player.eq.values() if item is not None)
        CRIT_DMG = sum(item.stats["CRIT_DMG"] for item in player.eq.values() if item is not None)
        CRIT_RATE = sum(item.stats["CRIT_RATE"] for item in player.eq.values() if item is not None)
        LIFESTEAL = sum(item.stats["LIFESTEAL"] for item in player.eq.values() if item is not None)
        ALL_DMG_DEALT = sum(item.stats["ALL_DMG_DEALT"] for item in player.eq.values() if item is not None)

        lista = {"ATK": ATK,
                 "DEF": DEF,
                 "HP": HP,
                 "SPD": SPD,
                 "CRIT_DMG": CRIT_DMG,
                 "CRIT_RATE": CRIT_RATE,
                 "LIFESTEAL": LIFESTEAL,
                 "ALL_DMG_DEALT": ALL_DMG_DEALT,
                 }

        for key, value in lista.items():
            player.stats[f"GEAR_{key}"] = value
