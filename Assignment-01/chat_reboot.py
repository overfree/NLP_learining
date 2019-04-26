#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：dacong time:2019/4/24



import jieba
import random
# from collections import defaultdict

fail = [True,None]

def is_variable(pat):
    """check the input string is a pattern variable ?x or not"""
    return pat.startswith('?x') and all(s.isalpha() for s in pat[1:])
def is_pattern_segment(pattern):
    "Check if the input string is a segment pattern variable ?*x"
    return pattern.startswith('?*') and all(s.isalpha() for s in pattern[2:])
def pat_to_dic(patterns):
    return {k:''.join(v) if isinstance(v,list) else v for k,v in patterns}
def substitute(pattern,pat_dic):
    if not pattern:return []
    return [pat_dic.get(pattern[0],pattern[0])] + substitute(pattern[1:],pat_dic)
def pat_match_with_seg(pattern,saying):
    if not pattern or not saying:return []
    pat = pattern[0]
    if is_variable(pat):
        return [(pat,saying[0])] + pat_match_with_seg(pattern[1:],saying[1:])
    elif is_pattern_segment(pat):
        match,index = segment_match(pattern,saying)
        return [match] + pat_match_with_seg(pattern[1:],saying[index:])
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:],saying[1:])
    else:
        return fail

def segment_match(pattern, saying):
    "Find the group of words in saying that matches with the ?*x variable in a given pattern."

    seg_pat,rest = pattern[0], pattern[1:]
    seg_pat = seg_pat.replace('?*', '?')  # change the ?* prefix into a single

    if not rest: return (seg_pat, saying), len(saying)

    for i, token in enumerate(saying):
        if rest[0] == token:
            return (seg_pat, saying[:i]), i  # note i = len(saying)

    return fail  # modified - to prevent ?*X matches the whole of saying


def get_response(saying,pat_dic):
    if not saying or not pat_dic:return []
    response_list = []
    saying_token = ' '.join(jieba.cut(saying)).split()# split the saying into tokens
    for key,value in pat_dic.items():
        key_str = ' '.join(jieba.cut(key))
        key_str_token = key_str.replace("? * x","?*x").replace("? * y", "?*y").replace("? * z", "?*z").split()

        got_patterns = pat_match_with_seg(key_str_token,saying_token)
        if not None in got_patterns:
            pat_response = pat_dic[key]
            for r in pat_response:
                r_token = ' '.join(jieba.cut(r)).replace("? x", "?x").replace("? y", "?y").replace("? z", "?z").split()
                response_list.append(''.join(substitute(r_token,pat_to_dic(got_patterns))))
        else:continue
    if response_list:
        return random.choice(response_list)
    else:
        return "对不起，我不知道你在说什么，可以再说明白一点吗？"




rules_dic = {
    '?*x机器人?*y':['你为什么要提机器人的事情？', '你为什么觉得机器人要解决你的问题？'],
    '?*x总是?*y':['你能想到一些其他情况吗?', '例如什么时候?', '你具体是说哪一次？', '真的---总是吗？'],
    '?*x和?*y一样?*z':['你觉得?z有什么问题吗?', '?z会对你有什么影响呢?'],
    '?*x我是?*y':['真的吗？', '?x想告诉你，或许我早就知道你是?y', '你为什么现在才告诉我你是?y'],
    '?*x就像?*y':['你觉得?x和?y有什么相似性？', '?x和?y真的有关系吗？', '怎么说？'],
    '?*x如果?*y':['你真的觉得?y会发生吗？', '你希望?y吗?', '真的吗？如果?y的话', '关于?y你怎么想？']
}


if __name__ == '__main__':
    print(get_response('你们我是有人样',rules_dic))

"""
问题1
编写一个程序, get_response(saying, response_rules)输入是一个字符串 + 我们定义的 rules，例如上边我们所写的 pattern， 输出是一个回答。

问题2
改写以上程序，将程序变成能够支持中文输入的模式。 提示: 你可以需用用到 jieba 分词

问题3
多设计一些模式，让这个程序变得更好玩，多和大家交流，看看大家有什么好玩的模式
【暂无新的想法和模式】
问题4
这样的程序有什么优点？有什么缺点？你有什么可以改进的方法吗？
【优点：可以自主定义规则，规则驱动，便于修改规则
  缺点：模式固定，不能够变通，而且对于特殊标点、空格等容错性较差
】
什么是数据驱动？数据驱动在这个程序里如何体现？
【网络查到的解释：数据驱动是通过移动互联网或者其他的相关软件为手段采集海量的数据，
将数据进行组织形成信息，之后对相关的信息进行整合和提炼，在数据的基础上经过训练和拟合形成自动化的决策模型；
在这个程序中定了了规则，通过将输入数据与规则的匹配整合，自动推送出对应的整合后结果；
】
数据驱动与 AI 的关系是什么？
【AI是构建能够自动对数据生成对应合理的输出内容的模型的过程，数据驱动就是一种规则，能够对外部数据经过
规则的处理反馈出整合的结果，但是AI是需要数据驱动加上知识的驱动一同推动的，所以数据驱动是AI的必要非充分条件。
】
"""