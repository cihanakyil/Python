from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pandas as pd

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(580, 359)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("covidicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 131, 16))
        
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 40, 561, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(440, 110, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 170, 561, 151))
        self.textBrowser.setDocumentTitle("")
        self.textBrowser.setObjectName("textBrowser")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 150, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 580, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showLetter)
        self.pushButton.clicked.connect(self.showAnswer)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "COVID-19 BİLGİ ASİSTANI"))
        self.label.setText(_translate("MainWindow", "Soruyu Giriniz :"))
        self.pushButton.setText(_translate("MainWindow", "CEVABI GÖR"))
        self.label_2.setText(_translate("MainWindow", "Cevabınız :"))

    def showAnswer(self):
        self.timer.stop()
        self.textBrowser.clear()
        self.timer.start(50)
        self.index = 0
        self.user_question = self.textEdit.toPlainText()

    def showLetter(self):
        if self.index < len(self.user_question):
            self.textBrowser.insertPlainText(self.user_question[self.index])
            self.index += 1
        else:
            self.timer.stop()
            self.processAndShowAnswer()

    def processAndShowAnswer(self):
        
        covid_data = pd.read_csv("world_covid-19_data_tr.csv")

        stop_words = set(stopwords.words('turkish'))
        stemmer = PorterStemmer()

        model_cases = make_pipeline(TfidfVectorizer(), MultinomialNB())  
        model_deaths = make_pipeline(TfidfVectorizer(), MultinomialNB())  
        model_recovered = make_pipeline(TfidfVectorizer(), MultinomialNB())  
        model_tests = make_pipeline(TfidfVectorizer(), MultinomialNB())  

        covid_data['processed_questions_cases'] = covid_data['ulke'].apply(
            lambda country: ' '.join([stemmer.stem(word.lower()) for word in word_tokenize(
                f"Covid-19 {country} vaka sayısı {self.user_question}") if word.lower() not in stop_words]))

        covid_data['processed_questions_deaths'] = covid_data['ulke'].apply(
            lambda country: ' '.join([stemmer.stem(word.lower()) for word in word_tokenize(
                f"Covid-19 {country} ölüm sayısı {self.user_question}") if word.lower() not in stop_words]))

        covid_data['processed_questions_recovered'] = covid_data['ulke'].apply(
            lambda country: ' '.join([stemmer.stem(word.lower()) for word in word_tokenize(
                f"Covid-19 {country} iyileşen sayısı {self.user_question}") if word.lower() not in stop_words]))
                
        covid_data['processed_questions_tests'] = covid_data['ulke'].apply(
            lambda country: ' '.join([stemmer.stem(word.lower()) for word in word_tokenize(
                f"Covid-19 {country} test sayısı {self.user_question}") if word.lower() not in stop_words]))

        model_cases.fit(covid_data['processed_questions_cases'], covid_data['toplam_vaka'])
        model_deaths.fit(covid_data['processed_questions_deaths'], covid_data['toplam_olum'])
        model_recovered.fit(covid_data['processed_questions_recovered'], covid_data['toplam_iyilesen'])
        model_tests.fit(covid_data['processed_questions_tests'], covid_data['toplam_test'])

        if 'vaka sayısı' in self.user_question.lower():
            predicted_value = model_cases.predict([f"Covid-19 {self.user_question}"])[0]
            self.textBrowser.append(f"Covid-19 {self.user_question} için cevap:\nVaka sayısı: {predicted_value}\n")

        elif 'ölüm sayısı' in self.user_question.lower():
            predicted_value2 = model_deaths.predict([f"Covid-19 {self.user_question}"])[0]
            self.textBrowser.append(f"Covid-19 {self.user_question} için cevap:\nÖlüm sayısı: {predicted_value2}\n")

        elif 'iyileşen sayısı' in self.user_question.lower():
            predicted_value3 = model_recovered.predict([f"Covid-19 {self.user_question}"])[0]
            self.textBrowser.append(f"Covid-19 {self.user_question} için cevap:\nIyileşen sayısı: {predicted_value3}\n")

        elif 'test sayısı' in self.user_question.lower():
            predicted_value4 = model_tests.predict([f"Covid-19 {self.user_question}"])[0]
            self.textBrowser.append(f"Covid-19 {self.user_question} için cevap:\nTest sayısı: {predicted_value4}\n")

        else:
            self.textBrowser.append("Üzgünüm, sorunuz anlaşılamadı.\n")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
