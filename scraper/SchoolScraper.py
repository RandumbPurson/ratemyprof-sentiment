# csv (std lib)
# docs: https://docs.python.org/3/library/csv.html
import csv

# beautifulsoup
# docs: https://beautiful-soup-4.readthedocs.io/en/latest/
from bs4 import BeautifulSoup

# Fields
CARD_CLS = "TeacherCard__StyledTeacherCard-syjs0d-0"
CARD_CLS_name = "CardName__StyledCardName-sc-1gyrgim-0"
CARD_CLS_num_rating = "CardNumRating__CardNumRatingCount-sc-17t4b9u-3"
CARD_CLS_department = "CardSchool__Department-sc-19lmz2k-0"
CARD_CLS_school = "CardSchool__School-sc-19lmz2k-1"

def get_card_info(page_source):
    soup = BeautifulSoup(page_source, features="lxml")
    cards = []
    
    for card in soup.find_all(class_=CARD_CLS):
        name = card.find(class_=CARD_CLS_name).contents[0]
        prof_id = card.get("href").split("/")[-1]
        school = card.find(class_=CARD_CLS_school).contents[0]
        department = card.find(class_=CARD_CLS_department).contents[0]
        num_ratings = card.find(class_=CARD_CLS_num_rating).contents[0].split(" ")[0]
        # SCHEMA: name, prof_id, school, department, num_ratings
        cards.append([name, prof_id, school, department, num_ratings])

    return cards


# SCHEMA
SCHEMA = ["name", "prof_id", "school", "department", "num_ratings"]
def save_card_info(card_info, filename):
    with open(f"{filename}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(SCHEMA)
        writer.writerows(card_info)
        
