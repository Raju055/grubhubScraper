import re, csv, time, json, requests, unicodedata
import random
from difflib import SequenceMatcher
from fuzzywuzzy.fuzz import ratio as fuzz_ratio
from random import randint


def numRestaurants():
    try:
        restaurantsnumber = int(input("Enter restaurants number : "))
    except:
        print("You must enter a number")
        numRestaurants()
    return restaurantsnumber


def _digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def numServingsize():
    try:
        ServingSize = int(input("Enter Serving Size : ") or "1")
    except:
        print("You must enter a number")
        numServingsize()
    return ServingSize


def get_rows(file_name):
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        yield from reader

def similarity_to(x, column_name):
    x = x.lower()
    def similarity(row):
        return fuzz_ratio(row[column_name].lower(), x)
    return similarity

auth_token = ""


def main(restaurantsnumber, ServingSize):
    output_file = str(restaurantsnumber) + '_nutritionix.csv'
    data_to_file = open(output_file, 'w', newline='')
    csv_writer = csv.writer(data_to_file, delimiter=",")
    csv_writer.writerow(
        ["Restaurant", "Seamless Food Item Main", "Menu List Category", "Seamless Food Item Sub",
         "Nutritionix Food Item", "Serving Size",
         "Calories", "Calories from Fat", "Total Fat", "Saturated Fat",
         "Trans Fat", "Cholesterol", "Sodium", "Total Carbohydrates", "Dietary Fiber", "Sugars", "Proteins",
         "Vitamin A", "Vitamin C", "Calcium", "Iron"
         ])
    global auth_token
    auth_url = 'https://api-gtm.grubhub.com/auth'
    headers = {
        'Pragma': 'no-cache',
        'Origin': 'https://www.seamless.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Cache-Control': 'no-cache',
        'Referer': 'https://www.seamless.com',
        'Connection': 'keep-alive'
    }
    auth_payload = {
        "brand": "SEAMLESS",
        "client_id": "beta_seamless_ayNyuFxxVQYefSAhFYCryvXBPQc",
        "device_id": _digits(10),
        "scope": "anonymous"
    }

    url = "https://api-gtm.grubhub.com/restaurants/" + str(
        restaurantsnumber) + "?hideChoiceCategories=true&version=4&variationId=rtpFreeItems&orderType=standard&hideUnavailableMenuItems=true&hideMenuItems=false&showMenuItemCoupons=true&includePromos=true&location=POINT(-74.01759339%2040.71073913)&locationMode=delivery"

    try:
        json_text = json.loads(requests.get(url, headers=headers).text)
    except:
        r = requests.post(auth_url, data=json.dumps(auth_payload), headers=headers)
        auth_token = "Bearer " + json.loads(r.text)['session_handle']['access_token']
        headers = {'Accept': 'application/json', 'Authorization': auth_token}
        json_text = json.loads(requests.get(url, headers=headers).text)
    numberrecords = 0
    for restaurant in json_text['restaurant']['menu_category_list']:
        for menuname in restaurant['menu_item_list']:
            try:
                name = menuname['name']
                items = get_rows('commonfood.csv')
                row1 = max(items, key=similarity_to(name, "Food Item"))
                numberrecords += 1
                seamless_Food_ItemmMain = name
                seamless_Food_ItemmSub = name
                Menu_List_Category = row1["Food Item"]
                Restaurant = json_text['restaurant']['name']
                nutritionix_Food_Item = row1["Food Item"]
                Serving_Size = row1["Serving Size"]
                Calories = row1["Calories"] * ServingSize
                Calories_from_Fat = row1["Calories from Fat"] * ServingSize
                Total_Fat = row1["Total Fat"] * ServingSize
                Saturated_Fat = row1["Saturated Fat"] * ServingSize
                Trans_Fat = row1["Trans Fat"] * ServingSize
                Cholesterol = row1["Cholesterol"] * ServingSize
                Sodium = row1["Sodium"] * ServingSize
                Total_Carbohydrates = row1["Total Carbohydrates"] * ServingSize
                Dietary_Fiber = row1["Dietary Fiber"] * ServingSize
                Sugars = row1["Sugars"] * ServingSize
                Proteins = row1["Proteins"] * ServingSize
                Vitamin_A = row1["Vitamin A"] * ServingSize
                Vitamin_C = row1["Vitamin C"] * ServingSize
                Calcium = row1["Calcium"] * ServingSize
                Iron = row1["Iron"] * ServingSize
                csv_writer.writerow(
                    [Restaurant, seamless_Food_ItemmMain, Menu_List_Category, seamless_Food_ItemmSub,
                     nutritionix_Food_Item,
                     Serving_Size, Calories, Calories_from_Fat, Total_Fat,
                     Saturated_Fat,
                     Trans_Fat, Cholesterol, Sodium, Total_Carbohydrates, Dietary_Fiber, Sugars, Proteins,
                     Vitamin_A, Vitamin_C, Calcium, Iron])
                print(str(numberrecords) + " ]food_name: " + nutritionix_Food_Item)

                url1 = "https://api-gtm.grubhub.com/restaurants/" + str(restaurantsnumber) + "/menu_items/" + menuname[
                    'id'] + "?time=1568719007454&orderType=standard&version=4"
                try:
                    json_text1 = json.loads(requests.get(url1, headers=headers).text)
                except:
                    r = requests.post(auth_url, data=json.dumps(auth_payload), headers=headers)
                    auth_token1 = "Bearer " + json.loads(r.text)['session_handle']['access_token']
                    headers1 = {'Accept': 'application/json', 'Authorization': auth_token1}
                    json_text1 = json.loads(requests.get(url1, headers=headers1).text)
                for _databrand in json_text1["choice_category_list"]:
                    for _category_list in _databrand["choice_option_list"]:
                        try:
                            itemextra = _category_list['description'].replace('Add', '').strip()
                            itemextra = itemextra.replace('Remove', '')
                            itemextra = itemextra.replace('Extra', '')
                            itemsExtra = get_rows('commonfood.csv')
                            row = max(itemsExtra, key=similarity_to(itemextra, "Food Item"))
                            numberrecords += 1
                            seamless_Food_ItemmMain = name
                            seamless_Food_ItemmSub = itemextra
                            Menu_List_Category = _databrand['name']
                            Restaurant = json_text['restaurant']['name']
                            nutritionix_Food_Item = row["Food Item"]
                            Serving_Size = row["Serving Size"]
                            Calories = row["Calories"] * ServingSize
                            Calories_from_Fat = row["Calories from Fat"] * ServingSize
                            Total_Fat = row["Total Fat"] * ServingSize
                            Saturated_Fat = row["Saturated Fat"] * ServingSize
                            Trans_Fat = row["Trans Fat"] * ServingSize
                            Cholesterol = row["Cholesterol"] * ServingSize
                            Sodium = row["Sodium"] * ServingSize
                            Total_Carbohydrates = row1["Total Carbohydrates"] * ServingSize
                            Dietary_Fiber = row["Dietary Fiber"] * ServingSize
                            Sugars = row["Sugars"] * ServingSize
                            Proteins = row["Proteins"] * ServingSize
                            Vitamin_A = row["Vitamin A"] * ServingSize
                            Vitamin_C = row["Vitamin C"] * ServingSize
                            Calcium = row["Calcium"] * ServingSize
                            Iron = row["Iron"] * ServingSize
                            csv_writer.writerow(
                                [Restaurant, seamless_Food_ItemmMain, Menu_List_Category, seamless_Food_ItemmSub,
                                 nutritionix_Food_Item, Serving_Size, Calories, Calories_from_Fat, Total_Fat,
                                 Saturated_Fat,
                                 Trans_Fat, Cholesterol, Sodium, Total_Carbohydrates, Dietary_Fiber, Sugars,
                                 Proteins,
                                 Vitamin_A, Vitamin_C, Calcium, Iron])
                            print(str(
                                numberrecords) + " ]food name Main: " + seamless_Food_ItemmMain + ", #food name sub: " + seamless_Food_ItemmSub)

                        except Exception:
                            print(
                                str(
                                    numberrecords) + "Error ]food name Main: " + seamless_Food_ItemmMain + ", #food name sub: " + seamless_Food_ItemmSub)
                            pass  # or you could use 'continue'

            except OSError as err:
                print("OS error: {0}".format(err))
            except ValueError as err:
                print("Error : ".format(err))
            except:
                pass  # or you could use 'continue'
    data_to_file.close()


if __name__ == '__main__':
    restaurantsnumber = numRestaurants()
    ServingSize = numServingsize()
    main(restaurantsnumber, ServingSize)
