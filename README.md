# NFTs Name Changer

The NFTs Name Changer is a Python application that allows you to rename multiple folders of NFT images easily. It provides a graphical user interface (GUI) built using the PyQt6 library.

## Prerequisites

- Python 3.x
- PyQt6 library

### Installation

1. Clone the repository or download the source code files.
2. Install the required dependencies by running the following command:

```py
pip install pyqt6
```

1. Run the application using the following command:

python main.py

Alternatively, you can create an executable file (.exe) using pyinstaller:

pip install pyinstaller

pyinstaller main.py --onefile --windowed --add-data "info.json;." --add-data "logo.png;." --icon "icon.png"

This will generate a standalone executable file that users can directly run without installing any dependencies.

### Usage

1. Launch the application by executing the `main.py` file or by running the generated executable (.exe) file.
2. The application window will appear with a "NFTs Name Changer" title and a "Choose Folder" button.
3. Click the "Choose Folder" button to select a single folder for renaming or drag and drop multiple folders into the application window.
4. If you choose a single folder, a message box will appear to ask whether you want to enter individual names for each image. Click "Yes" to enter individual names or "No" to use a common name for all images.
5. If you select "Yes," an input dialog will prompt you to enter a name for each image. Enter the names and press "Enter" to proceed. If you want to cancel the renaming process, click "Cancel" in the input dialog.
6. If you choose "No," an input dialog will prompt you to enter a common name for all images. Enter the name and press "Enter" to proceed. If you want to cancel the renaming process, click "Cancel" in the input dialog.
7. The application will rename the files according to the chosen options.
8. After the renaming process is complete, a message will appear indicating the success of the operation.

### Version

- Version: 0.1

---

Note: The application's functionality and features may be expanded or improved in future versions. For the latest updates and changes, refer to the repository or contact the developer.
