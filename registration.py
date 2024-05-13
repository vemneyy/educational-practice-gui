def openSignInWindow(self):
    self.window = QtWidgets.QMainWindow()  # Create a new window instance
    self.ui = Ui_SignInWindow(self.window)  # Pass the current main window to the sign-in window
    self.ui.setupUi(self.window)
    self.window.show()  # Show the new window
    MainWindow.close()  # Close the current main window


def openSignUpWindow(self):
    self.window = QtWidgets.QMainWindow()  # Create a new window instance
    self.ui = Ui_SignUpWindow(self.window)  # Pass the current main window to the sign-in window
    self.ui.setupUi(self.window)
    self.window.show()  # Show the new window
    MainWindow.close()  # Close the current main window

    self.buttonSignIn.clicked.connect(self.openSignInWindow)
    self.buttonSignUp.clicked.connect(self.openSignUpWindow)