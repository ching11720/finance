import csv
import matplotlib.pyplot as plt

money=[]
m1=[]
comment=[]
demand=[]
supply=[]

#匯入先前用excel篩選好的資料
with open('data.csv', 'r') as fd:
	next(fd)
	reader = csv.reader(fd)
	for row in reader:
		money.append(int(row[0]))
		comment.append(int(row[1]))
fd.close()

#demand
m1.append(money[0])
demand.append(0)
for i in range(len(money)):
	if(money[i]==m1[-1]):
		demand[-1]+=comment[i]
	else:
		m1.append(money[i])
		demand.append(comment[i])

#supply，假設每個賣家都願意供給100份代購需求
iii=0
supply.append(0)
for ii in money:
	if(ii==m1[iii]):
		supply[iii]+=100
	else:
		iii+=1
		supply.append(100)

#畫圖表
plt.plot(m1,demand,color=(165/255,144/255,175/255))
plt.plot(m1,supply,color=(255/255,203/255,91/255))

plt.show()
