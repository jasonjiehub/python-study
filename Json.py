import json
import simplejson
# data = {
#     'name': 'ACME',
#     'shares': 100,
#     'price': 542.23,
#     'second': {
#         'third': 30
#     }
# }
data = '{"nodes": [{"id": "119208", "name":"陈奕迅","img":"http://img03.sogoucdn.com/app/a/10010016/d09e11c92043fc6f0db373fe762594e1","intro":"陈奕迅(Eason Chan)，1974年7月27日出生于香港，中国香港流行男歌手、演员，香港演艺人协会副会长之一，香港流行。","w":17.0,"baike":"http://baike.sogou.com/v95599.htm","level":0},{"id":"1294857","name":"谢霆锋","img":"http://img02.sogoucdn.com/app/a/10010016/0ae867b47af29f331934fd4ed4dd70e8","w":4.0,"baike":"","level":1},{"id":"81844","name":"卢巧音","img":"http://img01.sogoucdn.com/app/a/10010016/b5eb00bfb9915d829d3244395e6a8e8a","w":4.0,"baike":"http://baike.sogou.com/v113549.htm","level":2}]}'
# json_str = json.dumps(data)
# print(type(json_str))
# data = json.loads(json_str)
# print(type(data))
# print(data['name'])
# print(data['second']['third'])
res = simplejson.loads(data)
print(res['nodes'])

