#!/usr/bin/env python3
"""
AI-Humanizer-ZH - 中文AI文本人类化工具
专门去除AI生成文本的机械感和公式化表达，使其更自然流畅、更像人类写作风格
基于Humanizer-zh项目理念优化，支持多种风格转换和批量处理
"""

import argparse
import random
import re
import os
import sys
from typing import List, Dict, Set

# 常见AI词汇警示列表
AI_WORDS = {
    '此外', '至关重要', '深入探讨', '强调', '持久的', '增强', '培养', '获得',
    '突出', '相互作用', '复杂', '复杂性', '格局', '关键性的', '展示', '织锦',
    '证明', '强调', '宝贵的', '充满活力的', '无缝', '直观', '强大', '革命性',
    '创新', '发展', '趋势', '未来', '挑战', '机遇', '重要', '核心', '关键',
    '基础', '关键', '主要', '重点', '核心', '首要', '重要', '必要', '不可或缺'
}

# 中文替换规则 - 基于Humanizer-zh的优化
ZH_REPLACEMENTS = {
    # 正式表达转口语化
    '综上所述': ['总的来说', '总而言之', '整体来说', '直白点说'],
    '由此可见': ['看得出来', '这说明', '显而易见', '如此说来'],
    '众所周知': ['大家都知道', '众所周知', '谁都明白', '不用说'],
    '显而易见': ['很明显', '明摆着', '一眼就能看出来', '显然'],
    '不可或缺': ['少不了', '很重要', '不可少', '缺不了'],
    '至关重要': ['非常重要', '特别关键', '极其重要', '重中之重'],
    '与此同时': ['与此同时', '同时', '也', '并且'],
    '值得一提的是': ['值得一提的是', '要特别提一下', '有一点要注意', '这里要提一下'],
    '换句话说': ['换句话说', '也就是说', '说白了', '简单点说'],
    '例如': ['比如', '例如', '比方说', '举个例子'],
    '因此': ['所以', '因此', '故而', '这就导致'],
    '因为': ['因为', '由于', '鉴于', '就因为'],
    '但是': ['不过', '但是', '可是', '然而'],
    '而且': ['而且', '并且', '还', '甚至'],
    '然而': ['然而', '但是', '不过', '可'],
    '首先': ['首先', '第一', '先', '第一步'],
    '其次': ['其次', '第二', '接着', '下一步'],
    '最后': ['最后', '最终', '说到底', '最后一步'],
    
    # AI常见套话替换
    '在本文中': ['在这篇文章里', '在这里', '本文中', '在这篇内容里'],
    '我们将讨论': ['咱们来聊聊', '我们要讨论', '这里谈谈', '我们聊一聊'],
    '本文旨在': ['这篇文章主要想', '本文主要', '这篇文章旨在', '本文目的是'],
    '基于以上分析': ['根据上面的分析', '基于以上分析', '从上文分析来看', '综合以上分析'],
    '这表明': ['这说明', '这表明', '这表示', '这显示'],
    '研究表明': ['有研究显示', '研究表明', '研究发现', '据研究'],
    '数据显示': ['数据显示', '数据表明', '统计显示', '据数据统计'],
    
    # 机械感词汇替换
    '进行': ['做', '进行', '实施', '开展'],
    '开展': ['展开', '开展', '推进', '搞起来'],
    '实施': ['推行', '实施', '执行', '落实'],
    '实现': ['达到', '实现', '完成', '达成'],
    '完成': ['做完', '完成', '搞定', '结束'],
    '提供': ['给', '提供', '给予', '供应'],
    '获得': ['得到', '获得', '拿到', '取得'],
    '具有': ['有', '具有', '具备', '拥有'],
    '存在': ['有', '存在', '具备', '有很多'],
    '包含': ['包括', '包含', '涵盖', '里面有'],
    '涉及': ['牵扯到', '涉及', '关系到', '和...有关'],
    '使用': ['用', '使用', '运用', '采用'],
    '利用': ['借助', '利用', '使用', '充分利用'],
    '通过': ['通过', '借助', '经由', '靠'],
    '使得': ['让', '使得', '致使', '导致'],
    '导致': ['导致', '造成', '引起', '使得'],
    '引起': ['引发', '引起', '导致', '招来'],
    '产生': ['产生', '形成', '带来', '引发'],
    '发生': ['发生', '出现', '产生', '爆发'],
    '出现': ['出现', '显现', '发生', '冒出来'],
    
    # AI三连词替换
    '无缝、直观和强大': ['简单好用', '功能强大', '易于操作', '用户友好'],
    '高效、稳定和可靠': ['运行稳定', '高效可靠', '性能稳定', '表现出色'],
    '创新、突破和发展': ['不断创新', '持续发展', '突破进步', '稳步前进'],
    '挑战、机遇和未来': ['机遇与挑战', '未来发展', '前景展望', '发展前景']
}

