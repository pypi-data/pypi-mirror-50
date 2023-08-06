import requests
from bs4 import BeautifulSoup as soup


PUBLIC_ENDP = 'https://www.instagram.com/{}?__a=1'
USER_INFO_ENDP = 'https://i.instagram.com/api/v1/users/{}/info'

class Profile:

	def __init__(self, username):

		# Avoid JSON not found
		for i in range(2):
			data = requests.get(PUBLIC_ENDP.format(username))

		self.logging_page_id = data.json()['logging_page_id']
		self.data = data.json()['graphql']['user']
		self.id = self.data['id']
		self.meta_url = USER_INFO_ENDP.format(self.id)
		self.name = self.data['full_name']
		self.username = self.data['username']
		self.is_private = self.data['is_private']
		self.posts = self.data['edge_owner_to_timeline_media']
		self.posts_length = self.posts['count']
		self.is_verified = self.data['is_verified']
		self.following = self.data['edge_follow']['count']
		self.follower = self.data['edge_followed_by']['count']
		self.biography = self.data['biography']
		self.external_url = self.data['external_url']
		self.is_business_account = self.data['is_business_account']
		self.is_joined_recently = self.data['is_joined_recently']

	def __len__(self):
		return self.posts_length

	def __str__(self):
		data = str("{}\n".format(self.username)
				  +"{}\n".format(self.name)
				  +"Followers: {:,}\n".format(self.follower)
				  +"Following: {:,}\n".format(self.following)
				  +"Posts: {:,}\n".format(self.__len__()))
		data += "Stories: "
		if self.is_private:
			data += "Private\n"
		else:
			storylen = self.get_stories_scraping()
			if storylen:
				data += "{}\n".format(len(storylen))
			else:
				data += "0\n"
		if self.biography:
			data += "Biography:\n{}\n".format(self.biography)
		if self.external_url:
			data += "\nUrl:\n{}\ninstagram.com/{}".format(self.external_url, self.username)
		else:
			data += "\nUrl:\ninstagram.com/{}".format(self.username)
		data = data.replace('https://','').replace('http://','').replace('www.','')
		return data

	def get_avatar(self):
		data = requests.get(self.meta_url).json()['user']
		result = []
		for item in data['hd_profile_pic_versions']:
			result += [{'width': item['width'], 'height': item['height'], 'url': item['url']}]
		item = data['hd_profile_pic_url_info']
		result += [{'width': item['width'], 'height': item['height'], 'url': item['url']}]
		return result

	def get_stories_scraping(self):
		if not self.is_private:

			# Avoid HTML tags not found
			for i in range(2):
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
		data = self.get_stories_scraping()
		if data:
			results = []

			for item in data:
				content = item.find('div',{'class':'story-post'})
				content = content.find('img')
				if not content:
					content = item.find('video').get('poster')
					content1 = item.find('source').get('src')
					results += [[content1, content]]
					continue
				results += [[content.get('src')]]

			results = results[::-1]
			return results

		return None

	def get_posts(self):
		data = self.posts['edges']
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





