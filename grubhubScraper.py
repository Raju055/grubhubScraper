import re, csv, time, json, requests, unicodedata

auth_token = ""


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
                'x-app-id': "ff0ccea8",
                'x-app-key': "605660a17994344157a78f518a111eda",
                'cache-control': "no-cache",
                'postman-token': "cdd9512f-4ad6-07f1-3fcd-09fdbe6ccb8a"
            }

            responseinstant = requests.request("GET", urlinstant, headers=headers, params=querystring)
            datainstant = responseinstant.text
            parsedinstant = json.loads(datainstant)

            for _data in parsedinstant['common']:
                headers = {
                    'x-app-id': "ff0ccea8",
                    'x-app-key': "605660a17994344157a78f518a111eda",
                    'x-remote-user-id': "7a43c5ba-50e7-44fb-b2b4-bbd1b7d22632",
                    'Content-Type': "application/x-www-form-urlencoded",

                }

                url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
                body = {
                    'query': _data['tag_name'],
                    'timezone': 'US/Eastern',
                }
                responsefood = requests.request("POST", url, data=body, headers=headers)
                datafood = responsefood.text
                parsedfoodsdetails = json.loads(datafood)
                try:
                    for parsedfood in parsedfoodsdetails['foods']:
                        try:
                            numberrecords += 1
                            print(str(numberrecords) + " ]Brand: " + _data["tag_name"])
                            Restaurant = parsedfood['brand_name']
                            Food_Item = parsedfood['food_name']
                            Serving_Size = str(parsedfood['serving_qty']) + " " + str(parsedfood['serving_unit'])
                            if parsedfood['serving_weight_grams'] != "":
                                Serving_Size = Serving_Size + " ( " + str(parsedfood['serving_weight_grams']) + "g )"
                            Calories = round(parsedfood['nf_calories'], 1)
                            Calories_from_Fat = int(parsedfood['nf_total_fat']) * 9
                            Total_Fat = round(parsedfood['nf_total_fat'], 1)
                            Saturated_Fat = round(parsedfood['nf_saturated_fat'], 1)
                            Cholesterol = round(parsedfood['nf_cholesterol'], 1)
                            Sodium = round(parsedfood['nf_sodium'], 1)
                            Total_Carbohydrates = round(parsedfood['nf_total_carbohydrate'], 1)
                            Dietary_Fiber = round(parsedfood['nf_dietary_fiber'], 1)
                            Sugars = round(parsedfood['nf_sugars'], 1)
                            Proteins = round(parsedfood['nf_protein'], 1)
                            Vitamin_A = ''
                            Vitamin_C = ''
                            Calcium = ''
                            Iron = ''
                            Trans_Fat = ''

                            for _parsedfooddata in parsedfood['full_nutrients']:
                                if _parsedfooddata['attr_id'] == 318:
                                    Vitamin_A = _parsedfooddata['value']
                                if _parsedfooddata['attr_id'] == 401:
                                    Vitamin_C = _parsedfooddata['value']
                                if _parsedfooddata['attr_id'] == 301:
                                    Calcium = _parsedfooddata['value']
                                if _parsedfooddata['attr_id'] == 303:
                                    Iron = _parsedfooddata['value']
                                if _parsedfooddata['attr_id'] == 605:
                                    Trans_Fat = _parsedfooddata['value']

                            csv_writer.writerow(
                                [Restaurant, Food_Item, Serving_Size, Calories, Calories_from_Fat, Total_Fat,
                                 Saturated_Fat,
                                 Trans_Fat, Cholesterol, Sodium, Total_Carbohydrates, Dietary_Fiber, Sugars, Proteins,
                                 Vitamin_A, Vitamin_C, Calcium, Iron])
                        except Exception:
                            pass  # or you could use 'continue'
                except Exception:
                    pass  # or you could use 'continue'
            data_to_file.close()


if __name__ == '__main__':
    main()

