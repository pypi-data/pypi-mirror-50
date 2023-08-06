import os
import sys
import time
import datetime

import json
import zipfile
import logging
import threading

import requests
from gradefast.submission import submission
from gradefast.exceptions import *

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)


class Filter:
    '''A class for filtering team ids that are to be downloaded'''
    def __init__(self):
        pass

    def filter_by_range(self, key):
        if key >= self.left and key <= self.right:
            return True
        else: 
            return False

    def filter_by_collection(self, key):
        if key in self.list_of_teams:
            return True
        else: 
            return False
        
    def __call__(self, submissions, list_of_teams=[], range_team_id=[]):
        '''
        :type submission : Submission object
        :param submission : Submission object containing team ids, urls and id_tags dictionary.
        '''
        
        flag = 0 # 0: specific teams 1: range
        
        self.submissions = submissions
        self.list_of_teams = list_of_teams
        self.range_team_id = range_team_id

        if list_of_teams != None and len(list_of_teams) != 0:
            flag = 0
            return list(filter(self.filter_by_collection, self.submissions))
        elif self.range_team_id != None and  len(self.range_team_id) != 0: 
            if self.range_team_id[0] > self.range_team_id[1] or len(self.range_team_id) != 1:
                flag = 1
                return list(filter(self.filter_by_range, self.submissions))
            else:
                raise RangeError()
        else:
            raise FilterException()


def setup_logger(name, log_file, level=logging.INFO):
    '''Function setup as many loggers as you want'''

    formatter = logging.Formatter('%(asctime)s %(message)s')
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger


# TODO (manjrekarom):
# 1. Retry feature not implemented
class Download:
    ''' A utility class to download data from portal '''
    def __init__(self, cookie, storage_location = '.', extract=False, 
                 keep_original=True, retry=True, retry_times=2):
        '''
        :type cookie : string
        :param cookie : Cookie
        
        :type storage_location : string
        :param storage_location : The location where the data is to be downloaded
        
        :type extract : Boolean
        :param extract : 

        :type keep_original : Boolean
        :param keep_original : 

        :type retry : Boolean
        :param retry : 

        :type retry_times : int
        :param retry_times : 

        '''
        self.cookie = cookie
        self.storage_location = storage_location
        

    def __call__(self, submissions):
        '''
        :type submission : Submission object
        :param submission : Submission object containing required information like url,team_id,etc

        '''
        # First make a parent folder
        directory_name = ''
        if submissions != None and len(submissions) > 0:
            directory_name = "{}_{}".format(submissions[0].task, datetime.datetime.now().strftime("%Y_%m_%d-%H_%M"))
        else:
            raise EmptySubmissionsException()
            
        path = os.path.join(self.storage_location, directory_name)
        if not os.path.isdir(path):
            os.makedirs(path, 0o755)
        self.storage_location = path

        # Setting up download success and failure loggers
        self.logger1 = setup_logger('download_success', os.path.join(self.storage_location,'download_success.log'),level = logging.INFO)
        self.logger2 = setup_logger('download_failed', os.path.join(self.storage_location,'download_failed.log'),level = logging.INFO)

        # Create a folder for every team and download every file inside the folder
        # TODO (manjrekarom): Paste a submissions log csv file with submissions downloaded 
        # marked as downloaded = True
        # This file should be kept in storage_location which will later be used to do `from_fs`
        # count = len(submission.team_id)

        cookie = {'eyrc_2018_session': self.cookie}
        print('Download {} files:'.format(len(submissions)))
        spinner = Spinner()
        
        list_of_data = []
        for submission in submissions:
            team_id = submission.team_id
            urls = submission.urls
            sys.stdout.write('Downloading for Team-id: {}: '.format(team_id))
            spinner.start()

            if not os.path.isdir(os.path.join(self.storage_location,team_id)):
                os.mkdir(os.path.join(self.storage_location,team_id))        

            try:
                for file_type, url in urls.items():
                    r = requests.get(url = url, allow_redirects=True, cookies=cookie)

                    with open(os.path.join(self.storage_location, team_id, team_id + '.' + file_type), 'wb') as file:
                        file.write(r.content)
                        list_of_data.append(team_id + '.' + file_type)
                    sys.stdout.write('\b Success!\n')
                    self.logger1.info(team_id + ' ' + file_type + ' successfully downloaded.')
                spinner.stop()

            except Exception as e:
                spinner.stop()
                sys.stdout.write('\bFailed.. Trying next file\n')
                self.logger2.info(team_id + ' ' + file_type + ' failed to download.' + str(e))

        # write a json to create a submissions object from
        return list_of_data, self.storage_location


class Extract:
    '''A class for extracting zips downloaded from the portals '''
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
    
    
    def __call__(name_of_zip, location_of_zips, target_path):
        '''
        :type name_of_zip: string
        :param name_of_zip : The name of zip to be extrated
        
        :type location_of_zips: string
        :param location_of_zips : The location where the zip is located
        
        :type target_path: string
        :param target_path: The location where the zip is to be extracted
        
        '''
        path_to_zip_file = os.path.join(location_of_zips, name_of_zip)
        directory_to_extract_to = target_path
        
        zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
        zip_ref.extractall(directory_to_extract_to)
        zip_ref.close()


class Persist:
    @staticmethod
    def from_json(path_to_submission_json_file):
        # convert submissions array to json array
        submissions = []
        with open(path_to_submission_json_file, 'r') as f:
            submissions_dict_arr = json.loads(json.load(f))
            # print(len((submissions_dict_arr)[0]))
            for submission_dict in submissions_dict_arr:
                submissions.append(Submission(**submission_dict))
            return submissions

    @staticmethod
    def to_json(submissions, save_location='./'):
        # convert submissions array to json array
        json_list = []
        for i in submissions:
            json_list.append(i.__dict__)
        json_data = json.dumps(json_list)

        with open(os.path.join(save_location, 'submission.json'), 'w') as outfile:
            json.dump(json_data, outfile)
    
    @staticmethod
    def to_database():
        pass


class Plagiarism:
    @staticmethod
    def check():
        pass