# 中文句子开头变化
ZH_SENTENCE_STARTERS = [
    '你知道吗，', '有意思的是，', '我发现，', '其实，', '说真的，',
    '老实说，', '不得不说，', '值得注意的是，', '有趣的是，', '让人惊讶的是，',
    '你猜怎么着，', '我觉得吧，', '要我说，', '依我看，', '据我所知，'
]

# 口语化填充词
ZH_FILLER_WORDS = ['呢', '啊', '吧', '啦', '嘛', '嘿', '嗯', '哦', '呀']

# 否定式排比检测模式
NEGATIVE_PATTERNS = [
    r'这不仅仅是.*更是', r'这不只是.*而是', r'不仅仅是.*而且是',
    r'不仅是.*更是', r'不只是.*而是', r'并非.*而是'
]

def detect_ai_patterns(text: str) -> Dict[str, int]:
    """检测文本中的AI写作模式"""
    patterns = {
        'ai_words': 0,              # AI词汇使用频率
        'negative_parallelism': 0,  # 否定式排比
        'triple_structure': 0,      # 三段式结构
        'excessive_formality': 0,   # 过度正式
        'empty_phrase': 0,          # 空泛短语
        'exaggeration': 0,          # 过度夸张
        'vague_attribution': 0,     # 模糊归因
    }
    
    # 检测AI词汇
    words = re.findall(r'[\u4e00-\u9fff]+', text)
    for word in words:
        if word in AI_WORDS:
            patterns['ai_words'] += 1
    
    # 检测否定式排比
    for pattern in NEGATIVE_PATTERNS:
        matches = re.findall(pattern, text)
        patterns['negative_parallelism'] += len(matches)
    
    # 检测三段式结构
    triple_matches = re.findall(r'([，,；;]).*?\1.*?\1', text)
    patterns['triple_structure'] += len(triple_matches)
    
    # 检测空泛短语
    empty_phrases = ['发展趋势', '未来展望', '挑战与机遇', '核心竞争力', '重要意义']
    for phrase in empty_phrases:
        if phrase in text:
            patterns['empty_phrase'] += 1
    
    # 检测过度夸张
    exaggeration_phrases = ['革命性', '突破性', '颠覆性', '无与伦比', '独一无二']
    for phrase in exaggeration_phrases:
        if phrase in text:
            patterns['exaggeration'] += 1
    
    # 检测模糊归因
    vague_phrases = ['研究表明', '数据显示', '专家认为', '据报道', '众所周知']
    for phrase in vague_phrases:
        if phrase in text:
            patterns['vague_attribution'] += 1
    
    return patterns

def apply_zh_replacements(text: str, variability: str = 'medium') -> str:
    """应用中文文本替换规则"""
    for old, new_list in ZH_REPLACEMENTS.items():
        if old in text:
            # 根据variability选择替换方式
            if variability == 'low':
                # 低变化：使用第一个替换词
                text = text.replace(old, new_list[0])
            elif variability == 'medium':
                # 中变化：随机选择替换词
                text = text.replace(old, random.choice(new_list))
            else:  # high
                # 高变化：使用更口语化的替换
                text = text.replace(old, random.choice(new_list[-2:]) if len(new_list) >= 2 else new_list[0])
    return text

def reduce_ai_words(text: str, variability: str = 'medium') -> str:
    """减少AI词汇的使用"""
    # 随机替换部分AI词汇
    words = text.split()
    for i, word in enumerate(words):
        # 检查是否包含AI词汇
        for ai_word in AI_WORDS:
            if ai_word in word and random.random() < 0.3 + {'low': 0, 'medium': 0.2, 'high': 0.4}[variability]:
                # 根据上下文选择合适的替换
                replacements = {
                    '创新': ['出新招', '玩新花样', '搞创新'],
                    '发展': ['变好', '进步', '往前走'],
                    '重要': ['要紧', '关键', '有用'],
                    '复杂': ['绕人', '麻烦', '不简单'],
                    '趋势': ['风向', '走向', '势头']
                }
                if ai_word in replacements:
                    words[i] = words[i].replace(ai_word, random.choice(replacements[ai_word]))
                break
    
    return ' '.join(words)

