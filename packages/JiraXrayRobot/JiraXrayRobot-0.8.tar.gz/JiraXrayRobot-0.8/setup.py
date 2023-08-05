from distutils.core import setup
setup(
  name = 'JiraXrayRobot',         
  packages = ['JiraXrayRobot'],   
  version = '0.8',      
  license='GNU General Public License family',
  description = 'Robot Framework Library to Interact with JIRA XRAY',
  author = 'Santanu Ray',
  author_email = 'santanukrray1982@gmail.com',
  url = 'https://github.com/esauray/JiraXrayRobot',
  download_url = 'https://github.com/esauray/JiraXrayRobot/archive/v_08.tar.gz',
  keywords = ['JIRA', 'XRAY', 'ROBOT FRAMEOWRK'],
  install_requires=[            
          'validators',
          'beautifulsoup4',
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)