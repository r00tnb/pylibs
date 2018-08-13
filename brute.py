# coding=utf-8

import threading

def brute_force_file(handle,files,threads=50):
    if not isinstance(files,tuple):
        raise TypeError,"files must be type of tuple,but it got {}".format(type(files))
    tmp = Brute(threads)
    tmp.set_dicfiles(*files)
    tmp.set_handle(handle)
    tmp.start()
    return tmp.get_match()


def brute_force_dic(handle,dic,threads=50):
    if not isinstance(dic,list):
        raise TypeError,"files must be type of list,but it got {}".format(type(files))
    tmp = Brute(threads)
    tmp.set_dic(dic)
    tmp.set_handle(handle)
    tmp.start()
    return tmp.get_match()

class Brute:
    def __init__(self,threads=50):
        self.__threads = threads
        self.__dicFiles = ()
        self.__dic = []
        self.__handle = None
        self.__currentIndex = 0
        self.__stop = True
        self.__lock = threading.Lock()
        self.__dicLen = 0
        self.__match = None

    def set_handle(self,handle):
        self.__handle = handle

    def set_threads(self,threads):
        self.__threads = threads

    def get_lock(self):
        return self.__lock

    def get_threads(self):
        return self.__threads

    def get_dic_len(self):
        return self.__dicLen

    def get_match(self):
        return self.__match

    def set_dicfiles(self,*args):
        self.__dicFiles = args
        self.__dic = []
        for i in args:
            with open(i,'r') as f:
                self.__dic.extend([i.strip() for i in f.readlines()])
        self.__dicLen = len(self.__dic)

    def set_dic(self,dic):
        if(not isinstance(dic,list)):
            raise TypeError,"The dic must be type of 'list',but now it is {}".format(type(dic))
        self.__dic = dic
        self.__dicLen = len(dic)
        self.__dicFiles = ()

    def get_dic(self):
        return self.__dic

    # 判断字典是否遍历完
    def is_over(self):
        if self.__currentIndex == self.__dicLen:
            return True
        return False

    @staticmethod
    def __work(inst):
        i = 0
        while True:
            inst.__lock.acquire()
            i = inst.__currentIndex
            inst.__currentIndex = i+1
            inst.__lock.release()
            if i >= inst.__dicLen or inst.__match != None:
                return
            if inst.__handle(inst.__dic[i],inst.__lock):
                inst.__lock.acquire()
                inst.__match = inst.__dic[i]
                inst.__lock.release()
                return

    def start(self,block=True):
        self.__stop = False
        self.__match = None

        th = []
        for t in xrange(self.__threads):
            t = threading.Thread(target=Brute.__work,args=(self,))
            th.append(t)

        for t in th:
            t.setDaemon(True)
            t.start()
        if block:
            for t in th:
                t.join()