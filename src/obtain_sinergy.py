from pyedhrec import EDHRec


edhrec = EDHRec()

def obtain_sinergy(commander, deck):
    commander_related = edhrec.get_commander_cards(commander)

    cards_with_synergy = []
    cards_without_synergy = [] 

    sections = ['New Cards', 'High Synergy Cards', 'Top Cards', 'Creatures', 'Instants', 'Sorceries', 'Utility Artifacts', 'Enchantments', 'Planeswalkers', 'Utility Lands', 'Mana Artifacts', 'Lands']
    for card in deck:
        found = False
        for section in sections:
            if section in commander_related:
                for new_card in commander_related[section]:
                    if new_card['name'].lower() == card.lower():
                        cards_with_synergy.append({'name': card, 'synergy': new_card['synergy']})
                        found = True
                        break
            if found:
                break
        if not found:
            cards_without_synergy.append(card)
    
    result =  {
        'cards_with_synergy': cards_with_synergy, 
        'cards_without_synergy': cards_without_synergy
        }
    
    return result