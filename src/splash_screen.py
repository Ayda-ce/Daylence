import os   
from utils import read_settings
from PyQt5.QtCore import Qt, QUrl  
from main_window import MainWindow
from styles import color_palette, font_families
from PyQt5.QtGui import QPalette, QColor, QPixmap  
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent  
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QSplashScreen, QDesktopWidget  

class SplashScreen(QSplashScreen):
	def __init__(self):
		super().__init__()

		# Initialization
		self.dir_path = os.path.dirname(os.path.realpath(__file__))
		self.settings = read_settings(self.dir_path + "\\Files\\settings.dat")
		self.theme = color_palette(self.settings['Theme'])
		self.font_families = font_families(self.settings['Font'])
		self.number_format = self.settings['Number_Format']

		# Splash image
		current_theme = self.settings['Theme']
		splash_image_name = f"splash_{current_theme}.png"
		splash_image_path = (self.dir_path + "\\Files\\" + splash_image_name)  

	    # Fallback image
		if not os.path.exists(splash_image_path):
			splash_image_path = os.path.join(self.dir_path, "Files", "splash_default.png")

        # Window setup
		self.width = 350
		self.height = 350
		self.setWindowFlags(Qt.FramelessWindowHint) # No window border
		self.setGeometry(0, 0, self.width, self.height)
		self.center()

        # Styling
		palette = QPalette()
		palette.setColor(QPalette.Background, QColor(self.theme['Splash']))
		self.setPalette(palette)
		self.setStyleSheet("border-radius: 12px")

        # Layout
		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignCenter)

        # Image label
		image_label = QLabel(self)
		pixmap = QPixmap(splash_image_path)
		if pixmap.isNull():
			pixmap = QPixmap(os.path.join(self.dir_path, "Files", "splash_default.png"))

        # Image scaling
		image_size = 350
		pixmap = pixmap.scaled(image_size, image_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)


		image_label.setPixmap(pixmap)
		image_label.setAlignment(Qt.AlignCenter)

        # Welcome text
		welcome_label = QLabel("Welcome ...", self)
		welcome_label.setStyleSheet(f"color: {self.theme['Text']}; font-size: 23px; font-weight: bold;")
		welcome_label.setAlignment(Qt.AlignCenter)

		layout.addWidget(image_label, alignment=Qt.AlignCenter)
		layout.addWidget(welcome_label, alignment=Qt.AlignCenter)

        # Background music
		self.setLayout(layout)
		self.player = QMediaPlayer()
		media_path = os.path.join(self.dir_path, "Files", "Song.mp3")
		self.player.setMedia(QMediaContent(QUrl.fromLocalFile(media_path)))
		self.end_position = 9*1000
		self.start_position = 5*1000
		self.player.setPosition(self.start_position)
		self.player.setVolume(3)
		self.player.play()
		self.player.positionChanged.connect(self.music_finished)
		self.player.mediaStatusChanged.connect(self.music_finished)


    # Music handler
	def music_finished(self, status):
		if self.player.position() >= self.end_position:
			self.player.stop()
			self.close()
			self.open_main_window()
	
	
	# Open main window
	def open_main_window(self):
		self.main_window = MainWindow()
		self.main_window.show()


	# Screen centering
	def center(self):
		screen_geometry = QDesktopWidget().screenGeometry()
		x = (screen_geometry.width() - self.width) // 2
		y = (screen_geometry.height() - self.height) // 2
		self.move(x, y)


	# Event ignore
	def mousePressEvent(self, event):  
		event.ignore()