#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：dacong time:2019/4/3

#map search
BEIJING,CHANGCHUN,MULUMUQI,WUHAN,GUANGZHOU,SHENZHEN,BANKOK,SHANGHAI,NEWYOUR = "BEIJING,CHANGCHUN,MULUMUQI,WUHAN,GUANGZHOU,SHENZHEN,BANKOK,SHANGHAI,NEWYOUR".split(",")
connection = {
    CHANGCHUN:{BEIJING},
    MULUMUQI:{BEIJING},
    BEIJING:{MULUMUQI,CHANGCHUN,WUHAN,SHENZHEN,NEWYOUR},
    NEWYOUR:{BEIJING,WUHAN},
    WUHAN:{SHANGHAI,BEIJING,GUANGZHOU},
    GUANGZHOU:{WUHAN,BANKOK},
    SHENZHEN:{WUHAN,BANKOK},
    BANKOK:{SHENZHEN,GUANGZHOU},
    SHANGHAI:{NEWYOUR,WUHAN}
}
import networkx as nx
import matplotlib.pyplot as plt
graph = connection
g = nx.Graph(graph)
#nx.draw(g)
#plt.show(g)

def nagivator(start,destination,connection_graph):
    pathes = [[start]]
    seen = set()
    while pathes:
        path = pathes.pop(0)
        froniter = path[-1]
        # print('i am stand in {}'.format(froniter))

        if froniter in seen:continue      #avoidance of repetition
        successors = connection_graph[froniter]

        for s in successors:
            # print('\t -----i am look forward {}'.format(s))
            if s == destination:
                path.append(s)
                return path
            else:
                pathes.append(path+[s])
        pathes = sorted(pathes,key=len)  #choose the nearest way
        seen.add(froniter)
def show_route(routes):               #show the route
    print('-->'.join(routes))
if __name__ == '__main__':
    show_route(nagivator(WUHAN,BANKOK,connection))


# isalpha() 方法检测字符串是否只由字母组成；startswith() 方法用于检查字符串是否是以指定子字符串开头
def is_variable(pat):
    return pat.startswith('?') and all(s.isalpha() for s in pat[1:])


# isalpha() returns True if all characters in the strings are alphabets
# startwith('x') returns True if the characters srartwith x

def pat_match(pattern, saying):
    if not pattern or not saying: return []

    if is_variable(pattern[0]):
        return [(pattern[0], saying[0])] + pat_match(pattern[1:], saying[1:])
    else:
        if pattern[0] != saying[0]:
            return []
        else:
            return pat_match(pattern[1:], saying[1:])


def pat_to_dict(patterns):
    return {k: ' '.join(v) if isinstance(v, list) else v for k, v in patterns}


def subsitite(rule, parsed_rules):
    if not rule: return []
    return [parsed_rules.get(rule[0], rule[0])] + subsitite(rule[1:], parsed_rules)


pattern = 'I want ?X'.split()
saying = "I want holiday".split()
got_pattern = pat_match(pattern, saying)
subsitite(pattern, pat_to_dict(got_pattern))
# print(subsutite(pattern,pat_to_dict(got_pattern)),pat_to_dict(got_pattern))

# print(pat_match("?X greater than ?Y".split(), "3 greater than 2".split()))

# print(pat_match(pattern,saying))
# print(' '.join(subsutite(pattern,pat_to_dict(got_pattern))))
defined_patterns = {
    "I need ?X": ["Image you will get ?X soon", "Why do you need ?X ?"],
    "My ?X told me something": ["Talk about more about your ?X", "How do you think about your ?X ?"]
}

##Task_one
"""
please implement the code, to get the response as followings:

    >>> get_response('I need iPhone') 
    >>> Image you will get iPhone soon
    >>> get_response("My mother told me something")
    >>> Talk about more about your monther.
"""


def get_response(saying, pat_dic=defined_patterns):
    import random
    if not saying: return "please input the saying:"
    response_list = []
    for k, v in pat_dic.items():
        got_pattern = pat_match(k.split(), saying.split())
        if got_pattern:
            pat_response = pat_dic.get(k)
            for r in pat_response:
                response_list.append(' '.join(subsutite(r.split(), pat_to_dict(got_pattern))))
        else:
            continue
    if response_list:
        return random.choice(response_list)
    else:
        return "sorry,u have say nothing ,pleast input the sayings"


"""
Segment Match
我们上边的这种形式，能够进行一些初级的对话了，但是我们的模式逐字逐句匹配的， "I need iPhone" 和 "I need ?X" 可以匹配，但是"I need an iPhone" 和 "I need ?X" 就不匹配了，那怎么办？

为了解决这个问题，我们可以新建一个变量类型 "?*X", 这种类型多了一个星号(*),表示匹配多个

首先，和前文类似，我们需要定义一个判断是不是匹配多个的variable
"""


def is_pattern_segment(pattern):
    return pattern.startswith('?*') and all(a.isalpha() for a in pattern[2:])


def segment_match(pattern, saying):
    "Find the group of words in saying that matches with the ?*x variable in a given pattern."

    seg_pat, rest = pattern[0], pattern[1:]
    seg_pat = seg_pat.replace('?*', '?')  # change the ?* prefix into a single ?

    if not rest: return (seg_pat, saying), len(saying)

    for i, token in enumerate(saying):
        if rest[0] == token:
            return (seg_pat, saying[:i]), i  # note i = len(saying) :)

    return fail  # to prevent ?*X matches the whole of saying


from collections import defaultdict

fail = [True, None]


def pat_match_with_seg(pattern, saying):
    "Revise the previous pat_match in order to match ?*x variable with a segment of texts."
    if not pattern or not saying: return []
    pat = pattern[0]
    if is_variable(pat):
        return [(pat, saying[0])] + pat_match_with_seg(pattern[1:], saying[1:])
    elif is_pattern_segment(pat):
        if segment_match(pattern, saying) != fail:
            match, index = segment_match(pattern, saying)
            return [match] + pat_match_with_seg(pattern[1:], saying[index:])
        else:
            return segment_match(pattern, saying)
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    else:
        return fail
# Task2: