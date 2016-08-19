import ui
import console
import requests
import utils
import urllib.parse
import novelDetails

class searchView(ui.View):
	def __init__(self):
		self.name='小説検索'
		self.background_color='white'
		self.searchButton=ui.ButtonItem()
		self.searchButton.title='検索'
		self.searchButton.action=self.startSearch
		self.right_button_items=[
			self.searchButton
		]
		self.wordInput = ui.TextField()
		self.wordInput.x=1
		self.wordInput.y=1
		self.wordInput.width=318
		self.wordInput.placeholder='検索ワード'
		self.wordInput.text='re:ゼロから'
		self.wordInput.height=32
		self.add_subview(self.wordInput)
	def startSearch(self,ev):
		console.show_activity('検索中')
		@utils.background
		def bg():
			data={
				'out':'json',
				'word':self.wordInput.text
			}
			data=urllib.parse.urlencode(data)
			print(data)
			res = requests.get('http://api.syosetu.com/novelapi/api/?'+data).json()
			@utils.foreground
			def fg():
				console.hide_activity()
				resultView(res,self.wordInput.text).present()
class resultView(ui.View):
	def __init__(self,res,word):
		self.name='「'+word+'」の検索結果'
		self.listview=ui.TableView()
		self.listview.flex='WH'
		self.listview.action=self.showDetails
		self.ds = ui.ListDataSource([])
		for novel in res[1:]:
			self.ds.items.append({
				'title':novel['title'],
				'raw':novel
			})
		self.listview.data_source = self.ds
		self.listview.delegate = self.ds
		self.ds.action=self.showDetails
		self.add_subview(self.listview)
	def showDetails(self,ev):
		novelDetails.detailView(ev.items[ev.selected_row]['raw']).present()
