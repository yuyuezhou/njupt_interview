import pypinyin
import pytrie
from pypinyin import Style
"""把初始的结果进行纠错"""


def read_file(fil):
    """
    把txt文件中的字符串读取出来
    :param fil: 文件的相对路径
    :return: 字符串
    """
    with open(fil, 'r+', encoding='utf-8') as file_object:
        """读取文件"""
        txt = file_object.read()
        return txt


def save_file(fil, txt):
    """

    :param fil: 要保存的文件路径
    :param txt: 要保存的文件
    :return: 没有return，如果保存错误返回error
    """
    with open(fil, 'w', encoding='utf-8') as file_object:
        file_object.write(txt)


def correct_for_word(fil, dic):
    """
    用来纠错单个单词的
    :param fil:输入一个单词
    :param dic:字典化的标准单词库
    :return:返回一个纠错好的单词
    """
    txt_py = pypinyin.slug(fil, errors='ignore')
    for key in dic.keys():
        if key == txt_py:
            fil = dic[key]
    return fil


def correct_for_txt(txt, dic):
    """
    修改文章中需要纠错的单词
    :param txt: 需要纠错的文本
    :param dic: 已经字典化的包含拼音的标准文本库
    :return: 纠错完成的句子
    """
    num = len(txt)  # 文本的长度
    txt1 = txt  # 得到文本的副本
    vocabulary_trie = pytrie.SortedStringTrie(dic)  # 生成拼音字典的匹配trie

    for value in range(0, num):
        tem_txt = txt[value:num]  # 得到子串
        tem_py = pypinyin.slug(tem_txt)  # 子串的拼音
        """开始处理子串,把子串作为参数，进行匹配"""
        result_match = vocabulary_trie.longest_prefix_value(tem_py, default='false')
        if result_match == 'false':
            continue
        else:
            need_change = tem_txt[0:len(result_match)]  # 需要被纠错的单词
            txt1 = txt1.replace(need_change, result_match)
    return txt1  # 返回纠错过的正确文本


def correct_txt_with_info(txt, dic,dic2):
    """
    修改文章中需要纠错的单词，然后告诉用户文章中专业词汇的个数和相关词汇
    :param txt: 需要纠错的文本
    :param dic: 字典化的标准库
    :return: 纠错过的文本和相关词汇信息
    """
    txt_num = len(txt)  # 文本的长度
    word_num = 0  # 被纠错的词汇个数，初始值为0
    need_change_list=[]#需要被自动纠错的词汇列表
    word_list = []  # 经过自动纠错的词汇列表，初始值为0
    user_change_list =[] # 需要经过用户确认才进行纠错的词汇列表
    value = 0  # 分片字符串，一开始从头开始分片
    txt1 = txt
    vocabulary_trie = pytrie.SortedStringTrie(dic)  # 生成拼音字典的匹配trie Trie，字典树，又称单词查找树，前缀树，是哈希树的变种
    vocabulary_trie_2 = pytrie.SortedStringTrie(dic2)
    #结点B为汉字，与其父结点A连接的边为B中汉字的拼音
    while value < txt_num:
        tem_txt = txt[value:txt_num]  # 得到字串
        tem_py = pypinyin.slug(tem_txt, style=Style.TONE)  # 获得字串的拼音（带音调）
        tem_py_2 = pypinyin.slug(tem_txt)  # 获得字串拼音（不带音调）
        # print("tem_py="+tem_py)
        """开始处理字串，把字串作为参数，进行匹配"""
        result_match = vocabulary_trie.longest_prefix_value(tem_py, default='false')  # 返回最长匹配边所对应的一系列结点，此处为带音调的匹配结果
        result_match_2 = vocabulary_trie_2.longest_prefix_value(tem_py_2, default='false')  # 不带音调的匹配结果
        #print("result_match=" + result_match_2)
        if result_match == 'false':
            value = value + 1
            continue
        else:
            #print("time+=====", time)
            need_change = tem_txt[0:len(result_match)]  # 需要被纠错的单词
            need_change_list.append(need_change)
            txt1 = txt1.replace(need_change, result_match)
            word_num = word_num + 1  # 领域词汇数量增加一个
            word_list.append(result_match)  # 领域词汇列表增加一个
            value = value + len(need_change)


    value=0
    txt_num_2=txt1
    while value < len(txt_num_2):
        tem_txt = txt[value:len(txt_num_2)]  # 得到字串
        tem_py_2 = pypinyin.slug(tem_txt)  # 获得字串拼音（不带音调）
        """开始处理字串，把字串作为参数，进行匹配"""
        result_match_2 = vocabulary_trie_2.longest_prefix_value(tem_py_2, default='false')  # 不带音调的匹配结果
        if result_match_2 == 'false':
            value = value + 1
            continue
        else:
            user_change = tem_txt[0:len(result_match_2)]  # 需要被纠错的单词
            user_change_list.append(user_change)
            # txt_num_2 = txt_num_2.replace(user_change, result_match_2)
            # word_num = word_num + 1  # 领域词汇数量增加一个
            # word_list.append(result_match)  # 领域词汇列表增加一个
            value = value + len(user_change)


    result = {'text': txt1, 'num': word_num, 'word': word_list,'need_change':need_change_list,'user_change':user_change_list,'final_txt':txt_num_2}
    return result

def user_correct(answer,txt,dic,word_list):
    if answer == 'Y':
        value = 0
        txt_num_2 = txt
        vocabulary_trie = pytrie.SortedStringTrie(dic)
        user_changed_list=[]
        while value < len(txt_num_2):
            tem_txt = txt[value:len(txt_num_2)]  # 得到字串
            tem_py = pypinyin.slug(tem_txt)  # 获得字串拼音（不带音调）
            """开始处理字串，把字串作为参数，进行匹配"""
            result_match = vocabulary_trie.longest_prefix_value(tem_py, default='false')  # 不带音调的匹配结果
            if result_match == 'false':
                value = value + 1
                continue
            else:
                user_change = tem_txt[0:len(result_match)]  # 需要被纠错的单词
                user_changed_list.append(user_change)
                txt_num_2 = txt_num_2.replace(user_change, result_match)
                word_list.append(result_match)  # 领域词汇列表增加一个
                value = value + len(user_change)

        result = {'text': txt_num_2, 'num': len(word_list)}
        print("纠错成功！")
        print("最终文本：\""+txt_num_2+"\"")
        print("共计纠错词汇个数："+str(len(word_list)))
    else:
        print("已拒绝推荐纠错，最终全文为：\""+txt+"\"")