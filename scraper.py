from bs4 import BeautifulSoup
import requests, vobject, re, os, itertools

PATH = os.path.join(os.path.dirname(__file__), 'main', 'static', 'files', 'txt')

RE_NAME = r'<strong class=\"text-lg font-bold text-gray-800\">\s*(.*?)\s*</strong>'
RE_NUMBER = r'(?<=تلفن همراه:</span>\n<span class=\"text-gray-700\">)[۰-۹]+'

NAMES_LIST, NUMBERS_LIST = list(), list()

MEN = 'https://hub.23055.ir/search-official-expert?p_p_id=NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=1&p_p_col_count=2&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_fname=&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_lname=&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_search=1&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_prvnc=23&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_cty=&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_gnd=1&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_cnumber=&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_fld=1217&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_delta=12&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_keywords=&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_advancedSearch=false&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_andOperator=true&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_resetCur=false&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_cur='
WOMEN = 'https://hub.23055.ir/search-official-expert?p_p_id=NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=1&p_p_col_count=2&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_fname=&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_lname=&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_search=1&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_prvnc=23&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_cty=&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_gnd=2&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_cnumber=&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_public_fld=1217&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_delta=12&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_keywords=&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_advancedSearch=false&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_andOperator=true&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_resetCur=false&_NetFormRecordsViewer_WAR_NetForm_INSTANCE_Bj31ZqhnvJ3m_cur='

SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'Mozilla/5.0'})

def CONNECT(PAGE):
        return BeautifulSoup(SESSION.get(PAGE, headers={'User-Agent': 'Mozilla/5.0'}).text, 'html.parser').find_all('a', attrs={'class' : 'p-4 border border-gray-300 rounded'})

def SCRAPE_DATA(URL):
    T_NAMES, T_NUMBERS = list(), list()
    for PAGE in itertools.count(1):
        if (ELEMENTS := BeautifulSoup(SESSION.get(URL + str(PAGE)).text, 'html.parser').find_all('a', attrs={'class' : 'p-4 border border-gray-300 rounded'})):
            for ITEM in ELEMENTS:
                T_NAMES.extend(re.findall(RE_NAME, str(ITEM))) if len(re.findall(RE_NAME, str(ITEM))) == 1 else T_NAMES.append("?")
                T_NUMBERS.extend(re.findall(RE_NUMBER, str(ITEM))) if len(re.findall(RE_NUMBER, str(ITEM))) == 1 else T_NUMBERS.append("۰۰۰۰۰۰۰۰۰۰۰")
        else:
            break
    NAMES_LIST.append(T_NAMES)
    NUMBERS_LIST.append(T_NUMBERS)

def TXT(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        for contact in data:
            file.write(f"{contact[0]}: {contact[1]}\n")

def VCF(GENDER, LIST_NAME, LIST_NUMBER):
    NAMES = ["کارشناس " + ITEM for ITEM in LIST_NAME]

    CONTACTS = [{'name': NAME, 'phone': NUMBER} for NAME, NUMBER in zip(NAMES, LIST_NUMBER)]

    VCARD_LIST = []

    for CONTACT in CONTACTS:
        VCARD = vobject.vCard()
        VCARD.add('fn').value = CONTACT['name']
        TEL = VCARD.add('tel')
        TEL.value = CONTACT['phone']
        TEL.type_param = 'CELL'
        VCARD_LIST.append(VCARD)

    file_name = os.path.join(PATH, f"{GENDER}.vcf")
    with open(file_name, 'w', encoding='utf-8') as VCF_FILE:
        for VCARD in VCARD_LIST:
            VCF_FILE.write(VCARD.serialize())

SCRAPE_DATA(MEN)
SCRAPE_DATA(WOMEN)

NAMES_ALL = NAMES_LIST[0] + NAMES_LIST[1]
NUMBERS_ALL = NUMBERS_LIST[0] + NUMBERS_LIST[1]

TXT(os.path.join(PATH, 'all.txt'), zip(NAMES_ALL, NUMBERS_ALL))
TXT(os.path.join(PATH, 'men.txt'), zip(NAMES_LIST[0], NUMBERS_LIST[0]))
TXT(os.path.join(PATH, 'women.txt'), zip(NAMES_LIST[1], NUMBERS_LIST[1]))

VCF("all", NAMES_ALL, NUMBERS_ALL)
VCF("men", NAMES_LIST[0], NUMBERS_LIST[0])
VCF("women", NAMES_LIST[1], NUMBERS_LIST[1])