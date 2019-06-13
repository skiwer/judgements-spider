#-*- coding=utf-8 -*-
from task_manager import TaskManager

def main():
    m = TaskManager()
    # m.initialize({"犯罪": 100})
    print(m.get_all_undo_tasks())

if __name__ == '__main__':
    main()