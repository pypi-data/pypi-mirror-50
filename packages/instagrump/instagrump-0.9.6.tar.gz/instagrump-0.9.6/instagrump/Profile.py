from bs4 import BeautifulSoup as soup
import requests

class Profile:

	def __init__(self, username):
		api_endp = '__a=1'
		self.username = username
		self.url = 'https://www.instagram.com/%s?%s' % (self.username, api_endp)
		self.data = requests.get(self.url).json()['graphql']['user']
		self.name = self.data['full_name']
		self.is_private = self.data['is_private']
		self.is_verified = self.data['is_verified']
		self.following = self.data['edge_follow']['count']
		self.follower = self.data['edge_followed_by']['count']
		self.biography = self.data['biography']
		self.external_url = self.data['external_url']
		self.id = self.data['id']
		self.is_business_account = self.data['is_business_account']
		self.is_joined_recently = self.data['is_joined_recently']
	def __len__(self):
		posts = self.data['edge_owner_to_timeline_media']['count']
		return posts
	def __str__(self):
		text = str("{}\n".format(self.username)+
				   "{}\n".format(self.name)+
				   "Followers: {:,}\n".format(self.follower)+
				   "Following: {:,}\n".format(self.following)+
				   "Posts: {:,}\n".format(self.__len__()))
		if self.is_private:
			text += "Profile is private\n"
		else:
			storylen = self.get_stories_scraping()
			if storylen:
				text += "Stories: {}\n".format(len(storylen))
			else:
				text += "Profile has no story\n"
		if self.biography:
			text += "Biography:\n{}\n".format(self.biography)
		if self.external_url:
			text += "\nUrl:\n{}\ninstagram.com/{}".format(self.external_url, self.username)
		else:
			text += "\nUrl:\ninstagram.com/{}".format(self.username)
		text = text.replace('https://','').replace('http://','').replace('www.','')
		return text

	def get_avatar(self):
		return self.data['profile_pic_url_hd']

	def get_hd_avatar(self):
		data = requests.get('https://www.instadp.com/profile/'+self.username)
		data = soup(data.text, 'html.parser')
		data = data.find('img').get('src')
		return data

	def get_stories_scraping(self):
		if not self.is_private:
			sto = requests.get('https://www.instadp.com/stories/'+self.username)
			page = soup(sto.text, 'html.parser')
			data = page.find('body').find('article',{'class':'content'}).find('div',{'class':'centered'})
			check = data.find('section',{'class':'result-content'}).find('div',{'class':'result-private'})
			if not check:
				data = data.find('section',{'class','result-content'}).find('ul',{'class':'stories-list'})
				try:
					data = data.find_all('li',{'class':'story'})
				except:
					self.get_stories_scraping()
				if not data:
					return None
				return data
		return False

	def get_stories(self):
		for i in range(2):
			data = self.get_stories_scraping()
		if data:
			results = []
			for item in data:
				result = item.find('div',{'class':'story-post'})
				content = result.find('img')
				if not content:
					content = item.find('video').get('poster')
					content1 = item.find('source').get('src')
					results += [[content1,content]]
					continue
				results += [[content.get('src')]]
			results = results[::-1]
			return results
		return None

	def get_posts(self):
		data = self.data['edge_owner_to_timeline_media']['edges']
		result = []
		for node in data:
			result.append('https://www.instagram.com/p/%s' % node['node']['shortcode'])
		return result

	def get_igtv(self):
		data = self.data['edge_felix_video_timeline']['edges']
		result = []
		for node in data:
			result.append('https://www.instagram.com/tv/%s' % node['node']['shortcode'])
		return result





