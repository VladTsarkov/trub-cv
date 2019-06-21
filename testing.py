from multiprocessing import Process
#import multiprocessing
"""
class Worker(multiprocessing.Process):

    def run(self):
        print('In %s' % self.name)
        return

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = Worker()
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()
"""
class Worker2(Process):
    def __init__(self):
        super(Worker2,self).__init__()
    def run(self):
        print('IN %s' % self.name)
        
class Worker(Process):
    def __init__(self):
        super(Worker,self).__init__()
    def run(self):
        print('In %s' % self.name)
        return

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        if i!=2:
            p = Worker()
        else:
            p = Worker2()
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()
