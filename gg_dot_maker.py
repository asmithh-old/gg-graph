import csv, pandas as pd, itertools, random, operator, numpy as np, math, matplotlib.pyplot as plt

##TODO: kick out duplicates from controversy
##(come up with consistent, defensible set of rules to kick out things that are probably duplicates)
##wikipedia; articles w/ high inlinks;
#low-hanging fruit: sort all stories by title & look for duplicate titles
##if something has 0 inlinks, it's considered lower priority.

links = pd.DataFrame.from_csv('story_links.csv')

#id_to_urls maps mediacloud story ids to the url of the story in question.
id_to_urls = {int(i):str(u) for i, u in itertools.izip(links['ref_stories_id'], links['ref_url'])}
#id_to_media maps a specific news story to its parent media outlet.
id_to_media = {int(i):str(m) for i, m in itertools.izip(links['ref_stories_id'], links['ref_media_name'])}

for i in links.iterrows():
    id_to_urls[int(i[0])] = i[1].to_dict()['source_url']
    #print i
refers = pd.DataFrame.from_csv('stories.csv')
for i in refers.iterrows():
    id_to_urls[int(i[0])] = i[1].to_dict()['url']
    #print i[1].to_dict().keys()
    id_to_media[int(i[0])] = i[1].to_dict()['media_name']
id_to_bitly_clicks = {s[0]:c for s, c in itertools.izip(refers.iterrows(), refers['bitly_click_count'])}

forward_adj_list = {}
backward_adj_list = {}
undir_adj_list = {}
#forward is the references pointing to the articles that referred to them.
#backward is the referring articles pointing to all things they reference.
#intuitively, the arrows in this graph point forward in time
#(from previously written articles to articles written later that refer to them.)

for s, r in itertools.izip(links.iterrows(), links['ref_stories_id']):
    #s is the referrer; r is the reference.
    if s[0] not in backward_adj_list:
        backward_adj_list[int(s[0])] = [int(r)]
    else:
        backward_adj_list[int(s[0])].append(int(r))

    if r not in forward_adj_list:
        forward_adj_list[int(r)] = [int(s[0])]
    else:
        forward_adj_list[int(r)].append(int(s[0]))

for i in list(set(forward_adj_list.keys() + backward_adj_list.keys())):
    if i in forward_adj_list and i in backward_adj_list:
        undir_adj_list[i] = set(forward_adj_list[i] + backward_adj_list[i])
    else:
        if i in forward_adj_list:
            undir_adj_list[i] = set(forward_adj_list[i])
        elif i in backward_adj_list:
            undir_adj_list[i] = set(backward_adj_list[i])


for i in forward_adj_list.keys():
    forward_adj_list[i] = tuple(forward_adj_list[i])



#maybe the node size should correspond to bit.ly clicks?
def random_walk(article, depth):
    visited = []
    while len(visited) < depth and article in backward_adj_list:
        #print article
        article = random.choice(backward_adj_list[article])
        visited.append(article)
    #print visited
    return visited

def do_random_walks(starts, num_walks, walk_fn):
    visited_by = {}
    global_seen = []
    for i in starts:
        seen = []
        for j in range(0, num_walks):
            seen += walk_fn(i, 5)
        res = {}
        for a in seen:
            if a in res:
                res[a] += 1
            else:
                res[a] = 1
        global_seen += seen
        visited_by[i] = res
    global_counts = {}
    for i in global_seen:
        if i in global_counts:
            global_counts[i] += 1
        else:
            global_counts[i] = 1
    #visited_by[x] is list of articles visited from that article x
    #global_counts[x] is number of times the markov chain saw that article x
    return (visited_by, global_counts)

num_markov_walks = 15000
source_articles = [288751132, 288751132, 269817086, 338488742, 338596025, 338667087, 287570873, 316017805, 305462143, 288730454, 338742345, 270342400, 288723335, 338652557, 288710049, 338508914, 288694479, 288709649, 338753805, 305256266, 284596369, 286506094, 276942228, 338464020, 302460613, 317303871, 273217103, 338645642, 270169879, 306444385, 288737425]
(visited_by, global_counts) = do_random_walks(source_articles, num_markov_walks, random_walk)

