import cv2
import numpy as np
import sys
from PyQt5 import QtWidgets, QtCore

class ShowVideo(QtCore.QObject):

    #initiating the built in camera
    #camera_port = 0
    #camera = cv2.VideoCapture(camera_port)
    cv2.VideoCapture('/home/mka/Downloads/test.mp4')
    videoSignal = QtCore.pyqtSignal(QtWidgets.QImage)

    def __init__(self, parent = None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        run_video = True

        while run_video:
            ret, image = self.camera.read()

            # OpenCV stores data in Blue-Green-Red format. 
            # Qt stores data in Red-Green-Blue format. The cmd swaps to
            # the right format
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Need to make a QImage.
            qt_image = QtWidgets.QImage(color_swapped_image.data, 
                                    color_swapped_image.cols, 
                                    color_swapped_image.rows,
                                    color_swapped_image.step,
                                    QtWidgets.QImage.Format_RGB888)

            self.videoSignal.emit(qt_image)


class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtWidgets.QImage()

    def paintEvent(self, _):
        painter = QtWidgets.QPainter(self)
        painter.drawImage(0,0, self.image)
        self.paintImage = QtWidgets.QImage()

    def initUI(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Test')
        self.show(image)

    @QtCore.pyqtSlot(QtWidgets.QImage)
    def setImage(self, image):
        self.image = image
        self.paintEvent()

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    # let's make instances of our two custom classes that we created
    image_viewer = ImageViewer()
    vid = ShowVideo()

    # Now let's connect the signal/slots of the two instances of
    # our custom classes together
    vid.videoSignal.connect(image_viewer.setImage)

    # I'm adding a button for ease to start the actual video capture
    # You could also use timers to start it automatically?
    push_button = QtWidgets.QPushButton("Start")

    # need to connect the button to our `startVideo` command
    push_button.clicked.connect(vid.startVideo)

    # Ok, so we made a button, but how do we get it to pop up?
    # Use a layout
    vertical_layout = QtWidgets.QVBoxLayout()

    # need to add the two widgets that we want, ImageViewer 
    # and QPushButton to the layout that we just made
    vertical_layout.addWidget(image_viewer)
    vertical_layout.addWidget(push_button)

    # Qt is a little odd in the fact that we need a widget
    # to set the layout to. Can't just set the QMainWindow 
    # layout directly. So I create a "LayoutWidget" 
    # here and set the layout to the layout we just made
    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    # Now let's create our main window, and set the central widget to 
    # the layout WIDGET that we just created
    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)

    # make sure to call the show method on QMainWindow if you want to 
    # see anything
    main_window.show()

    # and this is the magic sauce that adds in a loop
    sys.exit(app.exec_())
    
