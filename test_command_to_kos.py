import pymorphy2

dict_of_product = {"яблоки": ["зеленые", "красные", "синие"], "арбузы": "большие", "слон": None, "торт": None}
list_of_hard_product = [item for item in dict_of_product if dict_of_product[item]]
list_of_easy_product = [item for item in dict_of_product if not dict_of_product[item]]

morph = pymorphy2.MorphAnalyzer()


def find_product(text, list_of_product):
    text_words = text.split(' ')
    index = 1
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
            return [index, prod]
        index += 1
    return None


def easy_find_product(text):
    product = find_product(text, list_of_easy_product)
    if product:
        print(product)
    else:
        product = find_product(text, list_of_hard_product)
        if product:
            product.append(find_product(text, dict_of_product[product[1]]))
            if product[2]:
                product[1] += ' ' + product[2][1]
                product[0] = product[0]*10 + product[2][0]
                product.pop(2)
                print(product)
            else:
                print("Выбери продукт:" + str(dict_of_product[product[1]]))