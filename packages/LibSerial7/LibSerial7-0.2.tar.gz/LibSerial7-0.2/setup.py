from distutils.core import setup
setup(
  name = 'LibSerial7',       
  packages = ['LibSerial7'],   
  version = '0.2',      
  license='MIT',       
  description = 'Biblioteca LibSerial7 ',   
  author = 'Jaemilton',                  
  author_email = 'jaemilton@gmail.com',     
  url = 'https://github.com/jaemilton/LibSerial7',  
  download_url = 'https://github.com/jaemilton/LibSerial7/archive/0.1.tar.gz',    
  keywords = ['Serial', 'Senai', 'ComPort'],  
  install_requires=[           
          'datetime',       
      ],
  classifiers=[
    #"3 - Alpha", "4 - Beta" or "5 - Production/Stable"   
    'Development Status :: 5 - Production/Stable',   
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
  ],
)