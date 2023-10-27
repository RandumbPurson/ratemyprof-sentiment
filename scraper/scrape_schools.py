from RMPscraper import RMPscraper, save_info
from RMPmodules import get_card_info 

def scrape_schools(school_id, output, headless=True, max_iters=500):
    scraper = RMPscraper(
        base=f"https://www.ratemyprofessors.com/search/professors/{school_id}?q=*",
        headless=headless
    )
    scraper.find_click(".CCPAModal__StyledCloseButton-sc-10x9kq-2") # Closes cookies popup
    scraper.expand_all(max_iters=max_iters)
    page = scraper.source()
    scraper.driver.quit()

    cards, SCHEMA = get_card_info(page)
    SCHOOL_IDX = 2

    fname = cards[0][SCHOOL_IDX] if output is None else output
    save_info(cards, fname, SCHEMA)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("schoolID")
    parser.add_argument("-o", help="The output filename, should not include extension")
    parser.add_argument("-i", default=500, type=int, help="The max number of scroll iterations")
    parser.add_argument("--headless", default=True, help="Whether to run the chromedriver in headless mode")
    
    args = parser.parse_args()
    
    scrape_schools(args.schoolID, args.o, args.headless, args.i)
