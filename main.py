import Scripts.classes as c

if __name__ == "__main__":
    print("Start")

    player = c.Player("Mike")
    sword = c.Gear("Magic Sword",
                   c.GearType.WEAPON,
                   c.GearRarity.RARE,
                   130, 40, 55, 60, 2, 5, 0)

    helmet = c.Gear("Magic Helmet",
                    c.GearType.HELMET,
                    c.GearRarity.RARE,
                    130, 40, 55, 60, 2, 5, 0)

    healing_potion = c.Usable("Healing Potion",
                              c.UsableType.POTION,
                              3, 100)

    c.LobbySystem.AddToInv([sword, helmet], player)

    run = True
    while run:
        inp = input("\nDo you want to: 1-See equipped | 2-Equip new item | 3-See stats | 4-See inv\n "
                    "5-Add 3 HealPots | OTHER-Exit")
        match int(inp):
            case 1:
                for item in player.eq.values():
                    print(item)
            case 2:
                ind = int(input("Gear id: "))
                it = player.gear[ind]
                if it:
                    c.LobbySystem.EquipGear(it, player)
            case 3:
                print(player.stats)
            case 4:
                print("Inventory of gears:")
                for gear in player.gear.values():
                    print(gear)
                print("\nInventory of usables:")
                for usable in player.usables.values():
                    print(usable)
            case 5:
                print("Adding 3 potions")
                c.LobbySystem.AddToInv([healing_potion], player)
            case _:
                run = False