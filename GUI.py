from threading import *
from PyQt5 import QtWidgets, uic
import sys, os, random
import presensi, Data
from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem

import json

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('presensi.ui', self)

        self.presensi = presensi.presensi()
        self.data = Data.data()
        self.dataui_NIM = []
        self.dataui_Password = []
        self.is_new_preset = True
        self.show()
        self.loadkeui()
        self.pushButton_Presensi.clicked.connect(self.thread_presensi)
        self.pushButton_Tambah.clicked.connect(self.tambahrow)
        self.pushButton_Hapus.clicked.connect(self.hapusrow)
        self.check_preset()
        self.pushButton_LoadPreset.clicked.connect(self.load_preset)
        self.pushButton_NewPreset.clicked.connect(self.new_preset)
        self.pushButton_Simpan.clicked.connect(self.simpan_json)

    def simpan_json(self):
        if self.is_new_preset == True:
            file_name = "data" + str(random.randint(1,1000)) + ".json"
        else:
            file_name = self.comboBox_Preset.currentText()
        data_json = {}
        for row in range(self.Tabel_Mahasiswa.rowCount()):
            nim =self.Tabel_Mahasiswa.item(row,0).text()
            password = self.Tabel_Mahasiswa.item(row,1).text()
            data_json[row] = {"nim":nim, "password": password}
        self.data.simpanJson(file_name, data_json)
        self.Label_Presensi_2.setText(f"Daftar Mahasiswa: {file_name}")
        self.check_preset()

    def new_preset(self):
        self.Tabel_Mahasiswa.setRowCount(0)
        self.Label_Presensi_2.setText("Daftar Mahasiswa: New Preset")
        self.is_new_preset = True

    def load_preset(self):
        preset = self.comboBox_Preset.currentText()
        self.new_preset()
        self.Label_Presensi_2.setText(f"Daftar Mahasiswa: {preset}")
        user_data = self.data.getData(preset)
        self.Tabel_Mahasiswa.setRowCount(len(user_data.keys()))
        for index in user_data:
            self.Tabel_Mahasiswa.setItem(int(index), 0, QTableWidgetItem(user_data[index]["nim"]))
            self.Tabel_Mahasiswa.setItem(int(index), 1, QTableWidgetItem(user_data[index]["password"]))
        self.is_new_preset = False

    def check_preset(self):
        # list_file = os.listdir(self.PATH_PRESET)
        self.comboBox_Preset.clear()
        list_file = self.data.listPreset()
        if len(list_file) > 0:
            self.comboBox_Preset.addItems(list_file)

    def loadkeui(self):
        return
        # email = self.presensi.email()
        # password = self.presensi.password()
        # total = len(email)
        # print("data masuk ke UI: ", total)
        # self.Tabel_Mahasiswa.setRowCount(total)
        # for i in range(total):
        #     self.Tabel_Mahasiswa.setItem(i, 0, QTableWidgetItem(str(email[i])))
        #     self.Tabel_Mahasiswa.setItem(i, 1, QTableWidgetItem(str(password[i])))

    def loadkeprogram(self):
        row = self.Tabel_Mahasiswa.rowCount()
        print("data masuk ke Program: ", row)
        for i in range(row):
            self.dataui_NIM.insert(i, self.Tabel_Mahasiswa.item(i, 0).text())
            self.dataui_Password.insert(i, self.Tabel_Mahasiswa.item(i, 1).text())

    def ambil_link_presensi(self):
        link = self.Text_Edit_Presensi.toPlainText()
        return link

    def presensi_data(self):
        self.loadkeprogram()
        # link uty
        uty = "https://sia.uty.ac.id/"
        uty_absen = "https://sia.uty.ac.id/std/scanabsen"
        absensi_kode = self.ambil_link_presensi()
        uty_keluar = "https://sia.uty.ac.id/home/keluar"
        for i in range(len(self.dataui_NIM)):
            NIM_saat_ini = self.dataui_NIM[i]
            password_saat_ini = self.dataui_Password[i]
            self.presensi.login(uty, "loginNipNim", NIM_saat_ini, "loginPsw", password_saat_ini, "BtnLogin")
            berhasil_login = QListWidgetItem(str("Berhasil login: " + str(NIM_saat_ini)))
            self.listWidget_Progres.addItem(berhasil_login)
            print("login")

            self.presensi.ambilnama()
            nama = QListWidgetItem(str("Nama: " + str(self.presensi.nama)))
            self.listWidget_Progres.addItem(nama)
            print("nama")

            self.presensi.absensi(uty_absen, "inputcode", absensi_kode)
            berhasil_presensi = QListWidgetItem(str("Berhasil presensi: " + str(NIM_saat_ini)))
            self.listWidget_Progres.addItem(berhasil_presensi)
            print("presensi")

            self.presensi.alerta()
            alert_box = QListWidgetItem(str(self.presensi.aa))
            self.listWidget_Progres.addItem(alert_box)
            print("alerta")

            self.presensi.keluar(uty_keluar)
            keluar = QListWidgetItem("Keluar")
            self.listWidget_Progres.addItem(keluar)
            print("keluar")

            w = QListWidgetItem("-----------------")
            self.listWidget_Progres.addItem(w)
        selesai = QListWidgetItem("Program Selesai")
        self.listWidget_Progres.addItem(selesai)
        print("selesai")

        self.dataui_NIM.clear()
        self.dataui_Password.clear()


    def thread_presensi(self):
        t1 = Thread(target=self.presensi_data)
        t1.start()

    def tambahrow(self):
        row = self.Tabel_Mahasiswa.rowCount()
        self.Tabel_Mahasiswa.insertRow(row)

    def hapusrow(self):
        indices = self.Tabel_Mahasiswa.selectionModel().selectedRows()
        for each_row in reversed(sorted(indices)):
            self.Tabel_Mahasiswa.removeRow(each_row.row())
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