def fix_negative_parallelism(text: str) -> str:
    """修复否定式排比结构"""
    # 替换否定式排比
    replacements = {
        r'这不仅仅是(.*?)更是(.*?)': lambda m: f'这不只是{m.group(1)}，更是{m.group(2)}',
        r'这不只是(.*?)而是(.*?)': lambda m: f'其实这不是{m.group(1)}，而是{m.group(2)}',
        r'不仅仅是(.*?)而且是(.*?)': lambda m: f'这不仅是{m.group(1)}，而且是{m.group(2)}',
        r'不仅是(.*?)更是(.*?)': lambda m: f'这不只是{m.group(1)}，还是{m.group(2)}',
        r'不只是(.*?)而是(.*?)': lambda m: f'其实它不是{m.group(1)}，而是{m.group(2)}',
        r'并非(.*?)而是(.*?)': lambda m: f'这不是{m.group(1)}，而是{m.group(2)}'
    }
    
    for pattern, replacer in replacements.items():
        matches = re.findall(pattern, text)
        for match in matches:
            text = re.sub(pattern, replacer, text)
    
    return text

def vary_chinese_sentence_lengths(text: str, variability: str = 'medium') -> str:
    """调整中文句子长度变化"""
    # 按中文标点分割
    sentences = re.split(r'([。！？；.!?;])', text)
    
    # 重新组合句子和标点
    combined_sentences = []
    for i in range(0, len(sentences)-1, 2):
        combined_sentences.append(sentences[i] + sentences[i+1])
    
    if variability == 'low':
        return ''.join(combined_sentences)
    
    # 根据可变性调整句子长度
    varied_sentences = []
    for sentence in combined_sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # 处理中文长句
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', sentence))
        
        # 长句拆分为短句
        if chinese_chars > 40 and variability in ['medium', 'high']:
            # 按逗号、分号等分割
            clauses = re.split(r'([，,；;、])', sentence)
            if len(clauses) > 3:
                # 拆分成多个句子
                new_sentences = []
                current = ''
                for i, part in enumerate(clauses):
                    current += part
                    chinese_count = len(re.findall(r'[\u4e00-\u9fff]', current))
                    
                    # 每15-25个汉字分一个句子
                    if chinese_count > 15 and (i + 1) % 2 == 0:
                        new_sentences.append(current.strip() + '。')
                        current = ''
                
                if current:
                    new_sentences.append(current.strip() + '。')
                varied_sentences.extend(new_sentences)
                continue
        
        # 合并过短的句子
        elif chinese_chars < 10 and variability in ['high'] and varied_sentences:
            # 检查前一个句子
            prev_sentence = varied_sentences[-1]
            prev_chars = len(re.findall(r'[\u4e00-\u9fff]', prev_sentence))
            
            if prev_chars < 30:  # 前一个句子也不太长
                varied_sentences[-1] = prev_sentence.rstrip('。！？；.!?;') + '，' + sentence.lstrip('。！？；.!?;')
                continue
        
        varied_sentences.append(sentence)
    
    return ''.join(varied_sentences)

def add_chinese_natural_variations(text: str, variability: str = 'medium', style: str = 'casual') -> str:
    """增加中文自然的语言变化"""
    
    # 随机添加口语化开头
    sentences = text.split('。')
    if sentences and len(sentences) > 1:
        for i in range(len(sentences)-1):
            if random.random() < 0.2 and variability in ['medium', 'high'] and style in ['casual', 'creative']:
                if not any(elem in sentences[i] for elem in ZH_SENTENCE_STARTERS):
                    sentences[i] = random.choice(ZH_SENTENCE_STARTERS) + sentences[i]
        text = '。'.join(sentences)
    
    # 添加口语化填充词
    if random.random() < 0.4 and style in ['casual', 'creative']:
        words = re.split(r'([。！？；,.!?;])', text)
        for i in range(len(words)-1):
            if random.random() < 0.1 and variability in ['medium', 'high']:
                if re.match(r'[\u4e00-\u9fff]+', words[i]):
                    words[i] += random.choice(ZH_FILLER_WORDS)
        text = ''.join(words)
    
    # 替换过度使用的词语
    if variability in ['medium', 'high']:
        synonyms = {
            '非常': ['特别', '十分', '极其', '超级', '格外'],
            '很多': ['不少', '许多', '好多', '一大堆', '挺多'],
            '重要': ['关键', '要紧', '重要', '重大', '紧要'],
            '有趣': ['有意思', '有趣', '好玩', '逗乐', '搞笑'],
            '简单': ['容易', '简单', '轻松', '小菜一碟', '好弄'],
            '困难': ['不容易', '困难', '麻烦', '费劲', '难办'],
            '喜欢': ['偏爱', '喜欢', '爱好', '钟情', '待见'],
            '讨厌': ['反感', '讨厌', '不喜欢', '厌恶', '烦'],
            '好': ['不错', '好', '棒', '优秀', '牛'],
            '坏': ['糟糕', '坏', '差劲', '不行', '糟']
        }
        
        for old, new_list in synonyms.items():
            if old in text and random.random() < 0.3:
                text = text.replace(old, random.choice(new_list))
    
    return text

