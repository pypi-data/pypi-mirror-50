import os
import re
import json

import requests
from bs4 import BeautifulSoup
import urllib.request as urllib2

from gradefast.exceptions import ServerOrScraperException
from urllib.response import addinfourl


class Submission(object):
    def __init__(self,  team_id=1, task='task0', types=['zip'], urls=[], file_list=[], downloaded=False, latest=True):
        self.team_id = team_id
        self.task = task
        self.urls = urls
        self.types = types
        self.file_list = file_list
        self.latest = True
        self.downloaded = False


class LoadSubmissions:
    def __init__(self, cookie='', task_url='', fs_location='', types=['zip'], scraper='default'):
        self.task_url = task_url
        self.cookie = cookie
        self.fs_location = fs_location
        self.types = types
        self.submissions = []
        self.scraper = scraper

    @staticmethod    
    def from_url(task_url, cookie, types=['zip'], method='default'):
        return LoadSubmissions(task_url=task_url, cookie=cookie, types=types, scraper = method)

    @staticmethod
    def from_fs(fs_location):
        return LoadSubmissions(fs_location=fs_location)
    
    def get_submissions(self):
        # scrape urls and other data from webpage
        # returned by the scraper being used
        submissions = []
        if self.task_url != '':
            if self.scraper == '' or self.scraper == 'default':
                self.scraper = DefaultScraper
            
            task, team_id, id_tags = self.scraper(self.task_url, self.cookie, self.types).scrape_data_from_page()
            
            # fill all data inside the submission object
            # TODO:
            for i in range(0, len(team_id)):
                urls = {}
                for j in id_tags[team_id[i]]:
                    urls[j.get_text()] = j['href']
                submissions.append(Submission(task = task , team_id = team_id[i] ,types = self.types, urls = urls))
        elif self.fs_location != '':
            # file_list = os.listdir(self.fs_location)
            # Make changes acc to download for file
            # convert submissions array to json array
            with open(self.fs_location, 'r') as f:
                submissions_dict_arr = json.loads(json.load(f))
                # print(len((submissions_dict_arr)[0]))
                for submission_dict in submissions_dict_arr:
                    submissions.append(Submission(**submission_dict))
                return submissions
        else:
            print("Neither URL nor File location found.Try again")
            return None
        
        return submissions


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
            task_name = re.search('task([a-z A-Z 0-9])+', self.task_url).group()
        except:
            task_name = 'Task'
        return task_name
    
    def get_latest(self, urls):
        latest_urls = {}
        for i in range(0, len(urls)):
            if latest_urls.get(urls[i].get_text(), 'False') == 'False':
                latest_urls[urls[i].get_text()] = urls[i]
            else:
                if urls[i]['data-tooltip'] > latest_urls[urls[i].get_text()]['data-tooltip']: 
                    latest_urls[urls[i].get_text()] = urls[i]
        
        t = []
        uu = list(latest_urls.keys())               
        for u in uu:
            t.append(latest_urls[u])
        return t   

    # TODO: Except team_ids and file urls also return other data like time of download etc
    def scrape_data_from_page(self):
        '''
        Get the required data from the page.
        '''
        
        # if cookie is expired or invalid, the server makes a redirect
        # we can check if the server redirected and throw an exception
        class NoRedirectHandler(urllib2.HTTPRedirectHandler):
            def http_error_302(self, req, fp, code, msg, headers):
                infourl = addinfourl(fp, headers, req.get_full_url())
                infourl.status = code
                infourl.code = code
                return infourl
            http_error_300 = http_error_302
            http_error_301 = http_error_302
            http_error_303 = http_error_302
            http_error_307 = http_error_302

        opener = urllib2.build_opener(NoRedirectHandler())
        opener.addheaders.append(('Cookie', 'eyrc_2018_session=' + self.cookie))
        # data.task_url = 'http://23.253.205.190/eyrc18/public/admin/grade/task0'
        # data.task_url = 'http://23.253.205.190/eyrc18/public/admin/grade/task1b'

        web_page = opener.open(self.task_url)
        # check if cookie is valid? or the request succeeded
        # 2xx is correct code
        if web_page.getcode() / 100 != 2:
            raise ServerOrScraperException()

        parsed_web_page = BeautifulSoup(web_page, 'html.parser')

        a_list = parsed_web_page.find_all('a', {'class': 'gradeTeam'})
        id_tags = {}
        team_id = []
        # urls = []
        for a in a_list:  
            temp_url = a.parent.parent.find_all('a', {'class': 'waves-effect'})
            temp_url2 = temp_url[:]
            for t in temp_url2:
                if t.get_text() not in self.types:
                    temp_url.remove(t)
                # else:
                #   urls.append(t['href'])
            temp_url_latest = self.get_latest(temp_url)
            team_id.append(a['data-teamid'])
            id_tags[a['data-teamid']] = temp_url_latest 
        
        task_name = self.__get_task_name()        
        return task_name, team_id, id_tags
