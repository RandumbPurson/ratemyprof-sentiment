import argparse

from RMPscraper import RMPscraper, save_info
from RMPmodules import get_ratings

import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("profCSV", help="The filename of the csv file containing professors and their IDs")
parser.add_argument("-o", help="The output filename, should not include extension")
parser.add_argument("-s", default=5, type=int, help="The max number of scroll iterations")
parser.add_argument("--headless", default=True, help="Whether to run the chromedriver in headless mode")
parser.add_argument("-i", type=int, help="If set, limit the number of professors to get")


args = parser.parse_args()

def scrape_prof(prof_id):
    scraper = RMPscraper(
        base=f"https://www.ratemyprofessors.com/professor/{prof_id}", 
        headless=args.headless
    )
    scraper.find_click(".CCPAModal__StyledCloseButton-sc-10x9kq-2") # Closes cookies popup
    scraper.expand_all(max_iters=args.s)
    page = scraper.source()
    scraper.driver.quit()

    return get_ratings(page, prof_id)
    
def scrape_profs():
    proffesors = pd.read_csv(args.profCSV, header=0)
    school = proffesors.loc[0, "school"]
    professor_info = []
    i = 0
    for _, prof in proffesors.iterrows():
        if args.i is not None and i > args.i:
            break
        print(prof)
        if prof["num_ratings"] < 1:
            continue
        try:
            info, SCHEMA = scrape_prof(prof["prof_id"])
            professor_info.extend(info)
            i += 1
        except:
            print(f"Error getting professor data {prof}! Skipping for now...")
    
    fname = school+"-profs" if args.o is None else args.o
    save_info(professor_info,fname, SCHEMA)

scrape_profs()
