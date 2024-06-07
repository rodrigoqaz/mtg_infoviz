from src.scryfall import ScryfallHandler
import pyedhrec

scryfall_handler = ScryfallHandler()

scryfall_handler.download_bulk_data('All')
scryfall_handler.download_all_commander_cards()


edhrec = pyedhrec.EDHRec()

carta = "Ayara, First of Locthwain"
details = edhrec.get_card_details(carta)
combos = edhrec.get_card_combos(carta)
sinergia = edhrec.get_high_synergy_cards(carta)
print(sinergia)