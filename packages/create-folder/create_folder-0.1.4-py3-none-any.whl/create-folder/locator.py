'''
This is the main script of our python package
'''
# importing the requests library
import requests
import os
from functools import partial

def makefolders(root_dir, subfolders):
    concat_path = partial(os.path.join, root_dir)
    makedirs = partial(os.makedirs)  # Python 3.2+
    for path in map(concat_path, subfolders):
        makedirs(path)

if __name__=='__main__':
    root_dir = 'Testing/GenericFramwork'
    subfolders = ('Scripts\Server', 'Middleware', 'Hal','Tools', 'Binaries','Logs')
    makefolders(root_dir, subfolders) 
