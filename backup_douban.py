#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys
import json
import random
import argparse
import datetime
import webbrowser
import math
import gevent
from gevent.queue import Queue
from gevent import monkey; monkey.patch_all()
import requests
from requests.exceptions import MissingSchema
from pyquery import PyQuery

MY_URL = "https://www.douban.com/people/xxxxxxxxx/" # 这里填入豆瓣主页url

s = requests.Session()
headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
        "Referer": MY_URL,
        }


def get_movie_list(url):
    """get the movie's info from the url

    :returns: [{'title':'', 'url':'', 'tags':['','',...]},{},...]

    """
    item_list = []
    page_queue = get_page_queue(url)
    def get_one_page_info():
        """get one page's info and add to item_list"""
        while not page_queue.empty():
            p = page_queue.get()
            print(p)
            html = s.get(p, headers=headers).text
            doc = PyQuery(html)
            item_nodes = doc('div.item')
            rating = "未知"
            for item in item_nodes:
                item = doc(item)
                info = {}
                if(item('.rating2-t')):
                    rating = "2星" 
                if(item('.rating3-t')):
                    rating = "3星" 
                if(item('.rating4-t')):
                    rating = "4星" 
                if(item('.rating5-t')):
                    rating = "5星" 
                if(item('.rating1-t')):
                    rating = "1星" 
                comment = item('span.comment').text()
                date = item('span.date').text()
                title = item('li.title').text()
                item_url = item('li.title a').attr('href')
                tag_node = item('span.tags')
                tags = [] if tag_node == [] else tag_node.text().split(' ')[1:]
                info['title'] = re.sub('\s', '', title)
                info['url'] = item_url
                info['tags'] = tags
                info['date'] = date
                info['comment'] = comment
                info['rating'] = rating
                item_list.append(info)
    # start 4 greenlets
    gevent_list = [gevent.spawn(get_one_page_info) for i in range(4)]
    gevent.joinall(gevent_list)
    return item_list

def get_book_list(url):
    """get the movie's info from the url

    :returns: [{'title':'', 'url':'', 'tags':['','',...]},{},...]

    """
    item_list = []
    page_queue = get_page_queue(url)
    def get_one_page_info_2():
        """get one page's info and add to item_list"""
        while not page_queue.empty():
            p = page_queue.get()
            # print(p)
            html = s.get(p, headers=headers).text
            doc = PyQuery(html)
            item_nodes = doc('li.subject-item')
            rating = "未知"
            for item in item_nodes:
                item = doc(item)
                info = {}
                if(item('.rating2-t')):
                    rating = "2星" 
                comment = item('span.comment')
                if(item('.rating3-t')):
                    rating = "3星" 
                comment = item('span.comment')
                if(item('.rating4-t')):
                    rating = "4星" 
                comment = item('span.comment')
                if(item('.rating5-t')):
                    rating = "5星" 
                comment = item('span.comment')
                if(item('.rating1-t')):
                    rating = "1星" 
                comment = item('p.comment').text()
                date = item('span.date').text()
                pub = item('div.pub').text()
                title = item('h2 a').attr('title')
                item_url = item('div.info a').attr('href')
                tag_node = item('span.tags')
                tags = [] if tag_node == [] else tag_node.text().split(' ')[1:]
                info['title'] = re.sub('\s', '', title)
                info['pub'] = pub 
                info['url'] = item_url
                info['tags'] = tags
                info['date'] = date
                info['comment'] = comment
                info['rating'] = rating
                item_list.append(info)
    # start 4 greenlets
    gevent_list = [gevent.spawn(get_one_page_info_2) for i in range(4)]
    gevent.joinall(gevent_list)
    return item_list

def get_page_queue(url):
    """get all wish page to a queue"""
    page_queue = Queue()
    try:
        html = s.get(url, headers=headers).text
    except MissingSchema as e:
        print(e)
        print('请填入正确的url')
    doc = PyQuery(html)
    # amount of items
    item_count = int(doc('.subject-num').text().split('/')[1])
    pages_count = item_count // 15
    for i in range(pages_count + 1):
        page_url = url + "?start=%s&sort=time&rating=all&filter=all&mode=grid"%(i * 15)
        page_queue.put(page_url)
    return page_queue


