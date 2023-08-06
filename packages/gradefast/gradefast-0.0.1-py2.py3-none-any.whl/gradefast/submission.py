import urllib.request as urllib2
from bs4 import BeautifulSoup
import requests
import re
import os

class Submission:
    def __init__(self, file_list=[], task_name='Task', team_id=[], types=['zip'], urls=[], id_tags={}, latest=True):
        self.team_id = team_id
        self.task = task_name
        self.urls = urls
        self.types = types
        self.file_list = file_list
        self.id_tags = id_tags
        
    def getTeamids(self):
        return self.team_id

class LoadSubmissions:
    def __init__(self, cookie='', task_url='', fs_location='', types=['zip'], scraper='default'):
        self.task_url = task_url
        self.cookie = cookie
        self.fs_location = fs_location
        self.types = types
        self.submissions = []
        self.scraper = scraper

    @staticmethod    
    def from_url(task_url, cookie, types=['zip'],method='default'):
        return LoadSubmissions(task_url=task_url, cookie=cookie,types=types,scraper = method)

    @staticmethod
    def from_fs(fs_location):
        return LoadSubmissions(fs_location=fs_location)
    
    def getSubmissions(self):
        # scrape urls and other data from webpage
        # returned by the scraper being used
        if self.task_url != '':
            if self.scraper == '' or self.scraper == 'default':
                self.scraper = DefaultScraper
                # submissions.scraper = DefaultScraper
            
            task_name, team_id, urls, id_tags = self.scraper(self.task_url, self.cookie, self.types).scrape_data_from_page()
            # task_name,team_id,urls,id_tags = submissions.scraper(submissions.task_url, submissions.cookie, submissions.types).scrape_data_from_page()
            
            # fill all data inside the submission object
            # TODO:
            submission = Submission(task_name = task_name , team_id = team_id ,types = self.types, urls = urls,id_tags = id_tags)
            # submission.id_tags
            # submissions.append(Submission)
        elif self.fs_location != '':
            # TODO: Submission object should have all the fields filled just like in the from_url case
            # Persist this information in a file like json if you would like and use it to initialize submissions object
            file_list = os.listdir(self.fs_location)
            # team_id = RearrangeFiles()
            submission = Submission(file_list = file_list)
        else:
            print("Neither URL nor File location found. Try again")
            return None
        
        return submission
    
class Scraper:
    def __get_task_name(self):
        # fetch task name from task url
        # OR
        # use data from portal page
        raise NotImplementedError()

    def scrape_data_from_page(self):
        raise NotImplementedError()

class DefaultScraper(Scraper):
    def __init__(self, task_url, cookie, types=['zip']):
        self.task_url = task_url
        self.cookie = cookie
        self.types = types

    def __get_task_name(self):
        # TODO: filter name from URL
        '''
        A method to get name of the task from the URL.        
        '''
        try:
            task_name = re.search('task([a-z A-Z 0-9])+',self.task_url).group()
        except:
            task_name = 'Task'
        return task_name
    
    def getLatest(self,urls):
        latest_urls = {}
        for i in range(0,len(urls)):
            # print(latest_urls.get(urls[i].get_text(),'False') )
            if latest_urls.get(urls[i].get_text(),'False')=='False':
                latest_urls[urls[i].get_text()] = urls[i]
            else:
                if urls[i]['data-tooltip'] > latest_urls[urls[i].get_text()]['data-tooltip']: 
                    latest_urls[urls[i].get_text()] = urls[i]
        t = []
        t = list(latest_urls.values())               
        return t   
    
    # TODO: Except team_ids and file urls also return other data like time of download etc
    def scrape_data_from_page(self):
        '''
        Get the required data from the page.
        '''
        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', 'eyrc_2018_session=' + self.cookie))
        # data.task_url = 'http://23.253.205.190/eyrc18/public/admin/grade/task0'
        # data.task_url = 'http://23.253.205.190/eyrc18/public/admin/grade/task1b'

        web_page = opener.open(self.task_url)
        parsed_web_page = BeautifulSoup(web_page, 'html.parser')

        a_list = parsed_web_page.find_all('a', {'class': 'gradeTeam'})
        id_tags = {}
        team_id = []
        urls = []
        for a in a_list:  
            temp_url = a.parent.parent.find_all('a', {'class': 'waves-effect'})
            temp_url2 =temp_url[:]
            for t in temp_url2:
                if t.get_text() not in self.types:
                    temp_url.remove(t)
                else:
                    # print(t.get_text())
                    pass
            if not temp_url:
                # print('')
                pass
            else:   
                # print(temp_url)
                latest_url = self.getLatest(temp_url)
                for t in latest_url:
                    urls.append(t['href'])
                
                team_id.append(a['data-teamid'])
                id_tags[a['data-teamid']] = latest_url 
        
        task_name = self.__get_task_name()

        return task_name,team_id,urls,id_tags
