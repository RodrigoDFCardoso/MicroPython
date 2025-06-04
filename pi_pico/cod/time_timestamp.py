from machine import RTC
import time
rtc = RTC()
timestamp=rtc.datetime()
timestring="%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] +
                                                timestamp[4:7])


timestamp_2=time.localtime()
timestamp_3=time.time()

teste = '%04d%02d%02d'%(timestamp[0:3])
print(teste)

print(timestamp_2)
print(timestamp_3)