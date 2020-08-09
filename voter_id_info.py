import word_retriever as wr
import ImageAlignment as ia
import re
import os


def get_card_type(doc):
    set1 = ['elector', 'father', 'age', 'sex']
    set2 = ['name', 'father']
    set3 = ['address', 'thiscardcanbeused', 'governmentprogrammes']
    set4 = ['address', 'age', 'sex', 'note', 'merepossession']
    card_type = ""

    count = 0
    for word in set1:
        loc = ia.find_word_location(doc, word)
        loc1 = ia.find_word_location(doc, 'father')
        if loc is not None:
            count += 1
            if count == 3 and loc1 is not None:
                card_type = "oldCard_1"
                break

    count = 0
    for word in set2:
        loc = ia.find_word_location(doc, word)
        loc1 = ia.find_word_location(doc, 'age')
        loc2 = ia.find_word_location(doc, 'sex')
        if loc is not None and loc1 is None and loc2 is None:
            count += 1
            if count == 2:
                card_type = "newCard_1"
                break

    if card_type == "":
        count = 0
        for word in set3:
            loc = ia.find_word_location(doc, word)
            if loc is not None:
                count += 1
                if count == 3:
                    card_type = "oldCard_2"
                    break
        if card_type == "":
            count = 0
            for word in set4:
                loc = ia.find_word_location(doc, word)
                if loc is not None:
                    count += 1
                    if count == 5:
                        card_type = "newCard_2"
                        break
    return card_type

# a = get_card_type(docmnt)
# print(a)

