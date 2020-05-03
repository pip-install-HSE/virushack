import word2vec
from config import *
import pymorphy2
word = "собаки"

morph = pymorphy2.MorphAnalyzer()
model = word2vec.load(filename_start)

norm_word = morph.parse(word)[0]
r_norm_word = f"{norm_word.normal_form}_{norm_word.tag.POS}"

print(r_norm_word)
indexes, metrics = model.similar(r_norm_word)
test = model.generate_response(indexes, metrics).tolist()
for i in test:
    print(i[0])
