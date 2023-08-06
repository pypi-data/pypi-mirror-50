from distutils.core import setup
setup(
  name = 'LibSerial6',       
  packages = ['LibSerial6'],   
  version = '0.1',      
  license='MIT',       
  description = 'Biblioteca LibSerial6 Exercicio SENAI ',   
  author = 'Flavio Alberto Lopes Soares',                  
  author_email = 'flavioalsoares@gmail.com',     
  url = 'https://github.com/flavioalsoares/LibSerial6',  
  download_url = 'https://github.com/flavioalsoares/LibSerial6/archive/0.1.tar.gz',    
  keywords = ['Serial', 'Senai', 'ComPort'],  
  install_requires=['datetime'],
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
