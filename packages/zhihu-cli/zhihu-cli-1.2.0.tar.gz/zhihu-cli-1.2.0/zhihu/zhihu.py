# -*- coding: UTF-8 -*-
import json
import os
import re
import shutil
from datetime import datetime
from random import random
from time import sleep

import requests
from bs4 import BeautifulSoup


class Zhihu(object):

    def __request__(self, url, payloads=None):
        ua = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        try:
            sleep(random())
            response = requests.get(url, payloads, headers=ua)
            if response.status_code == 200:
                return json.loads(response.text, encoding='utf8')
            elif response.status_code == 403:
                raise ConnectionError(response.status_code, response.text)
            else:
                raise ConnectionError(response.status_code, response.url)

        except Exception as e:
            raise e

    def __download__(self, url):
        ua = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        try:
            sleep(random())
            response = requests.get(url, headers=ua)
            if response.status_code == 200:
                return response.content
            else:
                raise ConnectionError(response.status_code, response.url)
        except Exception as e:
            raise e

    def __ut2date__(self, ut):
        return datetime.fromtimestamp(ut).strftime('%Y-%m-%d %H:%M:%S') if ut else '0000-00-00 00:00:00'

    def __html2text__(self, html):
        pattern = re.compile(r"<.*?>")
        return pattern.sub('', html)

    def __addattribute__(self):
        for k, v in self.__info__.items():
            self.__dict__[k] = v
        self.__dict__['info'] = self.__info__


class User(Zhihu):

    def __init__(self, uid):
        self.__uid__ = uid
        self.__anonymous__ = ['', '0', 0, None]

        self.__gendermap__ = {
            1: "男",
            0: "女",
            -1: "未知",
        }

        self.__info__ = {
            "customized_id": '',                        # 自定义ID
            "internal_id": '',                          # 内部ID
            "nickname": '',                             # 显示名字
            "gender": self.__gendermap__[-1],           # 性别 0:女 1:男
            "avatar": '',                               # 用户头像
            "headline": '',                             # 个人简介
            "is_vip": '',                               # 盐选会员
            "follower_count": '',                       # 关注者数量
            "following_count": '',                      # 关注的人数量
            "answer_count": '',                         # 回答数量
            "question_count": '',                       # 提问数量
            "articles_count": '',                       # 文章数量
            "voteup_count": '',                         # 获得赞同数量
        }

        self.__getinfo__()

        if self.__uid__ not in self.__anonymous__:
            self.__info__['followers'] = self.__follower__()
            self.__info__['followings'] = self.__following__()

        self.__addattribute__()

    def __getinfo__(self):
        url = f"https://www.zhihu.com/api/v4/members/{self.__uid__}"

        payloads = {
            "include": "follower_count,following_count,answer_count,question_count,articles_count,voteup_count"
        }

        if self.__uid__ in self.__anonymous__:
            self.__info__['nickname'] = '匿名用户'
        else:
            info = self.__request__(url, payloads)

            self.__info__['customized_id'] = info['url_token']
            self.__info__['internal_id'] = info['id']
            self.__info__['nickname'] = info['name']
            self.__info__['avatar'] = info['avatar_url']
            self.__info__['gender'] = self.__gendermap__[info['gender']]
            self.__info__['headline'] = info['headline']
            self.__info__['is_vip'] = info['vip_info']['is_vip']
            self.__info__['follower_count'] = info['follower_count']
            self.__info__['following_count'] = info['following_count']
            self.__info__['answer_count'] = info['answer_count']
            self.__info__['question_count'] = info['question_count']
            self.__info__['articles_count'] = info['articles_count']
            self.__info__['voteup_count'] = info['voteup_count']

    def __follower__(self):
        url = f"https://www.zhihu.com/api/v4/members/{self.info['customized_id']}/followers"
        offset = 0
        payloads = {
            "limit": 1,
            "offset": offset,
        }
        info = self.__request__(url, payloads)
        is_end = info['paging']['is_end']

        yield User(info['data'][0]['url_token'])

        while not is_end:
            offset += 1
            payloads = {
                "limit": 1,
                "offset": offset,
            }
            info = self.__request__(url, payloads)
            is_end = info['paging']['is_end']

            yield User(info['data'][0]['url_token'])

    def __following__(self):
        url = f"https://www.zhihu.com/api/v4/members/{self.info['customized_id']}/followees"
        offset = 0
        payloads = {
            "limit": 1,
            "offset": offset,
        }
        info = self.__request__(url, payloads)
        is_end = info['paging']['is_end']

        yield User(info['data'][0]['url_token'])

        while not is_end:
            offset += 1
            payloads = {
                "limit": 1,
                "offset": offset,
            }
            info = self.__request__(url, payloads)
            is_end = info['paging']['is_end']

            yield User(info['data'][0]['url_token'])

    def __bool__(self):
        return False if self.__uid__ in self.__anonymous__ else True


