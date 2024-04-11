import gspread


class store():
    #When games % 6 = 4
    test1=  [{
            "title": "title1",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title2",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title3",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title4",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title5",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title6",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title7",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title8",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title9",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title10",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        }    ]

    #When games % 6 = 0
    test2 = [{
            "title": "title1",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title2",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title3",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title4",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title5",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title6",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title7",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title8",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title9",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title10",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title11",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        } 
        
        ]

        #when games < 6
    test3 = [{
            "title": "title1",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title2",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title3",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title4",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        }]

        #When pages > 2 
    test4 = [{
            "title": "title1",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title2",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title3",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title4",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title5",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title6",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title7",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title8",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title9",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title10",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title11",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        }, {
            "title": "title12",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title13",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title14",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        }, {
            "title": "title15",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title16",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title17",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title18",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title19",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title20",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title21",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title22",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title23",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        }, {
            "title": "title24",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title25",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        },
        {
            "title": "title26",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        }, {
            "title": "title27",
            "dev": "dev1",
            "price": 1,
            "tag1": "tag",
            "tag2": "",
            "tag3":"tag",
            "tag4":"tag"
        }                
        
        ]

    def __init__():
        pass

    def sort_price():
        pass

    def get_games_sharing_tag(self, selected):
        #return list of games with the same category 
        pass

    def get_game(input):
        #gets specific game based on searchbar
        pass

    def get_ID():
        pass

    def get_title():
        pass

    def get_dev():
        pass

    def get_price():
        pass

    def get_tags():
        pass

    def generate_ID():
        pass
    