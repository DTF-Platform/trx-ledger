from urllib.request import Request, urlopen
import json
from tronapi import Tron
from binascii import unhexlify
import codecs
import time
import fileinput

def conv(string):
    ret = "0x"+string[0:2]
    for i in range(1,21):
        ret += ",0x"+string[i*2:(i+1)*2]
    return ret


def urlopen_with_retry(toread, start):
     for i in range(5):
        try:
            time.sleep(0.3) 
            url = "https://apilist.tronscan.org/api/token_trc20?sort=issue_time&limit={}&start={}".format(toread, start)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            return urlopen(req).read()
        except Exception as e:
            print(e)
            continue

ItemsFields = 'trc20_tokens'
toread = 20
start = 0
f= open("signedList_TRC20.txt","w+")
tron = Tron()
totalToken = 0
while (toread>0):
    url = urlopen_with_retry(toread,start)
    data = json.loads(url.decode())

    for T in data[ItemsFields]:
        address = tron.address.to_hex(T['contract_address'])
        f.write('{}{}{}{}, \"${} \", {}{},'.format("{","{",conv(address),"}",T['symbol'],T['decimals'],"}" ))
        f.write('\n')
    
    totalToken += len(data[ItemsFields])
    if len(data[ItemsFields])<toread:
        toread = 0
    start = start + toread

f.write('\n')
f.write('''{{0x41,0xDE,0xAA,0x5F,0x32,0x96,0x3C,0x91,0x9C,0x2A,0x5A,0x8F,0x84,0x82,0xCC,0x8C,0x92,0xF5,0x04,0xB8,0xB2}, "$BET ", 6},
{{0x41,0xF8,0xAD,0xE6,0x3F,0x62,0x94,0xB1,0xE3,0x25,0x6C,0x46,0x9C,0x05,0xA7,0xE0,0x8A,0xE6,0xF1,0x53,0x2C}, "$GOC ", 6},
{{0x41,0x8d,0x22,0x24,0x68,0xca,0x88,0xa8,0xbd,0xc5,0x9d,0x03,0x36,0xe6,0x6c,0xb4,0x4c,0xe7,0x93,0xb9,0x10}, "$REWARD ", 6},
{{0x41,0x98,0xf4,0xdb,0x2f,0x43,0x3e,0x98,0xf6,0xd8,0x97,0xd6,0x94,0x57,0x47,0xee,0xa2,0x7f,0xb5,0x97,0x9d}, "$FREE ", 6},
{{0x41,0x14,0x18,0x3f,0x3b,0xbc,0xa4,0xae,0x9f,0xc1,0xde,0x55,0xb9,0xbb,0xe2,0xd0,0x71,0x94,0x2d,0xc1,0xa6}, "$CCT ", 6},''')
f.write('\n')
f.close()

totalToken += 5
print("Total Tokens: ",totalToken)
# TODO: update .c .h files



