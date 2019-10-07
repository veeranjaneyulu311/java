from datetime import datetime, timedelta
sec = timedelta(seconds=int((input('Enter the number of seconds: '))))
x = datetime(1,1,1)
print(type(x))
print(type(sec))
d = x + sec

print(type(d))
print(type(d.day-1))
print(d.hour)
print(d.minute)
print(d.second)