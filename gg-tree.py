import csv, pandas as pd, itertools, random, operator, numpy as np

links = pd.DataFrame.from_csv('story_links.csv')

#id_to_urls maps mediacloud story ids to the url of the story in question.
id_to_urls = {int(i):str(u) for i, u in itertools.izip(links['ref_stories_id'], links['ref_url'])}
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
linked_by_wikipedia = []
for i in forward_adj_list[338590484]:
    print i
    print id_to_urls[i]
    print id_to_media[int(i)]
    print
    linked_by_wikipedia.append(i)
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

##these are hand-collected sources (Alyssa's google results, restricted to Jan 2014-Dec 2014 + gamergate.me wiki "required reading")
#anti_gg = [281542462, 284121743, 288701642, 288708777, 288701686, 282522384, 288704748, 283469561, 338562091, 269817086, 283339223]
#pro_gg = [276942228, 268562597, 338653273, 281319215, 271211320, 338748505, 338518914, 338645262, 338518914, 338518984]


#maybe the node size should correspond to bit.ly clicks?
def random_walk(article, depth):
    visited = []
    while len(visited) < depth and article in backward_adj_list:
        #print article
        article = random.choice(backward_adj_list[article])
        visited.append(article)
    #print visited
    return visited

def not_dfs(article, num):
    visited = []
    queue = [article]
    while len(visited) < num and queue[0] in backward_adj_list:
        article = queue.pop(0)
        visited.append(article)
        queue.append(random.choice(backward_adj_list[article]))
        queue.append(random.choice(backward_adj_list[article]))
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

    return (visited_by, global_counts)

(anti_visited_by, global_anti) = do_random_walks(anti_gg, 10000, random_walk)
(pro_visited_by, global_pro) = do_random_walks(pro_gg, 10000, random_walk)


vertices = set(global_pro.keys() + global_anti.keys()+ anti_gg + pro_gg)
graph = 'digraph gg_digraph { \n'
edges = ''
nodes = ''
already_in_vertices = {}
for v in list(vertices):
    if v in global_pro and v in global_anti:
        pass
    else:
        if v not in global_pro:
            global_pro[v] = 0
        if v not in global_anti:
            global_anti[v] = 0
    total_count = global_anti[v] + global_pro[v]
    bitly_clicks = 1 + id_to_bitly_clicks[v]
    if v in anti_gg:
        color = 'cyan'
        total_count = 10000
        bitly_clicks = 10000
        print v
    elif v in pro_gg:
        color = 'cyan'
        total_count = 10000
        bitly_clicks = 10000
        print v
    else:
        total_count += 2
        if global_anti[v] > global_pro[v]:
            color = 'white'
        else:
            color = 'white'
    already_in_vertices[v] = True
    #total_count is number of times seen on 10000 random walks
    #bitly_clicks is number of bitly clicks on article according to media cloud (+1 so no node has 0 size)

    nodes += str(v) + ' [size = ' + str(bitly_clicks) + ', color = ' + color + ', label = ' + str(id_to_media[int(v)]) + ' ]; \n'


edges_in = {}
necessary_vertices = {}
for u in list(vertices):
    for v in list(vertices):
        if u in backward_adj_list and v in backward_adj_list[u]:
            edges += str(u) + ' -> ' + str(v) + '[color = black];\n'
            edges_in[(u,v)] = True
# for u in backward_adj_list.keys():
#     necessary_vertices[u] = True
#     for v in backward_adj_list[u]:
#         if (u,v) not in edges_in:
#             edges += str(u) + ' -> ' + str(v) + '[color = yellow];\n'
#             necessary_vertices[v] = True

# for v in undir_adj_list.keys():
#     if v not in already_in_vertices and v in necessary_vertices:
#         color = 'yellow'
#         total_count = 2
#         nodes += str(v) + ' [size = ' + str(np.log2(total_count)) + ', color = ' + color + ']; \n'
graph = graph + nodes + edges + '}'

#gg-shorter-walks.dot: size is by bit-ly clicks and manually chosen "representative" stories.
#gg-source-by-bitly-clicks: size by bit.ly clicks and representative stories are top bit.ly clicks
with open('gg-source-by-bitly-clicks.dot', 'w') as f:
    f.write(graph)
    f.close()


# print "anti"
# print
# for i in anti_visited_by.keys():
#     print id_to_urls[i]
#     print
#     #sorted(x.items(), key=operator.itemgetter(1))
#     for j in sorted(anti_visited_by[i].items(), key = operator.itemgetter(1)):
#         print id_to_urls[j[0]], j[1]
#     print
#     print
# print
# print




# for i in [id_to_urls[int(k[0])] for k in sorted(forward_adj_list.items(), key = lambda x:len(x[1]))[-20:]]:
#     print i

not_visited_yet = set(undir_adj_list.keys())
#
class node():
    def __init__(self, n):
        self.name = n
        self.children = []

def bfs(G, r):
    seen = set()
    tree = []
    Q = [node(r)]
    seen.add(r)
    while len(Q) > 0:
        v = Q.pop(0)
        v.children = G[v.name]
        tree.append(v)
        for i in G[v.name]:
            if i not in seen:
                Q.append(node(i))
                seen.add(i)
    return (tree, seen)

# while len(not_visited_yet) > 0:
#     x = random.choice(list(not_visited_yet))
#     (tree, seen)  =  bfs(undir_adj_list, x)
#     # for i in tree:
#     #     print i.name
#     #     print i.children
#     if len(tree) ==8413:
#         main = tree
#         #print len(tree)
#     for s in list(seen):
#         not_visited_yet.remove(s)

def bron_kerbosch(R,P,X):
    #finds all maximal cliques (each vertex v in a clique C is connected to all other vertices C\v in the clique.)
    if len(P) == 0 and len(X) == 0:
        if len(R) > 2:
            print R
            print
            print
        return R
    else:
        for v in list(P):
            bron_kerbosch(R | set([v]), P & undir_adj_list[v], X & undir_adj_list[v])
            P.remove(v)
            X = X | set([v])

#bron_kerbosch(set(), set(undir_adj_list.keys()), set())
