#최단경로 알고리즘 #reference : http://navercast.naver.com/contents.nhn?rid=2871&contents_id=85293
#목적지와 도착지를 설정해준다 departure = 'home' destination = 'school' 

graph = { 'home': {'hairShop':5, 'superMarket':10, 'EnglishAcademy':9},
'hairShop' : {'home':5 ,'superMarket':3, 'bank':11}, 
'superMarket' : {'hairShop':3, 'home':10, 'EnglishAcademy':7, 'restourant':3}, 
'EnglishAcademy': {'home':9, 'superMarket':7, 'school':12}, 
'restourant' : {'superMarket':3, 'bank':4}, 
'bank' : {'hairShop':11, 'restourant':4, 'EnglishAcademy':7, 'school':2}, 
'school' : {'bank':2, 'EnglishAcademy':12} } 




