import time
def println(string = ''):
    print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())) + str(string))