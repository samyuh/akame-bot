import discord
import time
import requests

from bs4 import BeautifulSoup

import re

# import embed color/ define embed color
embed_color = embed_color  
# API key
bot_key = bot_key 


@bot.event
async def on_message(message):

	# ignore self messages
	if message.author==bot.user:
		return

	if message.content.startswith('}hi') or message.content.startswith('}hello') or message.content.startswith('}hey'):
		embed=discord.Embed(description='Hello there {}'.format(message.author))
		embed.color=embed_color

		await message.channel.send(embed=embed)

	if message.content.startswith('}info'):
		query_=message.content.split('}info ')[1]
		query=query_.strip().replace(' ','+')
		url='https://next-episode.net/search/?name={}'.format(query)

		
		try:
			
			anime_link=get_top_link(query_,url)
			data_1,data_2=get_data_on_anime(anime_link)
			
			# anime has ended/canceled i.e no upcoming episode
			if data_2==0:
				text_description_1=f'''{data_1['summary']}\n
				> Genre : {data_1['genre']}
				> Average rating : {data_1['rating']}
				> Status : {data_1['status']}
				> Runtime : {data_1['runtime']}
				'''
				
				embed=discord.Embed(title=f"**{data_1['name']}**",description=f'Searched for : {query_}')
				embed.color=embed_color
				embed.add_field(name='**Overview\n**',value=text_description_1)
				embed.set_footer(text='Requested by : {}'.format(message.author))
				
				await message.channel.send(embed=embed)
				
			
			# anime is on-going
			else:
				text_description_1=f'''{data_1['summary']}\n
				> Genre : {data_1['genre']}
				> Average rating : {data_1['rating']}
				> Status : {data_1['status']}
				> Runtime : {data_1['runtime']}
				
				'''
				text_description_2=f'''
				> Season {data_2['season']} Episode {data_2['episode']}
				> Title : {data_2['title']}
				> Time left : {data_2['countdown']}
				> Date : {data_2['date']}

				'''
				embed=discord.Embed(title=f"**{data_1['name']}**",description=f'Searched for : {query_}')
				embed.color=embed_color
				embed.add_field(name='**Overview**',value=f'\n{text_description_1}\n',inline=False)
				embed.add_field(name='\n**Upcoming**\n',value=text_description_2,inline=False)
				embed.set_footer(text='Requested by : {}'.format(message.author))
				await message.channel.send(embed=embed)
		
		except:
			error='No entries found with _{}_ ,try checking the spelling or try a different anime!'.format(query_)
			embed=discord.Embed(title='Error',description=error)
			embed.color=embed_color

			await message.channel.send(embed=embed)

	if message.content.startswith('}help'):

		embed=discord.Embed(title="**Ehixx Bot**",description=help_main)
		embed.color=embed_color
		embed.set_footer(text='Ehixx bot @ 2021')
				
		await message.channel.send(embed=embed)






def get_top_link(query,url):
	'''
	input : url to search query.

	output : returns the link which is at the top of the search result.

	Scans for span class headlinehref and then scrapes the link, the 1st element contains the link for the page for the searched query.

	'''
	# if there are multiple search results , then select the one on top
	try :
		req=requests.get(url)
		soup=BeautifulSoup(req.text,'lxml')

		links_div=soup.find('span',class_='headlinehref')
	
		link=links_div.find_all('a',href=True)
		res=' http://next-episode.net'+str(link[0]['href'])
	
		return res

	# if theres only one search result
	except:
		res='http://next-episode.net/search/?name='+str(query)
		return res

def get_data_on_anime(url):
	'''
	input : link to the page of an anime (searched query)

	output : data relevant to the searched query.

	'''
	
	req=requests.get(url)
	soup=BeautifulSoup(req.text,'lxml')

	anime_title=soup.find('div',id='show_name').text

	anime_summary=soup.find('div',id='summary').text

	div_middle = soup.find('div',id='middle_section').text
	div_middle = re.sub('[\n]+','\n',div_middle)
	data = div_middle.split('\n')

	anime_genre=data[2].split(':')[1]
	anime_rating=data[-5]
	anime_runtime=data[5].split(':')[1]
	anime_runtime=re.sub('[\t]+','',anime_runtime)
	anime_runtime=anime_runtime.split('.')[0]
	anime_status=data[6].split(':')[1]
	anime_status=re.sub('[\t]+','',anime_status)

	res1={'genre':anime_genre,
		 'rating':anime_rating,
		 'status':anime_status,
		 'runtime':anime_runtime,
		 'name':anime_title,
		 'summary':anime_summary}


	# check if anime is on-going
	try:
		div_imp=soup.find('div',id='next_episode').text
		div_imp=re.sub('[\n]+','\n',div_imp)
		div_imp=re.sub('[\t]+','\n',div_imp)
		data=div_imp.split('\n')
			
		anime_title=data[2].split(':')[1]
		anime_countdown=data[3].split(':')[1]
		anime_date=data[4].split(':')[1]
		anime_season=data[6].split(':')[1]
		anime_episode=data[8].split(':')[1]
			
		res2={'title':anime_title,
			'countdown':anime_countdown,
			'date':anime_date,
			'season':anime_season,
			'episode':anime_episode}	
				
		return res1,res2
		
			 	
		# if anime is finished/canceled
	except:
			res2=0
			return res1,res2

help_main='''

	> A friendly and easy to use bot which gives information on any show/anime, along with the countdown for the next episode!
	> to use it enter `}info query` where query will be the name of the show/anime.

	try `}info demon slayer` now! 
'''


bot.run(bot_key)
