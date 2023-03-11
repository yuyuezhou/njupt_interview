# Project_Of_SRTP
基于语音识别的自动文本纠错系统

原博主：https://github.com/Little-Pr1nce/Project_Of_SRTP

在其基础上：  

2023-3-11  
更新了代码，优化了纠错逻辑：  
1.对同音错别字可以自动进行纠错 如“精神凡造”-->“精神烦躁”  
2.对不同音疑似错别字在请求用户同意后再进行纠错。如“一级一脑”-->询问用户是否替换-->用户同意-->"易急易恼“

2023-3-9  
使用前应该添加相关的模块，在命令行里面输入下列的代码（以后会增加，这是目前需要安装的模块）：
pip install requests
pip install pypinyin
pip install pytrie


