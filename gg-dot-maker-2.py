import csv, pandas as pd, itertools, random, operator, numpy as np

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

anti_gg = [270342400, 288709649, 288701709, 288694238, 305941274, 288694258, 286506094, 338442181, 284840342, 285912100, 338453214, 285115926, 288694138, 338559510, 287356856, 287298457, 338753805, 273217103]
pro_gg = [276942228, 288704530, 338463900, 288730845, 274189080, 288716268, 288750532, 288710343, 338667087, 338652557, 302460613, 317303871, 338645642]
source_articles = pro_gg + random.sample(anti_gg, 13)

visited_by = {i:{} for i in source_articles}
all_seen = set()
for i in source_articles:
    parent_pointers = {}
    depths = {}
    queue = [i]
    depths[i] = 0
    if i in backward_adj_list:
        queue += backward_adj_list[i]
        while queue and depths[queue[0]] < 6:
            node = queue.pop(0)
            all_seen.add(node)
            visited_by[i][node] = 10 - depths[node]
            #linear scaling of edge weight with closeness to start article -- higher weight for more closeness to start article.
            if node in backward_adj_list:
                for k in backward_adj_list[node]:
                    queue.append(k)
                    parent_pointers[k] = node
                    depths[k] =  depths[node] + 1
nodes = ''
edges = ''
graph = 'digraph gg_digraph { \n'
visited_by_gg = set()
visited_by_anti = set()
gg_link_strength = {}
anti_link_strength = {}
for i in list(all_seen):
    if i in source_articles and i in anti_gg:
        color = 'orange'
        size = 10
        for j in visited_by[i]:
            if j != i:
                edges += str(i) + ' -> ' + str(j) + '[color = black, weight = ' + str(visited_by[i][j]) + '];\n'
                visited_by_anti.add(j)
                if j not in anti_link_strength:
                    anti_link_strength[j] = 0
                anti_link_strength[j] = max(visited_by[i][j], anti_link_strength[j])
    elif i in source_articles and i in pro_gg:
        color = 'green'
        size = 10
        for j in visited_by[i]:
            if j != i:
                edges += str(i) + ' -> ' + str(j) + '[color = black, weight = ' + str(visited_by[i][j]) + '];\n'
                visited_by_gg.add(j)
                if j not in gg_link_strength:
                    gg_link_strength[j] = 0
                gg_link_strength[j] = max(visited_by[i][j], gg_link_strength[j])
    else:
        color = 'blue'
        size = 5
    nodes += str(i) + ' [size = ' + str(size) + ', color = ' + color + ', label = ' + str(id_to_media[int(i)]) + ' ]; \n'
#a = sorted(a, key=lambda x: x.modified, reverse=True)
p = sorted(list(visited_by_gg.intersection(visited_by_anti)), key = lambda x:gg_link_strength[x] + anti_link_strength[x], reverse = True)
y = sorted(list(visited_by_gg-visited_by_anti), key = lambda x:gg_link_strength[x], reverse = True)
n = sorted(list(visited_by_anti-visited_by_gg), key = lambda x:anti_link_strength[x], reverse = True)
print len(p)
print p
print
print len(y)
print y
print
print len(n)
print n
print
# print
# for i in p:
#     print id_to_urls[i]
#     print gg_link_strength[i]
#     print anti_link_strength[i]
#     print

graph = graph + nodes + edges + '}'
with open('gg-graph-better-sources.dot', 'w') as f:
    f.write(graph)
    f.close()
