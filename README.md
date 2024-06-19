# Stable Diffusion Style Organizer

## Description
The Stable Diffusion Style Organizer is a PyQt5-based desktop application designed to manage and organize styles for Stable Diffusion prompts. It allows users to load, save, add, edit, and delete styles from a CSV file. The application features a dark theme and customizable font sizes.

<img src='https://drive.google.com/uc?export=view&id=168hykuZRBNIFptv_VlbTg3Ws5zzQkMvT'>

## Features
- Load and save styles from a CSV file
- Add, edit, and delete styles
- Drag and drop to reorder styles
- Customizable font sizes
- Toggle visibility of full prompt information

## Installation

1. Clone the repository or download the source code.
2. Run the `install.bat` file to install the necessary dependencies.

```bat
install.bat
```

## Usage

1. Run the application using the `run.bat` file.

```bat
run.bat
```

2. The main window will display a list of styles. You can:
    - **Load CSV**: Load styles from a CSV file.
    - **Save CSV**: Save the current list of styles to a CSV file.
    - **Add Style**: Add a new style to the list.
    - **Delete Style**: Delete the selected style from the list.
    - **Settings**: Open the settings dialog to customize font size and toggle full prompt information visibility.

## Settings
- **Show Full Prompt Info**: Toggle the visibility of the full prompt information in the list.
- **Font Size**: Adjust the font size used in the application.

Settings are saved in a `settings.json` file and are loaded automatically when the application starts.

## Notes
- The application uses a dark theme for a visually comfortable experience.
- Ensure that the `settings.json` file is in the same directory as the executable for proper loading and saving of settings.

Enjoy using the Stable Diffusion Style Organizer!
