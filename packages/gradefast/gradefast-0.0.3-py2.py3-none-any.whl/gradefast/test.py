import os
import subprocess

from enum import Enum

class TestType(Enum):
    FILE=1
    PKG=2
    SCRIPT=3

class Test:
    def __init__(self, test_script_location, entry_point, type=TestType.FILE, plagiarism_check=False):
        # A test consists of a test_script file written by theme developers 
        # and a test entry point usually present in student submissions
        
        # The test script will be written in python. The test script will have 
        # a call to dependencies like :
        # 1. 

        # The Entry Points can be a:
        # 1. directory 
        # 2. program file like .c or .py 
        # 3. result.txt or result.png file 
        
        self.test_script_location = test_script_location

    # def _subprocess(self, cwd, program='python'):
    #     working_dir = os.path.dirname(test_script_location)
    #     proc = subprocess.Popen([program, self.test_script_location], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_dir)
    #     stdout, stderr = proc.communicate()

    def __call__(self, submission):
        if type == TestType.FILE:
            working_dir = os.path.dirname(test_script_location)
            proc = subprocess.Popen([
                "python", self.test_script_location,
                "-f", submission.task + "_" + self.entry_point + ".txt",
                "--team-id", submission.team_id], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_dir)
            stdout, stderr = proc.communicate()
        pass
