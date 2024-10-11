from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as Soup
import time
import random

#conti : https://tlyu0419.github.io/2019/05/01/Crawl-Facebook/

#一些基本資料#
fb="https://www.facebook.com/"
url="https://www.facebook.com/groups/919492278761869" #被爬蟲的社團，目前是一個不公開的社團
email=input("輸入您的email:\n")
password=input("輸入您的密碼:\n")

#匯入賣家資料
a=[]
with open('data.txt', 'r') as fd:
	for line in fd.readlines():
		if line[0]=='a':
			a.append(line)
fd.close()
for m in range(len(a)):
	a[m]=a[m].replace("author : ","")
	a[m]=a[m].replace("\n","")

print(a)
#隨機選出取樣賣家
for mm in range(len(a)):
	target=random.randint(0,len(a)-1)
	a_tmp=a[mm]
	a[mm]=a[target]
	a[target]=a_tmp
print(a)

#打開chrome#
chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.default_content_setting_values.notifications": 2
}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

driver.maximize_window() #最大化視窗

#進入並登入fb#
driver.get(fb)
driver.find_element(By.ID,"email").send_keys(email)
driver.find_element(By.ID,"pass").send_keys(password)
driver.find_element(By.NAME,"login").click()

time.sleep(18)

a_frames=[]
p_frames=[]
c_frames=[]
authors=[]
posts=[]
comments=[]

for x in range(1):
	#initialization
	a_frames.clear()
	p_frames.clear()
	c_frames.clear()
	authors.clear()
	posts.clear()
	comments.clear()

	time.sleep(10)
	#進入想爬蟲的社團，並輸入關鍵字#
	driver.get(url) #進入想進行爬蟲的社團
	time.sleep(8)
	driver.find_element(By.XPATH,"//div[@aria-label='搜尋']").click()
	driver.find_element(By.XPATH,"//input[@aria-label='搜尋此社團']").send_keys("江綾") #將關鍵字放進搜尋欄
	time.sleep(2)
	driver.find_element(By.XPATH,"//input[@aria-label='搜尋此社團']").send_keys(Keys.ENTER)
	time.sleep(8)

	#抓取data#
	def scroll(times): #下滑載入更多貼文
		for i in range(times):
			js = 'window.scrollTo(0, document.body.scrollHeight);'
			driver.execute_script(js)
			time.sleep(2)
	
	scroll(10)
	
	#用beautifulSoup在粉絲團中找到所有的貼文的tag，方便之後抓取資料，這部分不同的粉絲團可能會有不同的class name#
	soup=Soup(driver.page_source, "lxml")
	a_frames = soup.find_all(class_="x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a")
	p_frames = soup.find_all(class_="x1iorvi4 x1pi30zi x1l90r2v x1swvt13")
	c_frames = soup.find_all(class_="x168nmei x13lgxp2 x30kzoy x9jhf4c x6ikm8r x10wlt62")
	
	for i in c_frames:
		tmp=i.find('span',class_="x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa")
		if(tmp==None):
			comments.append('0則')
		else:
			comments.append(tmp.text)
	
	for j in p_frames:
		tt=j.find('span',class_="x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
		if(tt==None):
			posts.append('0')
		else:
			posts.append(tt.text)
	for k in a_frames:
		t=k.find('a',class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f")
		if(t==None):
			authors.append('0')
		else:
			authors.append(t.text)

	#儲存這些資料#
	fp = open("data2-2.txt", "a")
	for iii in range(len(posts)):
		fp.write("author : ")
		fp.write(authors[iii])
		fp.write("\n")
		fp.write("content : ")
		fp.write(posts[iii])
		fp.write("\n")
		fp.write("comment : ")
		fp.write(comments[iii])
		fp.write("\n")
	fp.close()

driver.quit()
