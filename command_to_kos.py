import json
import random
import time
import pymorphy2
from enum import Enum

from config import list_of_product

list_of_actions = ["addItem", "addLoyalty", "cancel", "deletePosition", "deleteAll",
                   "deleteTransaction", "payment", "returnAddITem", "sellingMode", "setContact", "startPOS",
                   "stopPOS", "subTotal"]

list_of_commands = ["добавить", 87868]

morph = pymorphy2.MorphAnalyzer()


def find_product(text):
    text_words = text.split(' ')
    index = 0
    for prod in list_of_product:
        findProd = 0
        prod_words = prod.split(' ')
        for p_word in prod_words:
            p_word = morph.parse(p_word.lower())
            for p_parse in p_word:
                p_word_norm = p_parse.normal_form
                go_out = False
                for t_word in text_words:
                    t_word = morph.parse(t_word.lower())
                    for t_parse in t_word:
                        t_word_norm = t_parse.normal_form
                        if p_word_norm in t_word_norm:
                            findProd += 1
                            go_out = True
                            break
                    if go_out:
                        break
                if go_out:
                    break
        if findProd == len(prod_words):
            return index
        index += 1
    return None


class subType(str, Enum):
    Weight = 0
    Health = 1


class Contact:
    type = ""
    data = ""


def getDataFromKSO():
    return random.randint(0, 10000)


class ThereIsNoProductWithCurrentName(Exception):
    pass


def check_product_exist(text):
    product_id = find_product(text)
    if product_id:
        return product_id
    else:
        raise ThereIsNoProductWithCurrentName("Нет такого продукта!")


def make_action(command, support_object=0):
    data = {"eventId": "sco" + str(round(time.time()))}
    if "начать" in command[0]:
        data["action"] = "startPOS"
        data["timeout"] = getDataFromKSO()
    elif "добавить" in command[0]:
        data["action"] = "addItem"
        data["itemCode"] = check_product_exist(command[1])
        if len(command) > 2:
            data["quantity"] = int(command[2])
    elif "взвесить" in command[0]:
        data["action"] = "subscribe"
        data["frequency"] = 1000
        data["type"] = subType.Weight
    elif "закрыть" in command[0]:
        data["action"] = "cancel"
        if len(command) > 1:
            data["requestEventId"] = command[1]  # Должны получить от КСО
#    elif "добавить информация" in command[0]:  # Команда для добавления сигарет с мин розничной ценой
#        data["action"] = "extInfo"
#        data["requestEventId"] = command[1]  # Должны получить от КСО
#        data["info"] = command[2]
    elif "отменить" in command[0]:
        data["action"] = "deleteTransaction"
    # TODO: удлаить номер шо делать!!!
    # elif "удалить номер" in command[0]:
    #     data["action"] = "deletePosition"
    #     data["itemNumber"] = check_product_exist(command[1])
    elif "удалить" in command[0]:
        data["action"] = "deleteAll"
        data["itemCode"] = command[1]
    elif "далее" in command[0]:
        data["action"] = "subTotal"
    elif "лояльность" in command[0] or "купон" in command[0] or "пенсионер" in command[0]\
            or "вип" in command[0] or "сотрудник" in command[0] or "семья" in command[0]:
        data["action"] = "addLoyalty"
        data["itemCode"] = command[1]
        if len(command) > 2:
            data["type"] = command[2]
    elif "кобренд" in command[0]:
        data["action"] = "payment"
        data["amount"] = int(command[1])
        data["paymentType"] = command[2]
    elif "вернуться" in command[0]:
        data["action"] = "returnAddITem"
    elif "банковский" in command[0]:
        data["action"] = "payment"
        data["paymentType"] = "Card"
        if support_object:
            data["contacts"] = support_object
    elif "выручай" in command[0]:
        data["action"] = "payment"
        data["paymentType"] = "Loyalty"
        data["loyaltyRedemptionType"] = "Msr"
        if "штрихкод" in command[0]:
            data["loyaltyRedemptionType"] = "Mobile"
        if len(command) > 1:
            data["amount"] = int(command[1])
    elif "социальный" in command[0]:
        data["action"] = "payment"
        data["paymentType"] = "SocCard"
        if len(command) > 1:
            data["amount"] = int(command[1])
    elif "код" in command[0]:  # QR
        data["action"] = "payment"
        data["paymentType"] = "Qr"
        if support_object:
            data["contacts"] = support_object

    json_dump = json.dumps(data)
    print(json_dump)


# make_action(list_of_commands, 0)
# print(find_product("добавить много красных красных яблок", morph, list_of_product))
