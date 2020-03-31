# backup_douban
备份豆瓣的电影、图书清单

## 源项目
https://github.com/Nanguage/douban_movie_recommander

## 增删
- ~~随机推荐~~
- ~~查找bilibili~~
- **备份为json格式**
- **新增读书页面、已看页面**

## 配置/运行

#### 第三方库依赖
BeautifulSoup
```
pip3 install -r "requirments.txt"
```

#### 设置:
	MY_URL = "https://www.douban.com/people/xxxxxxxx/" # 在xxxxxxxx这里填入豆瓣主页url

#### 用法: 
	usage: m_ovie_recommend [-c] [-i] [-u] 
	
	optional arguments:
	  -i, --info            Display the wish list's infomatiom.
	  -u, --update          Update local cache.
	  -c, --clean           Clean local cache.

#### 演示:  
![Kapture 2019-11-17 at 14.51.00.gif](https://i.loli.net/2019/11/17/QVPuM6t9iNzcd4G.gif)
