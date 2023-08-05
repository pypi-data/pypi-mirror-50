#coding=utf-8
from uiautomator import device as d
import time


d.set_debug(True)
d(text='我来了').wait.exists(timeout=100)
d.watcher("AUTO_FC_WHEN_ANR").when(text="ANR").when(text="Wait").click(text="Force Close")
# print "ffff"
# print d.watchers

# tt = {'11':'我来了'}
# print str(tt)
# print repr(tt).decode('string_escape')

