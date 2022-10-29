# -*- coding:utf-8 -*-
import requests
import random
import time
import hashlib

SAVE = 1

translate_url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
user_agent = '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52'


def get_translation_result(parameters):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': '252',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=778355149@42.92.128.222; OUTFOX_SEARCH_USER_ID_NCOO=4739596.930131668; ___rl__test__cookies=1667028026560',
        'Host': 'fanyi.youdao.com',
        'Origin': 'https://fanyi.youdao.com',
        'Referer': 'https://fanyi.youdao.com/',
        'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
        'X-Requested-With': 'XMLHttpRequest'
    }

    response = requests.post(url=translate_url, headers=headers, data=parameters)
    results = response.json()['translateResult'][0]
    result = ""
    for one_query in results:
        result += one_query['tgt']
    return result


def get_parameters_by_python(query, translate_from, translate_to):
    lts = str(int(time.time() * 1000))                                # 以毫秒为单位的 13 位时间戳
    salt = lts + str(random.randint(0, 9))                            # 13 位时间戳+随机数字，生成 salt 值
    sign = "fanyideskweb" + query + salt + "Ygy_4c=r#e#4EX^NUGUc5"    # 拼接字符串组成 sign
    sign = hashlib.md5(sign.encode()).hexdigest()                     # 将 sign 进行 MD5 加密，生成最终 sign 值
    bv = hashlib.md5(user_agent.encode()).hexdigest()                 # 对 UA 进行 MD5 加密，生成 bv 值
    parameters = {
        'i': query,
        'from': translate_from,
        'to': translate_to,
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'lts': lts,
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    return parameters

#考虑到从pdf复制的文字会存在大量换行符，因此，该函数将删除输入的换行符
def delete_line_breaks_cn(str):
    str = str.replace('\n','')
    return str.replace(' ','')

def delete_line_breaks_en(str):
    return str.replace('\n','')

#功能一 英汉互译。word为需要翻译的内容；save为SAVE时，会将翻译结果保存在同目录下的result.txt文件中，否则，通过print函数输出
def en_cn_translate(words,save):
    translate_from = translate_to = 'AUTO'
    query = delete_line_breaks_en(words)
    params = get_parameters_by_python(query, translate_from, translate_to)
    result = get_translation_result(params)
    if save == 1:
        writer = open("result.txt","w")
        writer.write(result)
        writer.close()
        print("Success!")
    else:
        print(result)
        print("Success!")
#功能二 汉译英译汉降重。word为需要降重的内容；save为SAVE时，会将翻译结果保存在同目录下的result.txt文件中，否则，通过print函数输出
def duplicate_reduce(words,save):
    translate_from = translate_to = 'AUTO'
    query = delete_line_breaks_cn(words)
    #汉译英
    params_en = get_parameters_by_python(query, translate_from, translate_to)
    result_en = get_translation_result(params_en)

    params_cn = get_parameters_by_python(result_en, translate_from, translate_to)
    result = get_translation_result(params_cn)
    if save == 1:
        writer = open("result.txt", "w")
        writer.write(result)
        writer.close()
        print("Success!")
    else:
        print(result)
        print("Success!")


if __name__ == '__main__':
    query = '''
        区块链被称为下一代的价值互联网,是一种去中心化新兴加密货币的基础系统架构。自 2008 年中本聪提出区块链一
        词以来,区块链因其本身的不可篡改、可溯源、去中心化等特性而逐渐受到人们的广泛关注,其中的两个典型代表为比特币区块
        链系统和以太坊区块链系统。但是在目前已有的文献资料中,大多是将已有的区块链技术应用到实际生活中,而对区块链的底
        层的实现介绍较为模糊,应将区块链从实际的应用中抽离出来,并通过比特币区块链系统和以太坊区块链系统的设计思想及其
        关键技术来了解区块链的工作原理。文中主要从区块链设计的密码学原理、共识算法、数据存储结构等方面来详细介绍区块链
        技术的基础架构,并针对比特币白皮书和以太坊黄皮书中较模糊的概念进行了补充,从而为后面的读者提供更加深入的研究参
        考。最后,介绍了区块链目前的应用现状和展望。
        '''

    # en_cn_translate(query,SAVE)
    duplicate_reduce(query,SAVE)













