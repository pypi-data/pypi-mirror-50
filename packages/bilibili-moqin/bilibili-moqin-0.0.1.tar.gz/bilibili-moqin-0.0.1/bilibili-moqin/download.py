import requests,json,os,re,time
from bs4 import BeautifulSoup
from contextlib import closing

class ProgressBar(object):
	'''进度条类，提供一个格式化的进度条'''
	def __init__(self, title,
				 count=0.0,
				 run_status=None,
				 fin_status=None,
				 total=100.0,
				 unit='', sep='/',
				 chunk_size=1.0):
		super(ProgressBar, self).__init__()
		self.info = "【%s】%s %.2f %s %s %.2f %s"
		self.title = title
		self.total = total
		self.count = count
		self.chunk_size = chunk_size
		self.status = run_status or ""
		self.fin_status = fin_status or " " * len(self.status)
		self.unit = unit
		self.seq = sep

	def __get_info(self):
		# 【名称】状态 进度 单位 分割线 总数 单位
		_info = self.info % (self.title, self.status,
							 self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
		return _info

	def refresh(self, count=1, status=None):
		self.count += count
		# if status is not None:
		self.status = status or self.status
		end_str = "\r"
		if self.count >= self.total:
			end_str = '\n'
			self.status = status or self.fin_status
		if self.count%1000==0:
			print(self.__get_info(), end=end_str)

def search(keyword):# 0返回av号list；1返回标题list
	'''搜索及获取视频的av号，该方法共有'''
	search_url="https://search.bilibili.com/all?keyword="+keyword
	s = requests.session() 
	proxies={'http':'120.83.99.148:9999'}
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
	search_res_html = BeautifulSoup(s.get(search_url,proxies=proxies,headers=headers).content,features="lxml")
	a_res=search_res_html.findAll('a',{'class':'title'})
	match=re.compile(r"\d+")
	av_list=[];title_list=[]
	i=0
	for av_DOM in a_res:
		i+=1
		av_num=(re.search(match,av_DOM['href'])).group()
		title=str(i)+"、"+av_DOM['title']
		print(title)
		av_list.append(av_num)
		title_list.append(title)
	return av_list,title_list

class av_download():
	'''
	本类提供bilibili的搜索以及选择视频下载
	有如下方法
	get_cid(self,av_num) 获取视频的cid
	get_playurl(self,av_num,cid) 拼接aid和cid，获取真实下载地址
	'''
	def __init__(self,av_info,*choose):
		'''
		参数说明：av_info：搜索结果，由bilibili.search()返回. 类型dict，结构{[av_list],[title_list]}
					av_info还可以是单纯的av号 eg：30724586，类型int，此时choose不填
				 choose：可选参数，选择的视频序号. 类型int，从1开始，在使用搜索下载时须填写
		'''
		av_info=av_info
		if isinstance(av_info,int):
			av=av_info
			cid_and_title_dict=self.get_cid(av)
			cid_list=cid_and_title_dict[0]
			filename_list=cid_and_title_dict[1]
			for i in range(len(cid_list)):
				cid=cid_list[i];filename=filename_list[i]
				url=self.get_playurl(av,cid)
				self.download(url,filename) #调用外层公用类函数
		else:
			av_list=av_info[0]
			choose=int(choose[0]) #这里是选择下载的条目
			av=av_list[choose-1]
			cid_and_title_dict=self.get_cid(av)
			cid_list=cid_and_title_dict[0]
			filename_list=cid_and_title_dict[1]
			for i in range(len(cid_list)):
				cid=cid_list[i];filename=filename_list[i]
				url=self.get_playurl(av,cid)
				self.download(url,filename)

	

	def download(self,playurl,filename):
		with closing(requests.get(playurl, stream=True)) as response:
			chunk_size = 1024 # 单次请求最大值
			content_size = int(response.headers['content-length']) # 内容体总大小
			progress = ProgressBar(filename, total=content_size,
											 unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
			with open(filename+".flv", "wb") as file:
				for data in response.iter_content(chunk_size=chunk_size):
					file.write(data)
					progress.refresh(count=len(data))
				print("下载完成")

	
	def get_cid(self,av_num):
		url="https://api.bilibili.com/x/player/pagelist?aid="+str(av_num)
		cid_xhr=json.loads(requests.get(url).text)
		data_list=cid_xhr['data']
		cid_list=[];filename_list=[]
		for i in data_list:
			cid_list.append(i['cid'])
			filename_list.append(i['part'])
		return cid_list,filename_list
	
	def get_playurl(self,av_num,cid):
		url="https://api.bilibili.com/x/player/playurl?avid="+str(av_num)+"&cid="+str(cid)
		playurl_xhr=json.loads(requests.get(url).text)
		playurl=playurl_xhr['data']['durl'][0]['url']
		match1=re.compile(r'&platform=pc')
		match2=re.compile(r'http.+&uparams')
		try:
			playurl=re.sub(match1,"",playurl)
		except:
			playurl=playurl
		try:
			playurl=re.search(match2,playurl).group()
		except:
			playurl=playurl
		
		print(playurl)
		return playurl
	
	

class au_download():
	'''
	本类提供b站音频下载
	输入amxxxxx识别为歌单下载
	输入auxxxxx识别为单曲下载
	'''
	
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
	def __init__(self,sid):

		if sid[0:2]=='am':
			self.from_songsheet(sid[2:])
		else:
			self.from_onlysong(sid[2:])
	
	def own_download(self,playurl,filename): #此处为歌曲类的私有下载器，与上视频类的下载方式不同，不可混用
		req=requests.get(playurl,headers=self.headers)
		with open(filename+".mp3","wb") as f :
			f.write(req.content)
			print(filename+"下载完成")

	def get_url(self,music_id):
		url="https://www.bilibili.com/audio/music-service-c/web/url?sid="+str(music_id)
		playurl=json.loads(requests.get(url).text)['data']['cdns'][0]
		return playurl
	
	def get_title(self,music_id):
		url="https://www.bilibili.com/audio/music-service-c/web/song/info?sid="+str(music_id)
		title=json.loads(requests.get(url).text)['data']['title']
		return title

	def from_songsheet(self,songsheet_id):
		sid=str(songsheet_id)
		url="https://www.bilibili.com/audio/music-service-c/web/song/of-menu?sid="+sid+"&pn=1&ps=100"
		songsheet_data_list=json.loads(requests.get(url).text)['data']['data']
		id_list=[];author_list=[];title_list=[]
		for i in range(len(songsheet_data_list)):
			id_list.append(songsheet_data_list[i]['id'])
			author_list.append(songsheet_data_list[i]['author'])
			title_list.append(songsheet_data_list[i]['title'])
		for i in range(len(id_list)):
			self.own_download(self.get_url(id_list[i]),filename=title_list[i])

	def from_onlysong(self,song_id):
		filename=self.get_title(song_id)
		url=self.get_url(song_id)
		self.own_download(url,filename)



class mc_download():
	'''
	1. https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web
		POST  {"ep_id":209069}
	2. https://is.hdslb.com/bfs/manga/24442/209069/data.index?token=73441250b03e3f16%3A6bfio0T2LdZ2Yc8h0obsc9pYweo%3D%3A1565536027
		GET
	3. https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web
		POST  {"urls":"[\"/bfs/manga/b1ebfc000ffd300d09ed93c87a9325b2dff50c7e.jpg\"]"}
	4. https://is.hdslb.com/bfs/manga/b1ebfc000ffd300d09ed93c87a9325b2dff50c7e.jpg@903w.jpg?token=73441250b03e3f16%3A29vxOv7F%2B7iuD2nFZHL5kFob2Os%3D%3A1565536029
		GET
	'''
	pass