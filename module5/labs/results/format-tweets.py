import sys
import json

f = open(sys.argv[1],"r")
data = json.load(f)
f.close()

for tweet in data["tweets"]:
    language = tweet["metadata"]["iso_language_code"].encode('utf-8')
    text = tweet["text"].replace("\n"," ")
    print("#iso-"+language.decode('utf-8')+" "+str(text.encode('utf-8')))