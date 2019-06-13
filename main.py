#-*- coding=utf-8 -*-
from task_manager import TaskManager
from multiprocessing import Process
import gevent
from gevent import monkey; monkey.patch_all()
from fetch import Fetch

class Main(Object):
    def __init__(self):
        self.tasks = TaskManager.get_all_undo_tasks()
    def task_allocation(self, max_task):
        start = 0
        num = len(self.tasks)

        if num == 0:
            return

        while start < num:
            current_tasks = self.tasks[start, max_task]
            p = Process(target=task_start, args=(current_tasks,))
            p.start()
            start += max_task

    def task_start(self, tasks):
        run_co_tasks = []
        for task in tasks:
            run_co_tasks.append(gevent.spawn(Fetch.get_one_page_by_keyword, task[0], task[1]))
        gevent.joinall(run_co_tasks)

if __name__ == '__main__':
    main = Main()
    main.task_allocation(1000)