def save_list(item_list, file_path):
    """use json save item_list"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(item_list, f,ensure_ascii=False,sort_keys=True, indent=4)


def get_local_cache(file_path):
    """read the item_list from cache"""
    if not(os.path.exists(file_path)) :
        return []
    with open(file_path, 'rb') as f:
        result = json.load(f)
    return result
    

def print_movie_info(item_list):
    '''print the information of all movies'''
    if(len(item_list) == 0) :
        print("no such file OR it's empty\n")
        return 0
    for i in item_list:
        print("-----------------------------------------------------------------")
        print()
        print("\033[33m%s\033[0m"%i["title"])
        print("\033[31mTags    :\033[0m   " + " ".join(i['tags']))
        print("\033[32mdouban  :\033[0m  \"%s\""%i['url'])
        print("\033[32mdate  :\033[0m  \"%s\""%i['date'])
        print("\033[32mcomment  :\033[0m  \"%s\""%i['comment'])
        print("\033[32mrating  :\033[0m  \"%s\""%i['rating'])
    print(len(item_list))

def print_book_info(item_list):
    '''print the information of all movies'''
    if(len(item_list) == 0) :
        print("no such file OR it's empty\n")
        return 0
    for i in item_list:
        print("-----------------------------------------------------------------")
        print()
        print("\033[33m%s\033[0m"%i["title"])
        print("\033[33mPub  :%s\033[0m"%i["pub"])
        print("\033[31mTags    :\033[0m   " + " ".join(i['tags']))
        print("\033[32mdouban  :\033[0m  \"%s\""%i['url'])
        print("\033[32mdate  :\033[0m  \"%s\""%i['date'])
        print("\033[32mcomment  :\033[0m  \"%s\""%i['comment'])
        print("\033[32mrating  :\033[0m  \"%s\""%i['rating'])
    print("total item nums is :")
    print(len(item_list))

def filiter_by_tags(item_list, tags):
    result = []
    for movie in item_list:
        for t in tags:
            if t not in movie['tags']:
                break
            result.append(movie)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--info', help="Display the wish list's infomatiom.", action="store_true")
    parser.add_argument('-u', '--update', help="Update local cache.", action="store_true")
    parser.add_argument('-c', '--clean', help="Clean local cache.", action="store_true")
    args = parser.parse_args()

    if args.clean:
        print("Cleaning ...")
        os.system("rm ./*json")
        sys.exit()

    if args.update :
        print("Which list to update:\n")
        print("1.movie collect list\n") 
        print("2.movie wish list\n")
        print("3.book collect list\n")
        print("4.book wish list\n")
        print("----------------------")
        # choose = [int(n) for n in input("choose one:").split()]
        item = input("please input")
        if item == "1" :
            MY_URL = MY_URL.replace('www', 'movie') + 'collect'
            CACHE_FILE_PATH = './movie_collect.json' 
            print("Updating ...")
            item_list = get_movie_list(MY_URL)
            save_list(item_list, CACHE_FILE_PATH)
            print("Local updated!(in '%s') run again with other option!"%CACHE_FILE_PATH)
        elif item == "2":
            print("this is two")
            MY_URL = MY_URL.replace('www', 'movie') + 'wish'
            CACHE_FILE_PATH = './movie_wish.json'
            print("Updating ...")
            item_list = get_movie_list(MY_URL)
            save_list(item_list, CACHE_FILE_PATH)
            print("Local updated!(in '%s') run again with other option!"%CACHE_FILE_PATH)
        elif item == "3":
            MY_URL = MY_URL.replace('www', 'book') + 'collect'
            CACHE_FILE_PATH = './book_collect.json' 
            print("Updating ...")
            item_list = get_book_list(MY_URL)
            # print_book_info(item_list)
            save_list(item_list, CACHE_FILE_PATH)
            print("Local updated!(in '%s') run again with other option!"%CACHE_FILE_PATH)
        elif item == "4":
            MY_URL = MY_URL.replace('www', 'book') + 'wish'
            CACHE_FILE_PATH = './book_wish.json'
            print("Updating ...")
            item_list = get_book_list(MY_URL)
            save_list(item_list, CACHE_FILE_PATH)
            print("Local updated!(in '%s') run again with other option!"%CACHE_FILE_PATH)
        else :
            print("illegal input\n")
            sys.exit()
        
    if args.info:
        print("Which list to show:\n")
        print("1.movie collect list\n") 
        print("2.movie wish list\n")
        print("3.book collect list\n")
        print("4.book wish list\n")
        print("----------------------")
        item = input("please input:")
        if item == "1" :
            CACHE_FILE_PATH = './movie_collect.json' 
            item_list = get_local_cache(CACHE_FILE_PATH)
            print_movie_info(item_list)
        elif item == "2":
            CACHE_FILE_PATH = './movie_wish.json' 
            item_list = get_local_cache(CACHE_FILE_PATH)
            print_movie_info(item_list)
        elif item == "3":
            CACHE_FILE_PATH = './book_collect.json' 
            item_list = get_local_cache(CACHE_FILE_PATH)
            print_book_info(item_list)
        elif item == "4":
            CACHE_FILE_PATH = './book_wish.json' 
            item_list = get_local_cache(CACHE_FILE_PATH)
            print_book_info(item_list)
        else :
            print("illegal input!\n")
            sys.exit() 