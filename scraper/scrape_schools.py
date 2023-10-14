import argparse
from RMPscraper import RMPscraper, save_info
from RMPmodules import get_card_info 

parser = argparse.ArgumentParser()

parser.add_argument("schoolID")
parser.add_argument("-o", help="The output filename, should not include extension")
parser.add_argument("-i", default=500, type=int, help="The max number of scroll iterations")
parser.add_argument("--headless", default=1, type=int, help="Whether to run headless, defaults to True")

args = parser.parse_args()

scraper = RMPscraper(
    base=f"https://www.ratemyprofessors.com/search/professors/{args.schoolID}?q=*",
    headless=args.headless
)
scraper.find_click(".CCPAModal__StyledCloseButton-sc-10x9kq-2") # Closes cookies popup
scraper.expand_all(max_iters=args.i)
page = scraper.source()
scraper.driver.quit()

cards, SCHEMA = get_card_info(page)
SCHOOL_IDX = 2

if args.o is None:
    fname = cards[0][SCHOOL_IDX]
else:
    fname = args.o
save_info(cards, fname, SCHEMA)
