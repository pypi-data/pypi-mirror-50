from distutils.core import setup
setup(
  name = 'LibSerial0',       
  packages = ['LibSerial0'],   
  version = '0.2',      
  license='MIT',       
  description = 'Biblioteca LibSerial0 ',   
  author = 'Fernando Simplicio',                  
  author_email = 'fernando@microgenios.com.br',     
  url = 'https://github.com/microgenios/LibSerial0',  
  download_url = 'https://github.com/microgenios/LibSerial0/archive/0.2.tar.gz',    
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