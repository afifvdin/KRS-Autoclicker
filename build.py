import pip
def install(package):
    pip.main(['install', package])
install('lxml')
install('requests')
install('selenium')
install('beautifulsoap4')
print('\nModule installation Successfull, Now Run main.py file')