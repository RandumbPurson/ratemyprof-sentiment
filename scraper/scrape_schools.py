import argparse
from RMPscraper import RMPscraper, save_info
from RMPmodules import get_card_info 

parser = argparse.ArgumentParser()

parser.add_argument("schoolID")
parser.add_argument("-o", help="The output filename, should not include extension")
parser.add_argument("-s", default=500, type=int, help="The max number of scroll iterations")
parser.add_argument("--headless", default=1, help="Whether to run the chromedriver in headless mode1 for headless, 0 for not headless")

args = parser.parse_args()

headless = args.headless == 1

def scrape_schools():
    scraper = RMPscraper(
        base=f"https://www.ratemyprofessors.com/search/professors/{args.schoolID}?q=*",
        headless=headless
    )
    scraper.find_click(".CCPAModal__StyledCloseButton-sc-10x9kq-2") # Closes cookies popup
    scraper.expand_all(max_iters=args.s)
    page = scraper.source()
    scraper.driver.quit()

    cards, SCHEMA = get_card_info(page)
    SCHOOL_IDX = 2

    fname = cards[0][SCHOOL_IDX] if args.o is None else args.o
    save_info(cards, fname, SCHEMA)

scrape_schools()
