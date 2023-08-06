import requests,json,os,re,time
from bs4 import BeautifulSoup
from contextlib import closing

class av_data():
	def __init__(self):
		pass

	def get_cid(self,av_num):
		url="https://api.bilibili.com/x/player/pagelist?aid="+str(av_num)
		cid_xhr=json.loads(requests.get(url).text)
		cid=cid_xhr['data'][0]['cid']
		filename=cid_xhr['data'][0]['part']
		return cid,filename

	def get_av_info(self,av_num):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
		}
		cid=self.get_cid(av_num)[0]
		url="https://api.bilibili.com/x/web-interface/archive/stat?aid="+str(av_num)
		av_info=json.loads(requests.get(url,headers=headers).text)
		return av_info

	def get_coin(self,av_info):
		coin_info=av_info['data']['coin']
		return coin_info
	
	def get_view(self,av_info):
		view_info=av_info['data']['view']
		return view_info

	def get_danmaku(self,av_info):
		danmaku_info=av_info['data']['danmaku']
		return danmaku_info

	def get_reply(self,av_info):
		reply_info=av_info['data']['reply']
		return reply_info

	def get_favorite(self,av_info):
		favorite_info=av_info['data']['favorite']
		return favorite_info

	def get_share(self,av_info):
		share_info=av_info['data']['share']
		return share_info

	def get_like(self,av_info):
		like_info=av_info['data']['like']
		return like_info


class comments_data():
	def __init__(self):
		pass
	def get_reply_list(self,VideoId, pages_number): # 传入两个参数分别是视频的ID和评论的页数
		video_url = 'https://api.bilibili.com/x/v2/reply' #设置请求地址
		video_url_headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
		}
		reply_list=[]
		# 按照页数循环
		for numbers in range(pages_number):
			time.sleep(0.3) #因为需要循环爬取，须设置延时
			# 设置GET请求参数
			video_url_params = {
				'jsonp': 'jsonp',
				'pn': numbers+1,  # 页数从0开始的所以要+1
				'type': '1',
				'oid': VideoId,  # 视频id
				'sort': '0',
			}
			# 获得评论列表
			reply_list.append(requests.get(video_url, params=video_url_params,headers=video_url_headers).json()['data']['replies']) # 这里直接取出评论列表
		return reply_list

	def get_reply_content(self,reply_list):
		reply_content_list=[]
		for page in range(len(reply_list)):
			for i in range(len(reply_list[page])):
				reply_content_list.append(reply_list[page][i]['content']['message'])
			return reply_content_list
		return reply_content_list

	def get_reply_user(self,reply_list):
		reply_uname_list=[]
		for page in range(len(reply_list)):
			for i in range(len(reply_list[page])):
				reply_uname_list.append(reply_list[page][i]['member']['uname'])
		return reply_uname_list


class danmaku_data():
	"""docstring for danmaku_data"""
	def get_cid(self,av_num):
		url="https://api.bilibili.com/x/player/pagelist?aid="+str(av_num)
		cid_xhr=json.loads(requests.get(url).text)
		data_list=cid_xhr['data']
		cid_list=[];filename_list=[]
		for i in data_list:
			cid_list.append(i['cid'])
		return cid_list

		

	def get_danmaku_list(self,av_num):
		headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
				}
		url_list=[]
		cid_list=self.get_cid(av_num)
		for i in range(len(cid_list)):
			url="https://api.bilibili.com/x/v1/dm/list.so?oid="+str(cid_list[i])
			url_list.append(url)
		danmaku_list=[]
		for k in range(len(url_list)):
			url=url_list[k]
			time.sleep(0.3)
			s=BeautifulSoup(requests.get(url,headers=headers).content,features="lxml")
			pre_danmaku_list=s.findAll('d')
			for j in range(len(pre_danmaku_list)):
				danmaku_list.append(pre_danmaku_list[j].text)
		return danmaku_list


class authorpage_data():

	def get_author_video(self,mid):
		headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
				}
		
		url="https://space.bilibili.com/ajax/member/getSubmitVideos?mid="+str(mid)+"&pagesize=100"
		authorpage_data=json.loads(requests.get(url,headers=headers).text)['data']
		page=authorpage_data['pages']
		total=authorpage_data['count']
		video_data=authorpage_data['vlist']
		video_list=[]
		for i in range(len(video_data)):
			temp_dict={}
			title=video_data[i]['title']
			av_num=video_data[i]['aid']
			temp_dict['title']=title
			temp_dict['aid']=av_num
			video_list.append(temp_dict)
		return video_list

	

