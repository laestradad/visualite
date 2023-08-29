# Visualite

## Setting Up a Virtual Environment

A virtual environment helps isolate project-specific dependencies. Follow these steps to set up a virtual environment:

1. Open a terminal or command prompt.
1. Navigate to your project directory:
   ```sh
   cd path/to/your/project
   ```
1. Create a virtual environment named 'venv':
   ```sh
   python -m venv venv
   ```
1. Activate the virtual environment:
   ```sh
   .\venv\Scripts\activate
   ```

## Installing Project Dependencies
Project dependencies are listed in the requirements.txt file. To install them, follow these steps:

1. Ensure your virtual environment is activated.
1. Install the dependencies using pip:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Project
With the virtual environment activated and dependencies installed, you can now run the project. For example:
   ```sh
   python main.py
   ```

## Deactivating the Virtual Environment
When you're done working on your project, deactivate the virtual environment to return to your system's default Python environment:
   ```sh
   deactivate
   ```