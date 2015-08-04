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
# all_story_ids = []
# with open('gg-top-250.txt') as f:
#     content = f.readlines()
#     for i in content:
#         all_story_ids.append(i[4:13])
all_story_ids = [288701647, 280836834, 274189080, 338571589, 288710106, 338605572, 288709649, 283259932, 338686009, 288750141, 288694340, 338728940, 288710219, 288736850, 288730708, 338535026, 288748160, 284596369, 288749405, 288701616, 338658501, 283628232, 282522384, 270169879, 338582319, 338700597, 288694091, 288709968, 288748407, 288749445, 288707977, 288750499, 338715556, 288750556, 338553289, 288746473, 283249659, 338583062, 288716327, 288704530, 288704631, 284121743, 338571411, 288702101, 288703647, 268562597, 288708777, 338669761, 288737511, 338451738, 338581293, 338668846, 92198720, 338441568, 288750448, 280721787, 338469262, 288710547, 270456736, 288723385, 288710076, 338685901, 338600921, 274563326, 267535864, 338604545, 338547718, 338604594, 269271628, 288703417, 288732265, 338604660, 288750733, 288737450, 288747123, 338555060, 288701686, 282383620, 288701709, 288747797, 269039403, 288744246, 76105611, 338488665, 288736603, 338645399, 296457113, 288713117, 288735154, 288750524, 288716268, 338685439, 288710656, 288694290, 338562067, 288710168, 271859230, 338635827, 288701496, 279147789, 271860243, 338562180, 338707638, 267099255, 288730865, 268602409, 271822587, 338453246, 281588529, 288744242, 338518847, 288710458, 288710020, 288737709, 283991116, 338677229, 288715251, 288750593, 288701442, 338464314, 288744570, 288716925, 288748163, 338652812, 281764533, 338453175, 288723641, 288704203, 288749269, 288704225, 288709956, 288723694, 270342400, 271903546, 268991343, 271316374, 338585496, 288701887, 338406987, 288750546, 338466271, 288717318, 338654242, 338602543, 283207221, 338729020, 288724041, 288710363, 288737591, 288737086, 288744260, 338592632, 288743819, 288701837, 338433470, 288737760, 288737785, 288723497, 288736700, 200985278, 288701645, 288737073, 288730445, 274202965, 288737121]
words = []
for story_id in all_story_ids:
    print count
    count += 1
    try:
        story_bigrams = []
        print 'getting sentences'
        for k in mc.storyCoreNlpList(story_id)[0]['corenlp'].keys():
            tokens = mc.storyCoreNlpList(story_id)[0]['corenlp'][k]['corenlp']['sentences'][0]['tokens']
            where = 0
            #print tokens
            for i in tokens:
                if len(i['word']) == 1 and i['word'] not in acceptable_short_words:
                    del tokens[where]
                where += 1
                words.append(i['word'])
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
#print words

#[ x if x%2 else x*100 for x in range(1, 10) ]
all_story_vectors = []
#story_vector_to_id = {}
for story_id in bigrams.keys():
    print story_id in bigrams
    story_vector = [bigrams[story_id][b] if b in bigrams[story_id] else 0 for b in global_bigrams.keys()]
    all_story_vectors.append(story_vector)
    #story_vector_to_id[story_vector] = story_id
with open('gg-text-data-mutual.txt', 'w') as f:
    f.write(str(words))
    f.write('/n')
    # f.write(str(all_story_vectors))
    # f.write('\n')
    # f.write(str(global_bigrams.keys()))
    # f.write('\n')
    #f.write(str(story_vector_to_id))