class Answer(Zhihu):

    def __init__(self, aid, **kwargs):
        self.__info__ = {
            "aid": aid,
            "type": kwargs.get('type', ''),
            "author": User(kwargs.get('author', None)),
            "excerpt": kwargs.get('excerpt', ''),
            "content": kwargs.get('content', ''),
            "text": self.__html2text__(kwargs.get('content', '')),
            "comment_count": kwargs.get('comment_count', ''),
            "voteup_count": kwargs.get('voteup_count', ''),
            "created": self.__ut2date__(kwargs.get('created', None)),
            "updated": self.__ut2date__(kwargs.get('updated', None)),
            "question": kwargs.get('question', '')
        }

        if not kwargs:
            self.__getinfo__()

        self.__addattribute__()

    def __getinfo__(self):
        url = f"https://www.zhihu.com/api/v4/answers/{self.__info__['aid']}"
        payloads = {
            "include": "content,excerpt,comment_count,voteup_count"
        }
        info = self.__request__(url, payloads)

        self.__info__['type'] = info['answer_type']
        self.__info__['author'] = User(info['author']['id'])
        self.__info__['excerpt'] = info['excerpt']
        self.__info__['content'] = info['content']
        self.__info__['text'] = self.__html2text__(info['content'])
        self.__info__['comment_count'] = info['comment_count']
        self.__info__['voteup_count'] = info['voteup_count']
        self.__info__['created'] = self.__ut2date__(info['created_time'])
        self.__info__['updated'] = self.__ut2date__(info['updated_time'])
        self.__info__['question'] = Question(info['question']['id'])

    def save_media(self, path=None):
        if not path:
            path = os.path.join(
                str(self.question.qid)+'_'+self.question.title,
                str(self.aid)
            )
        shutil.rmtree(path, ignore_errors=True)
        os.makedirs(path)

        soup = BeautifulSoup(self.__info__['content'], 'lxml')
        noscript = soup.find_all('noscript')

        for imgtag in noscript:
            if imgtag.img.has_attr('data-original'):
                url = imgtag.img['data-original']
            else:
                url = imgtag.img['src']
            data = self.__download__(url)
            with open(os.path.join(path, os.path.basename(url)), 'wb') as f:
                f.write(data)


class Question(Zhihu):

    def __init__(self, qid):
        self.__info__ = {
            'qid': qid,
            'title': None,
            'detail': None,
            'type': None,
            'created': None,
            'updated': None,
            'author': None,
        }

        self.__getinfo__()

        self.__addattribute__()

    def __getinfo__(self):
        url = f"https://www.zhihu.com/api/v4/questions/{self.__info__['qid']}"
        payloads = {
            "include": "question.detail,author"
        }
        info = self.__request__(url, payloads)

        self.__info__['title'] = info['title']
        self.__info__['detail'] = self.__html2text__(info['detail'])
        self.__info__['type'] = info['question_type']
        self.__info__['created'] = self.__ut2date__(info['created'])
        self.__info__['updated'] = self.__ut2date__(info['updated_time'])
        self.__info__['author'] = User(info['author']['id'])

    def answers(self, sort_by='default'):
        url = f"https://www.zhihu.com/api/v4/questions/{self.__info__['qid']}/answers"
        payloads = {
            "include": "content,excerpt,comment_count,voteup_count",
            "offset": 0,
            "limit": 1,
            "sort_by": sort_by
        }
        info = self.__request__(url, payloads)

        is_end = info['paging']['is_end']
        nexturl = info['paging']['next']

        yield Answer(
            aid=info['data'][0]['id'],
            type=info['data'][0]['answer_type'],
            author=info['data'][0]['author']['id'],
            excerpt=info['data'][0]['excerpt'],
            content=info['data'][0]['content'],
            text=info['data'][0]['content'],
            comment_count=info['data'][0]['comment_count'],
            voteup_count=info['data'][0]['voteup_count'],
            created=info['data'][0]['created_time'],
            updated=info['data'][0]['updated_time'],
            question=Question(info['data'][0]['question']['id'])
        )
        while not is_end:
            info = self.__request__(nexturl)
            is_end = info['paging']['is_end']
            nexturl = info['paging']['next']
            yield Answer(
                aid=info['data'][0]['id'],
                type=info['data'][0]['answer_type'],
                author=info['data'][0]['author']['id'],
                excerpt=info['data'][0]['excerpt'],
                content=info['data'][0]['content'],
                text=info['data'][0]['content'],
                comment_count=info['data'][0]['comment_count'],
                voteup_count=info['data'][0]['voteup_count'],
                created=info['data'][0]['created_time'],
                updated=info['data'][0]['updated_time'],
                question=Question(info['data'][0]['question']['id'])
            )