def adjust_chinese_punctuation(text: str, style: str = 'casual') -> str:
    """调整中文标点"""
    if style in ['casual', 'creative']:
        # 添加更多口语化标点
        text = text.replace('；', '，')
        text = text.replace('：', '：')
        # 增加感叹号使用频率
        sentences = text.split('。')
        if len(sentences) > 3:
            for i in range(len(sentences)-1):
                if random.random() < 0.2:
                    sentences[i] = sentences[i] + '！'
        text = '。'.join(sentences)
    
    return text

def humanize_chinese_text(text: str, style: str = 'casual', variability: str = 'medium') -> str:
    """将中文AI文本转换为更自然的人类风格"""
    # 1. 检测AI模式并调整
    patterns = detect_ai_patterns(text)
    
    # 如果AI特征明显，增加变化程度
    if sum(patterns.values()) > 5 and variability == 'low':
        variability = 'medium'
    
    # 2. 基础替换
    text = apply_zh_replacements(text, variability)
    
    # 3. 修复否定式排比
    text = fix_negative_parallelism(text)
    
    # 4. 减少AI词汇使用
    text = reduce_ai_words(text, variability)
    
    # 5. 根据风格调整
    if style == 'casual':
        text = text.replace('，', '，')
        text = text.replace('。', '。')
    elif style == 'formal':
        pass  # 保持正式风格
    elif style == 'creative':
        text = add_chinese_natural_variations(text, variability='high', style='creative')
    
    # 6. 调整句子长度
    text = vary_chinese_sentence_lengths(text, variability)
    
    # 7. 增加自然变化
    text = add_chinese_natural_variations(text, variability, style)
    
    # 8. 调整标点
    text = adjust_chinese_punctuation(text, style)
    
    # 9. 最终清理
    text = re.sub(r'\s+', ' ', text)  # 合并多余空格
    text = re.sub(r'([。！？；])\1+', r'\1', text)  # 去除重复标点
    
    return text.strip()

def main():
    parser = argparse.ArgumentParser(description='AI-Humanizer-ZH - 中文AI文本人类化工具')
    parser.add_argument('text', nargs='?', help='要处理的中文文本')
    parser.add_argument('--input', help='输入文件路径')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--style', choices=['casual', 'formal', 'creative'], default='casual',
                       help='输出风格: casual/口语化, formal/正式, creative/创意')
    parser.add_argument('--variability', choices=['low', 'medium', 'high'], default='medium',
                       help='文本变化程度: low/低, medium/中, high/高')
    parser.add_argument('--preserve', nargs='*', help='需要保留的关键词或短语')
    parser.add_argument('--debug', action='store_true', help='显示调试信息')
    
    args = parser.parse_args()
    
    # 获取输入文本
    if args.input and os.path.exists(args.input):
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print('请提供文本输入或指定输入文件')
        return
    
    # 显示调试信息
    if args.debug:
        print('📊 正在检测AI写作模式...')
        patterns = detect_ai_patterns(text)
        print('📋 AI模式检测结果:')
        for pattern, count in patterns.items():
            print(f'  {pattern.replace("_", " ").capitalize()}: {count}')
        print()
    
    # 保存需要保留的内容
    preserved = {}
    if args.preserve:
        for i, phrase in enumerate(args.preserve):
            placeholder = f'__PRESERVED_{i}__'
            preserved[placeholder] = phrase
            text = text.replace(phrase, placeholder)
    
    # 处理文本
    print(f'✅ 正在处理文本（风格: {args.style}, 变化程度: {args.variability}）...')
    humanized_text = humanize_chinese_text(text, args.style, args.variability)
    
    # 恢复保留的内容
    if args.preserve:
        for placeholder, phrase in preserved.items():
            humanized_text = humanized_text.replace(placeholder, phrase)
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(humanized_text)
        print(f'💾 处理后的文本已保存到 {args.output}')
    else:
        print('\n✨ 处理后的文本：')
        print('=' * 60)
        print(humanized_text)
        print('=' * 60)
        
        # 显示一些统计信息
        original_length = len(text)
        humanized_length = len(humanized_text)
        print(f'\n📊 统计信息：')
        print(f'  原始文本长度: {original_length} 字符')
        print(f'  处理后长度: {humanized_length} 字符')
        if original_length > 0:
            change_percent = ((humanized_length - original_length) / original_length) * 100
            print(f'  长度变化: {change_percent:+.1f}%')  

if __name__ == '__main__':
    main()
