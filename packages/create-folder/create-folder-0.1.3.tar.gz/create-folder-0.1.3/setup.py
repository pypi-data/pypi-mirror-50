from setuptools import setup
import os
import glob
import shutil
import subprocess


# reading long description from file
with open('DESCRIPTION.txt','r') as file:
    long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = ['requests']

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    ]

# calling the setup function 
setup(name='create-folder',
      version='0.1.3',
      description='To create folder and Subfolder',
      long_description=long_description,
      #url='',
      author='Deepankar',
      author_email='deepankarx.borgohain@intel.com',
      license='MIT',
      packages=['create-folder'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='Folders'
      )
## Executing the python main script
old_wd = os.getcwd()
x = os.chdir("create-folder")
print ("Change the current directory")
# varify the path using getcwd() 
cwd = os.getcwd()
# print the current directory 
print("Current working directory is:", cwd)
for file in glob.glob("locator.py"):
    print ("File", os.path.join(cwd,file))
    os.chdir(old_wd)
    print (old_wd)
    shutil.copy(os.path.join(cwd,file),old_wd)

process = subprocess.Popen(['python', 'locator.py'], stdout = subprocess.PIPE )

