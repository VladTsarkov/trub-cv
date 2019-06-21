from multiprocessing import Process, Queue
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
    def __init__(self,q):
        super(Worker2,self).__init__()
        self.q = q
    def run(self):
        print('IN %s' % self.q.get())

class Worker(Process):
    def __init__(self,name, q1 ,q2):
        super(Worker,self).__init__()
        self.q1 = q1
        self.q2 = q2
        self.name=name
    def run(self):
        name = self.name + "123"
        q.put(name)
        print('In %s' % name)
        return

if __name__ == '__main__':
    jobs = []
    q = Queue()
    name = "what"
    for i in range(5):
        p = Worker(q,name)
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()
    #print(q.get())
