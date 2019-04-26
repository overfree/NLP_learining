#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：dacong time:2019/4/15

grammer = """sentence => noun_phrase verb_phrase
noun_phrase =>Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article => 一个 | 这个
noun => 女人 | 篮球 | 桌子 | 小猫
verb => 看着 |坐在 | 听着 | 看见
Adj => 蓝色的 | 好看的 | 小小的 
"""
import random
def adj():return random.choice(["蓝色的","好看的","小小的"])
def noun():return random.choice("女人|篮球|桌子|小猫".split('|'))
def phrase_grammer(grammer_str,sep = '=>'):
    grammer = {}
    a = grammer_str.split('\n')
    for line in a:
        line = line.strip()
        if not line:continue
        target,rules = line.split(sep)
        grammer[target.strip()] = [i.split() for i in rules.split('|')]
    return grammer




def gene(grammar_parsed, target='sentence'):
    if target not in grammar_parsed: return target

    rule = random.choice(grammar_parsed[target])
    # print(grammar_parsed[target])
    return ''.join(gene(grammar_parsed, target=r) for r in rule if r != 'null')


if __name__ == '__main__':
    g = phrase_grammer(grammer)
    print(g)
    print(gene(g))