vertices = set(global_counts.keys() + source_articles)
graph = 'digraph gg_digraph { \n'
edges = ''
nodes = ''
already_in_vertices = {}
bitly_vs_markov = {}
total_markov_clicks = 0
total_bitly_clicks = 0
colors = {}
for v in list(vertices):
    #total_count is number of times seen on 10000 random walks
    #bitly_clicks is number of bitly clicks on article according to media cloud (+1 so no node has 0 size)
    if v in source_articles:
        colors[v] = 'orange'
        if v not in global_counts:
            global_counts[v] = 0
        if v not in backward_adj_list:
            backward_adj_list[v] = []

        total_count = num_markov_walks * (1.0/(1.0 + float(len(backward_adj_list[v])))) + global_counts[v]

        bitly_clicks = id_to_bitly_clicks[v]
        size = num_markov_walks
    else:
        colors[v] = 'pink'
        total_count = global_counts[v]
        size = total_count
        bitly_clicks = id_to_bitly_clicks[v]
    total_markov_clicks += total_count
    if math.isnan(bitly_clicks):
        total_bitly_clicks += 0.0
        bitly_vs_markov[v] = (total_count, 1.0)
        print v
    elif math.isnan(total_count):
        pass
    else:
        total_bitly_clicks += bitly_clicks
        bitly_vs_markov[v] = (total_count, bitly_clicks + 1.0)

normed_bitly_v_markov = {v: (float(bitly_vs_markov[v][0])/float(total_markov_clicks), float(bitly_vs_markov[v][1])/float(total_bitly_clicks)) for v in bitly_vs_markov.keys()}
bitly_markov_ratio = [np.log2(normed_bitly_v_markov[v][1] /normed_bitly_v_markov[v][0]) for v in normed_bitly_v_markov.keys()]
std =  np.std(bitly_markov_ratio)
mean = np.mean(bitly_markov_ratio)
print std
print mean
for v in normed_bitly_v_markov.keys():
    if np.log2(normed_bitly_v_markov[v][1]/normed_bitly_v_markov[v][0]) > mean + std:
        print v
        print id_to_urls[v]
        print id_to_media[v]
        print
for v in colors.keys():
    size = np.log2(normed_bitly_v_markov[v][1]/normed_bitly_v_markov[v][0]) + 1.0 + 13.7080865796
    color = colors[v]
    nodes += str(v) + ' [size = ' + str(size) + ', color = ' + color + ', label = ' + str(id_to_media[int(v)]) + ' ]; \n'
    already_in_vertices[v] = True
edges_in = {}
necessary_vertices = {}
for u in list(vertices):
    for v in list(vertices):
        if u in backward_adj_list and v in backward_adj_list[u]:
            edges += str(u) + ' -> ' + str(v) + '[color = black];\n'
            edges_in[(u,v)] = True
graph = graph + nodes + edges + '}'

#making article probability distribution
#P(a): what is the probability of encountering a in a random walk through top articles & their links? (markov)
#P(b): what is the probability of encountering b given distribution of bit.ly clicks?
print total_bitly_clicks
normed_markov = [normed_bitly_v_markov[v][0] for v in sorted(normed_bitly_v_markov.keys())]
normed_bitly = [normed_bitly_v_markov[v][1] for v in sorted(normed_bitly_v_markov.keys())]
#normed_bitly is borked
dot = np.sum([m * b for m, b in itertools.izip(normed_markov, normed_bitly)])
print dot
magnitude_markov = math.sqrt(np.sum([m*m for m in normed_markov]))
print magnitude_markov
magnitude_bitly = math.sqrt(np.sum([b*b for b in normed_bitly]))
print magnitude_bitly
print math.acos(dot / (magnitude_markov * magnitude_bitly))
#gg-shorter-walks.dot: size is by bit-ly clicks and manually chosen "representative" stories.
#gg-source-by-bitly-clicks: size by bit.ly clicks and representative stories are top bit.ly clicks
with open('gg-graph-markov-to-bitly.dot', 'w') as f:
    f.write(graph)
    f.close()
