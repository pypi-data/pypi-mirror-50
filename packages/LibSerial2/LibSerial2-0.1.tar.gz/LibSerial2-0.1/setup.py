from distutils.core import setup
setup(
  name = 'LibSerial2',       
  packages = ['LibSerial2'],   
  version = '0.1',      
  license='MIT',       
  description = 'Biblioteca LibSerial2 ',   
  author = 'Bruno Mena',                  
  author_email = 'brunogrejanin339@gmail.com',     
  url = 'https://github.com/brunomena/LibSerial2',  
  download_url = 'https://github.com/brunomena/LibSerial2/archive/0.1.tar.gz' ,
  keywords = ['Serial', 'Senai', 'ComPort'],  
  install_requires=[           
          'datetime',
          'random',         
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