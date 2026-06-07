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
                              c.UsableType.POTION, 11)

    c.LobbySystem.AddToInv([(sword, 1), (helmet, 1)], player)

    run = True
    while run:
        inp = input("\nDo you want to: 1-See the inventory | 2-Equip a new item | 3-See stats | 4-Add 3 HealPots | OTHER-Exit")
        match int(inp):
            case 1:
                player.PrintInventory()
            case 2:
                ind = int(input("Gear id from your inventory: "))
                it = player.gears[ind]
                if it:
                    c.LobbySystem.EquipGear(it, player)
            case 3:
                player.PrintStats()
            case 4:
                print("Adding 3 potions")
                c.LobbySystem.AddToInv([(healing_potion, 3)], player)
            case _:
                run = False
