import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from http.client import HTTPConnection
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import urllib.request
import os

class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.setWindowTitle('WEBCLIENT')
        self.resize(1024, 720)

        self.urllabel = QLabel(self)
        self.urllabel.setText('url: ')
        self.urllabel.move(0, -5)

        self.paramlabel = QLabel(self)
        self.paramlabel.setText('param: ')
        self.paramlabel.move(0, 15)

        self.urlbox = QLineEdit(self)
        self.urlbox.setGeometry(25, 0, 600, 20)

        self.parambox = QLineEdit(self)
        self.parambox.setGeometry(50, 20, 550, 20)

        self.getButton = QPushButton('GET', self)
        self.getButton.setGeometry(600, 0, 40, 20)
        self.getButton.clicked.connect(self.get)

        self.postButton = QPushButton('POST', self)
        self.postButton.setGeometry(600, 20, 40, 20)
        self.postButton.clicked.connect(self.post)

        self.reptext = QLabel(self)
        self.reptext.linkActivated.connect(self.do_get)
        self.reptext.setGeometry(0, 100, 1024, 700)
        self.reptext.setWordWrap(True)
        # self.reptext.setFont(QFont('Arial', 5))

        self.show()

    def get(self):
        self.do_get(self.urlbox.text())

    def post(self):
        self.do_post(self.urlbox.text())

    def get_image(self, link):
        pass

    def request_get(self, link):
        url = urlparse(link)
        conn = HTTPConnection(url.netloc)
        conn.request('GET', url.path, url.params, {
                        'USER-AGENT': '2019027192/HYEONSUKIM/WEBCLIENT/COMPUTERNETWORK'})
        rep = conn.getresponse()
        return rep.read()

    def request_post(self, link, data):
        url = urlparse(link)
        conn = HTTPConnection(url.netloc)
        conn.request('POST', url.path, data, {
                        'USER-AGENT': '2019027192/HYEONSUKIM/WEBCLIENT/COMPUTERNETWORK'})
        rep = conn.getresponse()
        print(rep)
        return rep.read()

    def do_get(self, link):
        print(f'get: {link}')
        try:
            raw = self.request_get(link)
            if '.jpg' in link:
                urllib.request.urlretrieve(link, './temp/image.jpg')
                self.reptext.setText('<img src="./temp/image.jpg">')
                return
            text = raw.decode('utf-8')
            bs = BeautifulSoup(text, 'html.parser')
            lst = bs.select('img')
            i = 0
            for img in lst:
                try:
                    target = urljoin(link, img['src'])
                    print(target)
                    nn = f'./temp/{i}.png'
                    # img['height'] = 50
                    # img['width'] = 50
                    i += 1
                    urllib.request.urlretrieve(target, nn)
                    img['src'] = nn
                except:
                    pass

            for img in lst:
                print(img['src'])
                
            self.reptext.setText(str(bs))
            print(str(bs))
            # self.reptext.adjustSize()

            # if os.path.exists('./temp'):
            #     for file in os.scandir('./temp'):
            #         os.remove(file.path)

        except Exception as e:
            err = QMessageBox()
            err.setText('invalid url or paramater')
            err.setDetailedText(str(e))
            err.exec_()

    def do_post(self, link):
        print(f'post: {link}')
        try:
            text = self.request_post(link, self.parambox.text()).decode('utf-8')
            bs = BeautifulSoup(text, 'html.parser')
            lst = bs.select('img')
            i = 0
            for img in lst:
                try:
                    target = urljoin(link, img['src'])
                    print(target)
                    nn = f'./temp/{i}.png'
                    # img['height'] = 50
                    # img['width'] = 50
                    i += 1
                    urllib.request.urlretrieve(target, nn)
                    img['src'] = nn
                except:
                    pass

            for img in lst:
                print(img['src'])
                
            self.reptext.setText(str(bs))
            print(str(bs))
            # self.reptext.adjustSize()

            # if os.path.exists('./temp'):
            #     for file in os.scandir('./temp'):
            #         os.remove(file.path)

        except Exception as e:
            err = QMessageBox()
            err.setText('invalid url or paramater')
            err.setDetailedText(str(e))
            err.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())
