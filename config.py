path = "/home/victor/PycharmProjects/virushack/"
filename = "text_to_command_conversion/model.txt"
filename_start = path+filename
filename_phrases = filename_start + '-phrases'
filename_bin = filename_start + '.bin'
filename_clusters = filename_start + '-clusters.txt'

# commands = ["начать", "добавить", "далее", "далее", "оплата", "банковской"]
# list_of_product = ["яблоки зеленые", "яблоки красные"]
working_commands = ["начать", "добавить", "взвесить", "закрыть", "отменить", "далее", "удалить", "банковский", "назад"]
similar_working_commands = {'начать': ['начни', "начните"]}

dict_of_product = {"яблоки": ["зеленые", "красные", "синие"], "арбузы": "большие", "слон": None, "торт": None}
list_of_hard_product = [item for item in dict_of_product if dict_of_product[item]]
list_of_easy_product = [item for item in dict_of_product if not dict_of_product[item]]
