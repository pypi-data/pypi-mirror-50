My toolbox for dynamic programming

#tf-id
from anarcute import *
import requests, json

sentence="Eat more of those french fries and drink cola"
text=requests.get("https://gist.githubusercontent.com/phillipj/4944029/raw/75ba2243dd5ec2875f629bf5d79f6c1e4b5a8b46/alice_in_wonderland.txt").text
print(tf_idf(sentence,text))
>> {'eat': 168.7962962962963, 'more': 62.006802721088434, 'of': 5.9111543450064845, 'those': 303.8333333333333, 'french': 759.5833333333333, 'and': 3.4843272171253816, 'drink': 434.047619047619}

#If text is too big it's frequencies can be pre-cached.
filename="alice.json"
vector=vectorize(text)
open(filename,"w+").write(json.dumps(vector))
vector=json.load(open(filename,"r+"))

print(tf_idf(sentence,vector))