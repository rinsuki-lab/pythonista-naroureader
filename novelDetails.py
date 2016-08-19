import ui
import requests
from bs4 import BeautifulSoup
import utils
import console
import re
import webbrowser
class detailView (ui.View):
	def __init__(self,info):
		print(info)
		self.name=info['title']
		self.background_color='#bbb'
		self.arasuzi = ui.TextView()
		self.arasuzi.text = info['story']
		self.arasuzi.height = 139
		self.arasuzi.flex='W'
		self.arasuzi.editable=False
		self.list = ui.TableView()
		self.list.y=140
		self.list.flex='W'
		self.data=ui.ListDataSource([])
		self.list.data_source=self.data
		self.list.delegate=self.data
		self.add_subview(self.arasuzi)
		self.add_subview(self.list)
		console.show_activity('詳細取得中')
		@utils.background
		def bg():
			novel=requests.get('http://ncode.syosetu.com/'+info['ncode'])
			novel.encoding='UTF-8'
			novel_soup = BeautifulSoup(novel.text)
			storys_soup = novel_soup.select('.index_box > *')
			print(storys_soup)
			storys=[]
			cnt=0
			for story_soup in storys_soup:
				if(story_soup.name=='div'):
					# 説明
					storys.append({
						'title':story_soup.string
					})
				elif(story_soup.select('a')!=[]):
					cnt+=1
					storys.append({
						'title':story_soup.select('a')[0].string,
						'accessory_type':'disclosure_indicator',
						'num':cnt
					})
			self.dlid=re.search('\\/ncode\\/([0-9]+)\\/',novel_soup.select('#novel_footer > ul > li')[2].select('a')[0].get('href')).group(1)
			print(self.dlid)
			@utils.foreground
			def fg():
				print(storys)
				self.data.items=storys
				self.data.reload()
				self.data.action=self.tapped
				console.hide_activity()
	def layout(self):
		self.arasuzi.height=(self.height/3)-1
		self.list.y=self.height/3
		self.list.height=(self.height/3)*2
		pass
	def tapped(self,ev):
		console.show_activity('ダウンロード中')
		@utils.background
		def bg():
			num=ev.items[ev.selected_row].get('num')
			if(not num):
				return
			url='http://ncode.syosetu.com/txtdownload/dlstart/ncode/'+str(self.dlid)+'/?no='+str(num)+'&hankaku=0&code=utf-8&kaigyo=crlf'
			r=requests.get(url)
			r.encoding='UTF-8'
			@utils.foreground
			def fg():
				console.hide_activity()
				v=storyView(ev.items[ev.selected_row].get('title'),r.text)
				v.present()
class storyView(ui.View):
	def __init__(self,title,text):
		self.text=ui.TextView()
		self.text.text=text
		self.text.flex='WH'
		self.text.editable=False
		self.text.font=('<system>',16)
		self.add_subview(self.text)
		self.name=title
