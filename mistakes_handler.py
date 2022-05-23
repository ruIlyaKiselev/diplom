from nerus import load_nerus

docs = load_nerus('nerus_lenta.conllu.gz')
doc = next(docs)
print(doc)