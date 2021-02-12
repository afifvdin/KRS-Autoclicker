#-------- Import Package
import pip, requests, os, zipfile, time, lxml

def mainMenu(driverPath):
    #-------- Set Username Password
    uname = input('NIM = ')
    pwd = str(input('Password = '))

    #-------- Set Main Info
    semester = int(input('Semester? '))
    count = int(input('Berapa Mata Kuliah = '))
    print('\n----- HINT -----')
    print('Bukalah siakad > Kartu Rencana Studi > Tambah Mata Kuliah > Klik semester anda > Inspect Element checkboxnya untuk setiap mata kuliah > Input class nya ke terminal\n')
    matkul = [str(input('Mata Kuliah = ')) for n in range(count)]
    print('\n----- HINT -----')
    print('Input pilihan kelas anda urut dari atas [A = 1, B = 2, C = 3, D = 4], misal : \nMatkul A = C\nMatkul B = D\nMatkul C = A')
    print('Maka inputnya > 3 > 4 > 1\n')
    choose = [int(input('Pilihan Kelas (Urut dari atas) = ')) for i in range(count)]
    print('\nNote!! Ctrl+C to Stop!')

    #-------- Starting

    #-------- Open Web Browser and go to URL
    driver = webdriver.Chrome(driverPath+'\chromedriver.exe')
    driver.get('https://siakad.trunojoyo.ac.id')
    print()

    #-------- Find Username and Password
    homepage = driver.find_element_by_id('username')
    homepage.send_keys(uname)
    homepage = driver.find_element_by_id('password')
    homepage.send_keys(pwd)
    homepage.send_keys(Keys.RETURN)

    #-------- Copy HTML Code to Analyze later
    tryOne = driver.page_source
    with open('file.html', 'w') as f:
        f.write(tryOne)

    #-------- Find Something in file :)
    openFile = BeautifulSoup(open('file.html'), features="lxml")
    for tagSearch in openFile.find_all('a'):
        if tagSearch.text == 'Kartu Rencana Studi':
            theLink = str(tagSearch['href'])
            driver.get(theLink)
            break
    complete = False
    while complete == False:
        try:
            krs = driver.find_element_by_name('btnProses')
        except:
            print("KRS Belum dibuka...\nExiting...")
            time.sleep(1)
            break
        driver.execute_script("arguments[0].click()", krs)

        #-------- Go to URL
        driver.execute_script("javascript:Effect.toggle({},'blind')".format(('semester_' + str(semester))))

        #-------- Select your course
        for i in range(len(matkul)):
            chs = choose[i]
            checknow = driver.find_elements_by_class_name(matkul[i])
            count = 1
            found = False
            for j in checknow:
                if count == chs and found == False:
                    driver.execute_script("arguments[0].click();", j)
                    found = True
                count += 1
        driver.execute_script("arguments[0].click()", driver.find_element_by_name('btnAdd'))

        #-------- Save Result to HTML to analyze
        resultSource = driver.page_source
        with open('result.html', 'w') as f:
            f.write(resultSource)
        result = BeautifulSoup(open('result.html'))

        #-------- Analyze result
        try:
            for tag in result.find_all('namakelas'):
                if tag.text == ' sudah penuh.':
                    driver.execute_script("arguments[0].click()", driver.find_element_by_name('btnKembali'))
            complete = True
            print("Pengambilan Kelas Berhasil")
        except:
            print('Trying . . .')
        #except:
        #    complete = True
        #    print('Done')

# Install Package
def install(package):
    pip.main(['install', package])

# Download Driver
def locateDriver(driverPath):
    url = "https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_win32.zip"
    r = requests.get(url, allow_redirects=True)
    open(driverPath+'\chromedriver.zip', 'wb').write(r.content)
    with zipfile.ZipFile(driverPath+'\chromedriver.zip', 'r') as chromezipped:
        chromezipped.extractall(driverPath)

# Main Process
if __name__ == '__main__':
    driverPath = os.path.expanduser('~\Documents')
    if not os.path.exists(driverPath+'\chromedriver.exe'):
        print("Downloading Chrome Driver from available source...")
        locateDriver(driverPath)
    try:
        from bs4 import BeautifulSoup
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
    except ImportError:
        print("Installing Modules...")
        install('selenium')
        install('beautifulsoap4')
        from bs4 import BeautifulSoup
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
    finally:
        print("\nAll Done. Dependencies Ready.\n")
        mainMenu(driverPath)