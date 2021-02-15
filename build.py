import pip
def install(package):
    pip.main(['install', package])
install('lxml')
install('requests')
install('selenium')
install('beautifulsoup4')
print('\nModule installation Successfull, Now Run main.py file')