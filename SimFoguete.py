import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt

class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulação do Foguete")
        self.setGeometry(100, 100, 300, 400)

        # Configurando o plano de fundo da nova janela
        self.setStyleSheet("background-color: white;")

        # Labels e Entradas para as Condições Iniciais
        self.create_input_fields()

        # Botão para iniciar a simulação
        self.simulate_button = QPushButton("Simular", self)
        self.simulate_button.setStyleSheet("font-size: 16px; background-color: lightgrey; color: black;")
        self.simulate_button.clicked.connect(self.simular_foguete)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Altura Inicial (m):"))
        layout.addWidget(self.entry_altura_inicial)
        layout.addWidget(QLabel("Velocidade Inicial (m/s):"))
        layout.addWidget(self.entry_velocidade_inicial)
        layout.addWidget(QLabel("Massa do Foguete (kg):"))
        layout.addWidget(self.entry_massa_foguete)
        layout.addWidget(QLabel("Tempo Inicial (s):"))
        layout.addWidget(self.entry_tempo_inicial)
        layout.addWidget(QLabel("Tempo Final (s):"))
        layout.addWidget(self.entry_tempo_final)
        layout.addWidget(self.simulate_button)

        self.setLayout(layout)

    def create_input_fields(self):
        self.entry_altura_inicial = QLineEdit(self)
        self.entry_velocidade_inicial = QLineEdit(self)
        self.entry_massa_foguete = QLineEdit(self)
        self.entry_tempo_inicial = QLineEdit(self)
        self.entry_tempo_final = QLineEdit(self)

    def simular_foguete(self):
        try:
            # Lendo as condições iniciais a partir dos inputs
            y0 = float(self.entry_altura_inicial.text())
            v0 = float(self.entry_velocidade_inicial.text())
            m0 = float(self.entry_massa_foguete.text())
            t0 = float(self.entry_tempo_inicial.text())
            tf = float(self.entry_tempo_final.text())

            # Parâmetros Constantes
            b = 1.0  # Fator de Amortecimento
            v_ex = 100.0  # Velocidade de Exaustão (m/s)
            g = -9.81  # Aceleração da Gravidade (m/s^2)
            dm_dt = -0.1  # Taxa de Queima de Combustível (kg/s)

            # Definindo o Sistema de Equações
            def SistemaEDO(t, Y):
                y, v, m = Y
                dydt = v
                dvdt = g + (dm_dt * v_ex / m) - (b / m) * v
                dmdt = dm_dt
                return [dydt, dvdt, dmdt]

            # Inserindo as Condições Iniciais
            Y0 = [y0, v0, m0]

            # Resolver a EDO utilizando solve_ivp
            solution = solve_ivp(SistemaEDO, [t0, tf], Y0, t_eval=np.linspace(t0, tf, 500))

            # Verificar se a solução tem valores para y, v e m
            if solution.success and len(solution.y) > 0:
                t_values = solution.t
                y_values = solution.y[0]
                v_values = solution.y[1]
                m_values = solution.y[2]

                # Plotando os Resultados
                plt.figure(figsize=(12, 6))
                plt.plot(t_values, y_values, label="Posição em y (m)")
                plt.plot(t_values, v_values, label="Velocidade em y (m/s)")
                plt.plot(t_values, m_values, label="Massa (kg)")

                plt.xlabel('Tempo (s)')
                plt.ylabel('Valores')
                plt.legend()
                plt.title('Solução da EDO do Foguete')
                plt.grid(True)
                plt.show()
            else:
                self.show_error("A integração falhou. Verifique os valores iniciais.")
        except ValueError:
            self.show_error("Por favor, insira valores numéricos válidos.")

    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Erro")
        msg.exec_()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rocket Simulator")
        self.setGeometry(100, 100, 400, 300)

        # Configurando o plano de fundo da janela principal
        self.setStyleSheet("background-color: white;")

        # Adicionando um rótulo com GIF
        gif_label = QLabel(self)
        movie = QMovie("base.gif")  # Substitua "base.gif" pelo nome do arquivo GIF
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        gif_label.setScaledContents(True)
        gif_label.setFixedSize(200, 200)  # Tamanho fixo do GIF
        movie.start()  # Inicia a animação do GIF

        # Título com estilo de cor, tamanho de fonte e centralização
        title = QLabel("ROCKET SIMULATOR", self)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        title.setAlignment(Qt.AlignCenter)

        # Botão com centralização no layout
        button = QPushButton("COMEÇAR", self)
        button.setStyleSheet("font-size: 18px; background-color: lightgrey; color: black;")
        button.clicked.connect(self.open_new_window)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(title, alignment=Qt.AlignCenter)  # Título no topo
        layout.addWidget(gif_label, alignment=Qt.AlignCenter)  # GIF embaixo do título
        layout.addWidget(button, alignment=Qt.AlignCenter)  # Centraliza o botão no layout

        self.setLayout(layout)

    def open_new_window(self):
        self.new_window = NewWindow()
        self.new_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
