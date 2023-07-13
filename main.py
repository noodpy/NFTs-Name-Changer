import os
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QInputDialog, QMessageBox, QMainWindow, QMenu, QMenuBar, QDialog, QProgressBar
from PyQt6.QtGui import QIcon, QPixmap, QAction, QColor, QDesktopServices
from PyQt6.QtCore import Qt, QUrl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NFTs Name Changer")

        
        window_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
        self.setWindowIcon(QIcon(window_icon_path))

        self.base_image_path = None

        layout = QVBoxLayout()

        logo_label = QLabel(self)
        logo_image_path = os.path.join(os.path.dirname(__file__), "logo.png")
        logo_label.setPixmap(QPixmap(logo_image_path).scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        title_label = QLabel("NFTs Name Changer")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        self.label = QLabel("Click the button to choose a single folder for renaming or drag and drop multiple folders in this window to rename.")
        layout.addWidget(self.label)

        self.button = QPushButton("Choose Folder")
        self.button.clicked.connect(self.choose_folder)
        layout.addWidget(self.button)
        
        version_label = QLabel("Version: 0.1")
        version_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(version_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = self.menuBar()

        
        self.setStyleSheet("QMenuBar { background-color: #333; color: #fff; }")

        
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.create_action("&Open", self.choose_folder, "Ctrl+O"))

        
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self.create_action("&About", self.show_developer_info, "F1"))

    def create_action(self, text, slot, shortcut=None, icon=None, tooltip=None):
        action = QAction(text, self)
        action.triggered.connect(slot)

        if shortcut is not None:
            action.setShortcut(shortcut)

        if icon is not None:
            action.setIcon(QIcon(icon))

        if tooltip is not None:
            action.setToolTip(tooltip)

        return action

    def show_developer_info(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  
        layout.setSpacing(10)  

        
        info_file_path = os.path.join(os.path.dirname(__file__), "info.json")
        with open(info_file_path) as info_file:
            info_data = json.load(info_file)

        description = info_data["description"]
        description_label = QLabel(description)
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        author_label = QLabel(f"Author: {info_data['author']}")
        layout.addWidget(author_label)

        github_link = info_data["github_link"]
        github_button = QPushButton("GitHub Account")
        github_button.setToolTip("Visit the developer's GitHub account")
        github_button.clicked.connect(lambda: self.open_link_in_browser(github_link))
        layout.addWidget(github_button)

        threads_link = info_data["threads_link"]
        threads_button = QPushButton("Threads Account")
        threads_button.setToolTip("Visit the developer's Threads account")
        threads_button.clicked.connect(lambda: self.open_link_in_browser(threads_link))
        layout.addWidget(threads_button)

        dialog.setLayout(layout)
        dialog.exec()

    def open_link_in_browser(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def choose_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.rename_files(folder_path)

    def rename_files(self, folder_path):
        file_list = os.listdir(folder_path)
        file_list.sort()

        start_number = 1

        
        option = QMessageBox.question(self, "Renaming Option", "Do you want to enter individual names for each image?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if option == QMessageBox.StandardButton.Yes:
            for i, filename in enumerate(file_list):
                _, ext = os.path.splitext(filename)

                
                image_name, ok = QInputDialog.getText(self, "Image Name", f"Enter a name for image {i + 1}:", text=f"Nood #{start_number + i:04d}")

                if ok:
                    new_name = f"{image_name}{ext}"
                    try:
                        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to rename file {filename}: {str(e)}")
                        break
                else:
                    break

        elif option == QMessageBox.StandardButton.No:
            common_name, ok = QInputDialog.getText(self, "Common Name", "Enter a common name for all images:", text="Nood")

            if ok:
                for i, filename in enumerate(file_list):
                    _, ext = os.path.splitext(filename)
                    new_name = f"{common_name} #{start_number + i:04d}{ext}"
                    try:
                        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to rename file {filename}: {str(e)}")
                        break
            else:
                QMessageBox.critical(self, "Error", "Invalid common name entered. Files not renamed.")
                return

        self.label.setText("Files renamed successfully!")

    def update_progress(self, value, total):
        progress = int((value / total) * 100)
        self.progress_bar.setValue(progress)

    def choose_folders(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folders")
        if folder_path:
            self.rename_files(folder_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        folder_paths = [url.toLocalFile() for url in event.mimeData().urls()]
        if folder_paths:
            total_folders = len(folder_paths)
            self.progress_bar = QProgressBar()
            self.statusBar().addWidget(self.progress_bar)
            for i, folder_path in enumerate(folder_paths):
                self.update_progress(i, total_folders)
                self.rename_files(folder_path)
            self.statusBar().removeWidget(self.progress_bar)
            self.progress_bar = None
            self.label.setText("All folders renamed successfully!")

if __name__ == "__main__":
    app = QApplication([])

    app.setStyle("Fusion")

    palette = app.palette()
    palette.setColor(palette.ColorGroup.Normal, palette.ColorRole.Window, QColor("#f0f0f0"))
    palette.setColor(palette.ColorGroup.Normal, palette.ColorRole.WindowText, QColor("#333333"))
    palette.setColor(palette.ColorGroup.Normal, palette.ColorRole.Base, QColor("#ffffff"))
    palette.setColor(palette.ColorGroup.Normal, palette.ColorRole.Button, QColor("#f0f0f0"))
    palette.setColor(palette.ColorGroup.Normal, palette.ColorRole.ButtonText, QColor("#333333"))
    app.setPalette(palette)

    window = MainWindow()
    window.setAcceptDrops(True)
    window.show()
    app.exec()
