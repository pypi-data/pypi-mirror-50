# --*-- coding: utf-8 --*--

# 翻译器（翻译类型）
BAIDU = "baidu"
GOOGLE = "google"
TRANS_TYPE_LIST = [BAIDU, GOOGLE]


# 百度翻译秘钥ID
APP_ID = '20190619000308802' #你的appid
SECRET_KEY = 'gAuBfGBhy7uCY37JtlYk' #你的密钥

# 翻译方式
CRAWL = "crawl" # 爬虫方式
API = "api"     # 接口方式
TRANS_MODE_LIST = [CRAWL, API]

# 状态码和状态信息
SUCCESS_STATUE_CODE = "1000"                                # 成功
PARAM_STATUE_CODE = "1002"                                  # 必填参数为空
EXCEPT_STATU_CODE = "1003"                                  # 其它异常情况
INVALID_TRANS_TYPE = "INVALID TRANSLATE TYPE"               # 传入的翻译类型有误或不合法
INVALID_TRANS_MODE = "INVALID TRANSLATE MODE"               # 传入的翻译方式有误或不合法
INVALID_SOURCE_LANG = "INVALID SOURCE(from_lang) LANGUAGE"             # 传入的源语言参数有误
INVALID_DEST_LANG = "INVALID DESTINATION(to_lang) LANGUAGE"          # 传入的译文语言参数有误
INVALID_PARAMETER = "FROM_LANG OR TO_LANG OR QUERY_TEXT IS NONE"    # 传入的必填参数有误
NO_SUCH_MODE = "PLEASE SWITCH TO ANOTHER TRANSLATE MODE"            # 无该翻译方式，可切换其它翻译方式
LANG_ERROR = "FROM_LANG AND TO_LANG SHOULD'T BE THE SAME."  # 源语言和译文语言不应该一样
LANG_TYPE_ERROR = "FROM_LANG OR TO_LANG TYPE ERROR, SHOULD BE STRING"               # 源语言和译文语言
INVALID_LANG_ERROR = "INVALID SOURCE(from_lang) OR DESTINATION(to_lang) LANGUAGE"   # 不合法的源语言和译文语言

# 网络错误相关
NETWORK_ERRER = "NETWORK ERROR"                             # 网络错误
NETWORK_MOVED = "Moved"

SUCCESS = "SUCCESS"

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

# 支持语言列表
LANGUAGES = ["auto", "zh", "en", "yue", "wyw", "jp", "kor", "fra", "spa", "th", "ara", "ru", "pt", "de", "it", "el", "nl", "pl", "bul", "est", "dan", "fin", "cs", "rom", "slo", "swe", "hu", "cht", "vie"]

LANGMAP = {
    'zh': 'zh-cn',  # 中文
    'vie': 'vi',    # 越南语
    'cht': 'zh-tw', # 繁体中文
    'swe': 'sv',    # 瑞典语
    'rom': 'ro',    # 罗马尼亚语
    'fra': 'fr',    # 法语
    'jp': 'ja',     # 日语
    'kor': 'ko',    # 韩语
    'spa': 'es',    # 西班牙语
    'ara': 'ar',    # 阿拉伯语
    'bul': 'bg',    # 保加利亚语
    'est': 'et',    # 爱沙尼亚语
    'dan': 'da',    # 丹麦语
    'fin': 'fi',    # 芬兰语
    'sol': 'sl'     # 斯洛文尼亚语
}

# LANGMAP的key和value转换
LANGMAP_REVERSED = dict(map(reversed, LANGMAP.items()))