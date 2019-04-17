# -*- coding: utf-8 -*-
'''
@author: DipperStar
@mail: ssr@yinheng.xyz
'''
import requests
import json
import time
from pocketapi import API
from mongo import MongoDB
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
import pymongo

class POCKET48(API):
    '''

    '''
    def __init__(self, mobile, password, membername):
        super().__init__(mobile, password, membername)
        self.dbchat = MongoDB('Poket48', str(self.roomId))
        self.Sched = BlockingScheduler()
        
    def update_chat(self):
        for data in self.chatroom():
            if self.dbchat.update(data,upsert = True) == 'success':
                pass

    def message(self):
        pass
    
    def run(self):
        pass


