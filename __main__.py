import sys
from PyQt5.QtWidgets import QApplication
from src.vista.InterfazEPorra import App_EPorra
from src.logica.Logica import Logica

if __name__ == '__main__':
    # Punto inicial de la aplicación

    logica = Logica()

    app = App_EPorra(sys.argv, logica)
    sys.exit(app.exec_())