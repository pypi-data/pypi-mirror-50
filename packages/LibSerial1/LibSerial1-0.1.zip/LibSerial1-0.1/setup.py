from distutils.core import setup
setup(
  name = 'LibSerial1',       
  packages = ['LibSerial1'],   
  version = '0.1',      
  license='MIT',       
  description = 'Biblioteca LibSerial1 ',   
  author = 'Sergio Pastori',                  
  author_email = 'sergiopastori@gmail.com',     
  url = 'https://github.com/sergiopastori/LibSerial1',  
  download_url = 'https://github.com/sergiopastori/LibSerial1/archive/0.1.tar.gz',    
  keywords = ['Serial', 'Senai', 'ComPort'],  
  install_requires=[           
          'datetime',
          'random',         
      ],
  classifiers=[
    #"3 - Alpha", "4 - Beta" or "5 - Production/Stable"   
    'Development Status :: 3 - Alpha',   
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
  ],
)