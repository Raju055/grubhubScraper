import re, csv, time, json, requests, unicodedata

auth_token = ""


def remSpCh(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    return ''.join([i for i in s if ord(i) < 128])


def isRestaurantDeliveryOrPickup(delivery, pickup):
    if delivery and pickup:
        return 'Both'
    elif delivery:
        return 'Delivery Only'
    else:
        return 'Pickup Only'


def main():
    output_file = 'result_nutritionix.csv'
    data_to_file = open(output_file, 'w', newline='')
    csv_writer = csv.writer(data_to_file, delimiter=",")
    csv_writer.writerow(
        ["Restaurant", "Food Item", "Serving Size", "Calories", "Calories from Fat", "Total Fat", "Saturated Fat",
         "Trans Fat", "Cholesterol", "Sodium", "Total Carbohydrates", "Dietary Fiber", "Sugars", "Proteins",
         "Vitamin A", "Vitamin C", "Calcium", "Iron"
         ])
    global auth_token
    auth_url = "https://api-gtm.grubhub.com/auth"
    auth_payload = {"brand": "GRUBHUB", "client_id": "beta_UmWlpstzQSFmocLy3h1UieYcVST", "device_id": -1512757421,
                    "scope": "anonymous"}
    url = "https://api-gtm.grubhub.com/restaurants/2316?hideChoiceCategories=true&version=4&variationId=rtpFreeItems&orderType=standard&hideUnavailableMenuItems=true&hideMenuItems=false&showMenuItemCoupons=true&includePromos=true&location=POINT(-73.99679566%2040.75337982)&locationMode=delivery"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': auth_token}
    application_json = {'Content-Type': 'application/json'}
    try:
        json_text = json.loads(requests.get(url, headers=headers).text)
    except:
        r = requests.post(auth_url, headers=application_json, data=json.dumps(auth_payload))
        auth_token = "Bearer " + json.loads(r.text)['session_handle']['access_token']
        headers = {'Accept': 'application/json', 'Authorization': auth_token}
        json_text = json.loads(requests.get(url, headers=headers).text)
    numberrecords = 0
    for restaurant in json_text['restaurant']['menu_category_list']:
        for menuname in restaurant['menu_item_list']:
            name = menuname['name']

            urlinstant = "https://trackapi.nutritionix.com/v2/search/instant"
            querystring = {"query": name, "self": "true", "branded": "false", "common": "true",
                           "common_general": "true", "common_grocery": "true", "common_restaurant": "true",
                           "detailed": "false", "claims": "false"}

            headers = {
                'accept': "application/json",
                'accept-encoding': "gzip, deflate, br",
                'accept-language': "en-US,en;q=0.9",
                'connection': "keep-alive",
                'cookie': "__cfduid=d8c922fdf22deba3bcb03df9687b955591568009977; _ga=GA1.2.62655578.1568009980; _gid=GA1.2.1480837771.1568009980",
                'host': "trackapi.nutritionix.com",
                'referer': "https://trackapi.nutritionix.com/docs/",
                'sec-fetch-mode': "cors",
                'sec-fetch-site': "same-origin",
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
                'x-app-id': "f1a5c4e4",
                'x-app-key': "5be93f976af68dd906a532a857421157",
                'cache-control': "no-cache",
                'postman-token': "cdd9512f-4ad6-07f1-3fcd-09fdbe6ccb8a"
            }

            responseinstant = requests.request("GET", urlinstant, headers=headers, params=querystring)
            datainstant = responseinstant.text
            parsedinstant = json.loads(datainstant)

            parsedinstant['common']
            url = "https://d1gvlspmcma3iu.cloudfront.net/brands-restaurant.json.gz"
            response = requests.get(url)
            data = response.text
            parsed = json.loads(data)

            for _data in parsed:
                urlbrand = "https://www.nutritionix.com/nixapi/brands/" + _data['id'] + "/items/1?limit=2000&search="
                responsebrand = requests.get(urlbrand)
                databrand = responsebrand.text
                parsedbrand = json.loads(databrand)
                for _databrand in parsedbrand["items"]:
                    try:
                        numberrecords += 1
                        print(str(numberrecords) + " ]Brand: " + _data["name"] + ", Food :" + _databrand["item_name"])
                        urlfood = "https://www.nutritionix.com/nixapi/items/" + _databrand["item_id"]
                        responsefood = requests.get(urlfood)
                        datafood = responsefood.text
                        parsedfood = json.loads(datafood)

                        Restaurant = '"' + _data['name'] + '"'
                        Food_Item = '"' + parsedfood['item_name'] + '"'
                        Serving_Size = str(parsedfood['serving_qty']) + " " + str(parsedfood['serving_unit'])
                        if parsedfood['metric_qty'] != "":
                            Serving_Size = '"' + Serving_Size + " ( " + str(parsedfood['metric_qty']) + " " + str(
                                parsedfood['metric_unit']) + " )" + '"'

                        Calories = parsedfood['calories']
                        Calories_from_Fat = int(parsedfood['total_fat']) * 9
                        Total_Fat = parsedfood['total_fat']
                        Saturated_Fat = parsedfood['saturated_fat']
                        Trans_Fat = parsedfood['trans_fat']
                        Cholesterol = parsedfood['cholesterol']
                        Sodium = parsedfood['sodium']
                        Total_Carbohydrates = parsedfood['total_carb']
                        Dietary_Fiber = parsedfood['dietary_fiber']
                        Sugars = parsedfood['sugars']
                        Proteins = parsedfood['protein']
                        Vitamin_A = parsedfood['vitamin_a']
                        Vitamin_C = parsedfood['vitamin_c']
                        Calcium = parsedfood['calcium_dv']
                        Iron = parsedfood['iron_dv']

                        csv_writer.writerow(
                            [Restaurant, Food_Item, Serving_Size, Calories, Calories_from_Fat, Total_Fat, Saturated_Fat,
                             Trans_Fat, Cholesterol, Sodium, Total_Carbohydrates, Dietary_Fiber, Sugars, Proteins,
                             Vitamin_A, Vitamin_C, Calcium, Iron])
                    except Exception:
                        pass  # or you could use 'continue'
            data_to_file.close()


if __name__ == '__main__':
    main()
