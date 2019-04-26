from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import time


class SCHEDULE(object):
    '''
    计划任务，用于循环执行任务
    : param interval_time: 循环间隔 int
    : param mode: 计划任务模式，默认为'interval' 循环模式
    : func run : 开启循环
    '''

    def __init__(self):
        self._Sched = BackgroundScheduler()
        self.interval_time = 10
        self.mode = 'interval'

    def _sleep(self):
        time.sleep(0.5)

    def run(self):
        '''
        开启循环
        '''
        self._Sched.add_job(self._todo, 'interval', seconds=self.interval_time,
                            max_instances=5)
        self._Sched.start()

    def block(self):
        '''
        开启阻塞，用于多偶像监控
        '''
        blk = BlockingScheduler()
        blk.add_job(self._sleep, 'interval', seconds=1)
        blk.start()
