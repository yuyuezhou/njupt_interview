from using_baidu_webapi import get_token, recognize
from methods_for_correction import save_file, read_file
from operation_for_vocabularylib import read_xls_file_return, str_of_result, addition_pinyin, save_xls_file
from methods_for_correction import correct_txt_with_info,user_correct

"""基于领域文本的自动纠错系统后端的主函数 by michael"""

"""1）首先使用using_baidu_WebApi模块来完成识别过程，并且得到txt文件"""

#voice_filename = r"D:\MyRepository\njupt_interview\测试样例和词库\cs音频(单词）\cs1.wav"            # 音频文件名称，必要的时候要写绝对地址
voice_filename = r"D:\MyRepository\njupt_interview\测试样例和词库\第二次测试音频\新录音 2.wav"
uncorrected_txt_filename = r"D:\MyRepository\njupt_interview\测试样例和词库\仅识别未纠错\just_from_api.txt"  # 没有纠错的文本的文件路径
rate = 16000                                # 音频文件的码率
form = 'wav'                                # 音频文件的格式

signal = open(voice_filename, "rb").read()  # 以二进制读取文件
token = get_token()                         # 获取网页的token
first_result = recognize(signal, rate, token, form)  # 得到网页翻译的结果
print('网页识别的结果为：' + first_result)                                  # 打印的到的语音结果
save_file(uncorrected_txt_filename, first_result)

"""2）将保存的网页识别的结果进行纠错"""

"""2.1）首先，对给定的领域文本库进行处理，方便后续纠错的使用"""

source_filename = r"D:\\MyRepository\\njupt_interview\\测试样例和词库\\症状实验.xls" # 原始库文件的绝对地址
vocabulary_filename = r"D:\MyRepository\njupt_interview\测试样例和词库\pinyin_for_lib_tone.xls"  # 可供比对的单词库（带音调）
vocabulary_filename_2 = r"D:\MyRepository\njupt_interview\测试样例和词库\pinyin_for_lib.xls"  # 可供比对的单词库（不带音调）

result_1 = read_xls_file_return(source_filename)    #读取xls文件,并返回出结果
result_2 = str_of_result(result_1)  #把得到的列表文件中的元素从列表转化到字符串，并处理字符串可以直接被pinyin模块识别
result_3 = addition_pinyin(result_2, len(result_2),1) #得到一个有症状名和对应拼音的列表,返回这个列表
save_xls_file(result_3, vocabulary_filename)  # 保存生成的可供对比的单词库(带音调)

result_3 = addition_pinyin(result_2, len(result_2),2)
save_xls_file(result_3, vocabulary_filename_2)

"""2.2)开始纠错"""

"""2.2.1)首先读取pinyin_for_lib库的文件的内容，然后转化为字典来进一步处理"""
py = read_xls_file_return(vocabulary_filename)  # 读取可供对比的单词库内容
py_dic = dict(py)                              # 把得到的列表字典化

py = read_xls_file_return(vocabulary_filename_2)  # 读取可供对比的单词库内容
py_dic_2 = dict(py)

"""2.2.2)开始进行文本纠错"""
uncorrected_txt_filename = r"D:\MyRepository\njupt_interview\测试样例和词库\仅识别未纠错\just_from_api.txt"  # 没有纠错的文本的文件路径
final_filname = r"D:\MyRepository\njupt_interview\测试样例和词库\仅识别未纠错\result_final.txt"             # 纠错后文本的文件路径
uncorrected_txt = read_file(uncorrected_txt_filename)
final_txt = correct_txt_with_info(uncorrected_txt, py_dic,py_dic_2)
print("文中需要纠错的词汇为："+str(final_txt['need_change']))
print('自动纠错的结果为：' + str(final_txt['word']))
print('经过自动纠错后的全文：' + final_txt['text'])
print("其他推荐纠错的词汇为："+str(final_txt['user_change']))


answer = input("是否许可上述推荐纠错？ Y/N")
user_correct(answer,final_txt['text'],py_dic_2,final_txt['word'])
if answer == 'N':
    print('纠错个数为: ' + str(final_txt['num']))


"""2.2.3)保存纠错的结果"""
result_dic = {'纠错后的结果为：': final_txt['text'],
              '涉及到的领域词汇个数为: ': str(final_txt['num']),
              '这些领域词汇有：': str(final_txt['word'])}
txt = ''
for key, value in result_dic.items():
    txt = txt + key + value + '\n'
save_file(final_filname, txt)