def get_card_info(doc, text):
    ct = get_card_type(doc)
    card_info_dict = {}
    loc_list = []
    epicno_pattern = r'[A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
    if ct == "oldCard_1":
        keyword_list = ['name', 'father', 'sex', 'age']
        try:
            epicno_values = re.findall(epicno_pattern, text)
            # print(epicno_values)
            card_info_dict['EPIC_number'] = epicno_values[0]
        except Exception:
            card_info_dict['EPIC_number'] = ""
        for word in keyword_list:
            loc = ia.find_word_location(doc, word)
            if loc is not None:
                loc_list.append(loc)
        for word in keyword_list:
            try:
                card_info_dict["Elector's Name"] = ia.text_within(doc, loc_list[0].vertices[2].x+10, loc_list[0].vertices[0].y-10, loc_list[0].vertices[2].x+500, loc_list[0].vertices[2].y+10).replace(':', '').replace('\n', '')
            except Exception:
                card_info_dict["Elector's Name"] = ""
            try:
                card_info_dict["Father's Name"] = ia.text_within(doc, loc_list[1].vertices[2].x+75, loc_list[1].vertices[0].y-10, loc_list[1].vertices[2].x+500, loc_list[1].vertices[2].y+10).replace(':', '').replace('\n', '')
            except Exception:
                card_info_dict["Father's Name"] = ""
            try:
                loc = ia.find_word_location(doc, 'female')
                if loc is None:
                    card_info_dict["Sex"] = 'Male'
                else:
                    card_info_dict["Sex"] = 'Female'
            except Exception:
                card_info_dict["Sex"] = ""
            try:
                card_info_dict["Age"] = ia.text_within(doc, loc_list[3].vertices[2].x+100, loc_list[3].vertices[0].y-10, loc_list[3].vertices[2].x+300, loc_list[3].vertices[2].y+10).replace(':', '').replace('\n', '').replace(' ', '')
            except Exception:
                card_info_dict["Age"] = ""
        # print(card_info_dict)
    elif ct == "oldCard_2":
        loc = ia.find_word_location(doc, 'address')
        if loc is not None:
            try:
                card_info_dict["Address"] = ia.text_within(doc, loc.vertices[0].x, loc.vertices[2].y, loc.vertices[2].x+300, loc.vertices[2].y+100).replace('\n', '')
            except Exception:
                card_info_dict["Address"] = ""
        # print(card_info_dict)
    elif ct == "newCard_1":
        keyword_list = ['name', 'father']
        try:
            epicno_values = re.findall(epicno_pattern, text)
            # print(epicno_values)
            card_info_dict['EPIC_number'] = epicno_values[0]
        except Exception:
            card_info_dict['EPIC_number'] = ""
        for word in keyword_list:
            loc = ia.find_word_location(doc, word)
            if loc is not None:
                loc_list.append(loc)
        loc1 = ia.find_word_location(doc, 'mother')
        if len(loc_list) == 1 and loc1 is not None:
            loc_list.append(loc1)
        for word in keyword_list:
            try:
                card_info_dict["Elector's Name"] = ia.text_within(doc, loc_list[0].vertices[2].x+10, loc_list[0].vertices[0].y-10, loc_list[0].vertices[2].x+500, loc_list[0].vertices[2].y+10).replace(':', '').replace('\n', '')
            except Exception:
                card_info_dict["Elector's Name"] = ""
            if loc1 is None:
                try:
                    card_info_dict["Father's Name"] = ia.text_within(doc, loc_list[1].vertices[2].x+30, loc_list[1].vertices[0].y-10, loc_list[1].vertices[2].x+500, loc_list[1].vertices[2].y+10).replace(':', '').replace('\n', '')
                except Exception:
                    card_info_dict["Father's Name"] = ""
            else:
                try:
                    card_info_dict["Mother's Name"] = ia.text_within(doc, loc_list[1].vertices[2].x+40, loc_list[1].vertices[0].y-10, loc_list[1].vertices[2].x+500, loc_list[1].vertices[2].y+10).replace(':', '').replace('\n', '')
                except Exception:
                    card_info_dict["Mother's Name"] = ""
        # print(card_info_dict)
    elif ct == "newCard_2":
        loc1 = ia.find_word_location(doc, 'female')
        loc2 = ia.find_word_location(doc, 'male')
        try:
            if loc1 is None and loc2 is not None:
                card_info_dict['Sex'] = "Male"
            elif loc1 is not None:
                card_info_dict['Sex'] = "Female"
            elif loc1 is None and loc2 is None:
                loc = ia.find_word_location(doc, 'sex')
                card_info_dict['Sex'] = ia.text_within(doc, loc.vertices[2].x+40, loc.vertices[0].y-10, loc.vertices[2].x+300, loc.vertices[2].y+10).replace('/', '').replace('\n', '')
        except Exception:
            card_info_dict['Sex'] = ""
        loc = ia.find_word_location(doc, 'address')
        try:
            adrs1 = ia.text_within(doc, loc.vertices[2].x+10, loc.vertices[0].y-10, loc.vertices[2].x+400, loc.vertices[2].y+10).replace('\n', ' ')
            adrs2 = ia.text_within(doc, loc.vertices[0].x-20, loc.vertices[2].y, loc.vertices[2].x+400, loc.vertices[2].y+50).replace('\n', ' ')
            card_info_dict['Address'] = adrs1 + adrs2
        except Exception:
            card_info_dict['Address'] = ""
        loc1 = ia.find_word_location(doc, 'birth')
        loc2 = ia.find_word_location(doc, 'age')
        try:
            if abs(loc1.vertices[0].y - loc2.vertices[0].y) < 5 and abs(loc1.vertices[2].y - loc2.vertices[2].y )< 5:
                card_info_dict['Date Of Birth'] = ia.text_within(doc, loc1.vertices[2].x+15, loc1.vertices[0].y-10, loc1.vertices[2].x+200, loc1.vertices[2].y+10).replace(' ', '').replace('\n', '')
                card_info_dict['Age'] = ia.text_within(doc, loc2.vertices[2].x+80, loc2.vertices[0].y-10, loc2.vertices[2].x+200, loc2.vertices[2].y+5).replace(' ', '').replace('\n', '')
            else:
                card_info_dict['Date Of Birth'] = ia.text_within(doc, loc1.vertices[2].x+20, loc1.vertices[0].y-10, loc1.vertices[2].x+300, loc1.vertices[2].y+10).replace(' ', '').replace('\n', '')
                card_info_dict['Age'] = ia.text_within(doc, loc2.vertices[2].x+10, loc2.vertices[0].y-10, loc2.vertices[2].x+200, loc2.vertices[2].y+5).replace(' ', '').replace('\n', '')
        except Exception:
            card_info_dict['Date Of Birth'] = ""
            card_info_dict['Age'] = ""
        # print(card_info_dict)

    return card_info_dict


img = "img_fldr/"  # folder which contains test imgs. 
for filename in os.listdir(img):
    print(filename, "  ---")
    res, dcmnt, txt = wr.data_retrieve(img+filename)
    data = get_card_info(dcmnt, txt)
    print(data)
    print("-----------------------------------------------")
