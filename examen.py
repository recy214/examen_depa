import serial as placa
import sys
from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile = "focos_examen.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        self.arduino = None
        self.focos_encendidos = False

        self.segundoPlano = QtCore.QTimer(self)
        self.segundoPlano.timeout.connect(self.lecturas)

        self.btn_conectar.setText("Conectar")
        self.btn_capturar_luz.setText("Capturar Datos")
        self.btn_focos.setText("Encender Focos")
        self.btn_conectar.clicked.connect(self.accion)
        self.btn_capturar_luz.clicked.connect(self.toggle_captura)
        self.btn_focos.clicked.connect(self.control_focos)
        self.btn_regresar.clicked.connect(self.close)

    def lecturas(self):
        if self.arduino and self.arduino.isOpen():
            if self.arduino.inWaiting():
                try:
                    lectura = self.arduino.readline().decode().strip()
                    if lectura and lectura.startswith("L,"):
                        partes = lectura.split(",", 1)
                        if len(partes) == 2:
                             _, val = partes
                             self.listLuminosidad.addItem(val)
                             self.listLuminosidad.setCurrentRow(
                                 self.listLuminosidad.count() - 1)
                except Exception as e:
                    print(f"Error durante la lectura o procesamiento serial: {e}")
                    QtWidgets.QMessageBox.warning(self, "Error de Lectura Serial", f"Fallo al Leer del Arduino:\n{e}")

    def accion(self):
        texto = self.btn_conectar.text().upper()
        if texto == "CONECTAR":
            puerto = f"COM{self.com.text().strip()}"
            try:
                self.arduino = placa.Serial(puerto, baudrate=9600, timeout=1)
                self.btn_conectar.setText("DESCONECTAR")
                self.txt_estado.setText("CONECTADO")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"No se Pudo Conectar al Arduino:\n{e}")
                self.arduino = None
                self.txt_estado.setText("DESCONECTADO")

        else:
            if self.segundoPlano.isActive():
                self.segundoPlano.stop()
                self.btn_capturar_luz.setText("Continuar Captura")
            if self.arduino and self.arduino.isOpen():
                try:
                    self.arduino.close()
                except Exception as e:
                     print(f"Error al cerrar serial al desconectar: {e}")
            self.arduino = None
            self.btn_conectar.setText("CONECTAR")
            self.txt_estado.setText("DESCONECTADO")

    def toggle_captura(self):
        if not self.arduino or not self.arduino.isOpen():
            QtWidgets.QMessageBox.warning(self, "Error", "No Estás Conectado al Arduino.")
            return
        if not self.segundoPlano.isActive():
            self.segundoPlano.start(100)
            self.btn_capturar_luz.setText("Detener Datos")
        else:
            self.segundoPlano.stop()
            self.btn_capturar_luz.setText("Continuar Captura")

    def control_focos(self):
        if not (self.arduino and self.arduino.isOpen()):
            QtWidgets.QMessageBox.warning(self, "Error", "No Estás Conectado al Arduino.")
            return
        try:
            if not self.focos_encendidos:
                self.arduino.write(b"1")
                self.btn_focos.setText("Apagar Focos")
                self.focos_encendidos = True
            else:
                self.arduino.write(b"0")
                self.btn_focos.setText("Encender Focos")
                self.focos_encendidos = False
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"No se Pudo Enviar el Comando: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MyApp()
    main_window.show()
    sys.exit(app.exec_())
