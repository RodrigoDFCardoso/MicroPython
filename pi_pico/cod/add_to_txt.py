import time

timestamp = time.localtime()
print(timestamp)
file_name = 'data_%04d%02d%02d.txt'%(timestamp[0:3])

a=95
file=open(file_name,"w")	# file is created and opened in write mode
while a>0:			# program logic
    tempo=time.time()
    t = str(f'{tempo} {a}')
    file.write(str(t)+"\n")	# data is written as a string in the CSV file
    file.flush()		# internal buffer is flushed
    a-=5