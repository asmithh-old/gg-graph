import csv, pandas as pd, ast, numpy as np, mediacloud, json, itertools, random, time
all_story_ids = []
api_key = '1418b32a4e8140745240fa0b855060963c9939749bdd5562ee1b62590660b0fb'
mc = mediacloud.api.AdminMediaCloud(api_key)
with open('stories.csv') as f:
    content = f.readlines()
    for i in content:
        try:
            all_story_ids.append(ast.literal_eval(i.split(',')[0]))
        except:
            pass

acceptable_short_words = {'a', 'i', 'u', 'I', 'A'}
bigrams = {}
global_bigrams = {}
count = 0
all_story_ids = random.sample(all_story_ids, 200)
for story_id in all_story_ids:
    print count
    count += 1
    try:
        story_bigrams = []
        print 'getting sentences'
        for k in mc.storyCoreNlpList(story_id)[0]['corenlp'].keys():
            tokens = mc.storyCoreNlpList(story_id)[0]['corenlp'][k]['corenlp']['sentences'][0]['tokens']
            where = 0
            for i in tokens:
                if len(i['word']) == 1 and i['word'] not in acceptable_short_words:
                    del tokens[where]
                where += 1

            story_bigrams += [(a['word'], b['word']) for a,b in itertools.izip(tokens, tokens[1:])]

        print 'making bigrams'
        bigrams[story_id] = {b: story_bigrams.count(b) for b in story_bigrams}
        for b in story_bigrams:
            global_bigrams[b] = True
        print 'done'

    except:
        print story_id
    print
    print
print global_bigrams
print bigrams.keys()


#[ x if x%2 else x*100 for x in range(1, 10) ]
all_story_vectors = []
story_vector_to_id = {}
for story_id in bigrams.keys():
    print story_id in bigrams
    story_vector = [bigrams[story_id][b] if b in bigrams[story_id] else 0 for b in global_bigrams.keys()]
    all_story_vectors.append(story_vector)
    story_vector_to_id[story_vector] = story_id
with open('gg_ngrams_data_2.csv', 'w') as f:
    f.write(str(all_story_vectors))
    f.write('\n')
    f.write(str(global_bigrams.keys()))
    f.write('\n')
    f.write(str(story_vector_to_id))
