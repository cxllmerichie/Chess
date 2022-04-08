"""import os
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 800, 120
        self.setMinimumSize(self.window_width, self.window_height)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        btn = QPushButton('Play', clicked=self.playAudioFile)
        self.layout.addWidget(btn)

        volumeControl = QHBoxLayout()
        self.layout.addLayout(volumeControl)

        btnVolumeUp = QPushButton('+', clicked=self.volumeUp)
        btnVolumeDown = QPushButton('-', clicked=self.volumeDown)
        butVolumeMute = QPushButton('Mute', clicked=self.volumeMute)
        volumeControl.addWidget(btnVolumeUp)
        volumeControl.addWidget(butVolumeMute)
        volumeControl.addWidget(btnVolumeDown)

        self.player = QMediaPlayer()

    def volumeUp(self):
        currentVolume = self.player.volume()  #
        print(currentVolume)
        self.player.setVolume(currentVolume + 5)

    def volumeDown(self):
        currentVolume = self.player.volume()  #
        print(currentVolume)
        self.player.setVolume(currentVolume - 5)

    def volumeMute(self):
        self.player.setMuted(not self.player.isMuted())

    def playAudioFile(self):
        full_file_path = os.path.join(os.getcwd(), 'test.mp3')
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)

        self.player.setMedia(content)
        self.player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')"""