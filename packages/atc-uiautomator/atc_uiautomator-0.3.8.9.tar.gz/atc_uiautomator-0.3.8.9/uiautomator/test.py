#coding=utf-8
from uiautomator import device as d
import time
from threading import Timer


d.set_debug(True)
# d(text='我来了').wait.exists(timeout=100)
d.watcher("auto_yunxu").when(packageName='com.android.systemui').when(text="允许").click(text="允许")
# print "ffff"
print d.watchers
# d.watchers.remove()
print d.watchers
# d.watchers.triggered
def tt():
    d(text='ttt').wait.exists(timeout=3000) 
Timer(3, tt).start()
print d.getPhoneInfo()
for i in d.getSmsInfo(2):
    print i
