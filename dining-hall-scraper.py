import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

DAYS = 7 - (date.today().weekday() + 1) % 7 #how many days of the week are accessible thru website

def generate_urls(): 
    week_urls = []
    curr_date = date.today()
    base_url = "https://hospitality.usc.edu/residential-dining-menus/?menu_date="
    for i in range(DAYS):
        day_url = base_url + curr_date.strftime("%B") + "+" + curr_date.strftime("%-d") + "%2C+" + curr_date.strftime("%Y")
        week_urls.append(day_url)
        curr_date += timedelta(days=1)
    return week_urls

def print_week(week):
    for day in week: 
        print(day + ": ") 
        day_dict = week.get(day)
        for location in day_dict:
            print(location + ": ")
            print(day_dict.get(location), end = '\n')

def create_week_template():
    
    week_items = {}
    for i in range(DAYS):

        dining_hall_items = {
            'USC Village Dining Hall': [],
            'Parkside Restaurant & Grill': [],
            'Everybody\'s Kitchen': []
        } 

        day_of_week = date.today() + timedelta(days=i) #Monday, Tuesday...
        
        week_items[day_of_week.strftime("%A")] = dining_hall_items

    return week_items



def scrape():
    week_urls = generate_urls()
    week_items = create_week_template() #Monday: dining_hall_items, Tuesday: dining_hall_items...
    
    for i in range(DAYS):
        day_of_week = date.today() + timedelta(days=i)
        """dining_hall_items = {
            'USC Village Dining Hall': [],
            'Parkside Restaurant & Grill': [],
            'Everybody\'s Kitchen': []
        } 
        """
        #day's url 
        url = week_urls[i]
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        
        #Create list of day's items for each dining hall 
        dining_halls = soup.find_all('div', class_ = 'col-sm-6 col-md-4')   
        for dining_hall in dining_halls:
            hall_food = []
            dining_hall_name = dining_hall.find('h3', class_ = 'menu-venue-title').text

            #if dining_hall_name in dining_hall_items:

            for ul in dining_hall.find_all('ul', class_ = 'menu-item-list'):
                for item in ul.find_all('li'):
                    food = item.find(string = True, recursive = False).strip()
                    hall_food.append(food)
                    #week_items[day_of_week][dining_hall_name].append(food)
                week_items[day_of_week.strftime("%A")][dining_hall_name] = hall_food
            #get all items of day and put into respective key's list 
    return week_items

    

def get_foods(): 
    #ask user what food they want 
    foods = []
    ask = True
    while (ask):
        user_in = input("Enter the foods you like, each item separated by a comma: ")
        if (len(user_in) > 0):
            foods.extend(user_in.split(", "))
        print("Your current list of foods: ", foods)
        add_more = input("Are there more? (Y/N): ")
        if (add_more == "N" or add_more == "n"):
            ask = False
    print("Foods you're checking: ", foods)
    return foods

def find_items(week_items, find_list):
    
    items_found = create_week_template()
    
    for day in week_items: # 'Monday': {evk: [], village = []}
        day_halls_dict = week_items.get(day) # {evk: [], village = []}
        for dining_hall in day_halls_dict: 
            found = []
            day_list = day_halls_dict.get(dining_hall) # (evk's) [list of foods] 

            #check keywords of the foods you're watching (ex. "Pesto Ziti Pasta" would be a match if looking for "pesto")
            found = [potential for item in find_list for potential in day_list if item.lower() in potential.lower()]
            
            items_found[day][dining_hall] = found
            #no items found for that day and that dining hall 
            if len(items_found[day][dining_hall]) == 0:
                del items_found[day][dining_hall]
        if len(items_found[day]) == 0:
            del items_found[day]
            
    
    return items_found

def print_found(found):
    if found:
        #at least one day 
        for day in found: 
            print(day + ": ")
            
            for hall in found[day]:
                print(hall + ": ", end = "")
                print(", ".join(found[day].get(hall)), "")
                
                


def main():
    week_items = scrape()
    #fav_food = get_foods()
    fav_food = ["green goddess", "gyro", "steak", "burrito", "churros", "ramen", "pesto", "coleslaw", "Chicken Sandwich", "Kale, Quinoa and Feta Salad", "pulled pork", "fish taco"]
    found = find_items(week_items, fav_food)
    print_found(found)

    
main()
