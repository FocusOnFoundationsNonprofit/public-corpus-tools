# Public Corpus Tools
by Focus on Foundations, a 501(c)3 nonprofit
Founder: Randy True

## Description

Tools to interact with a corpus, such as loading it to a vector database and interacting with it via Q&A and chat.

## Installation

1. Clone the Repository: Start by cloning this repository to your local machine. You can do this using the following command in your terminal or command prompt:

   ```
   git clone https://github.com/FocusOnFoundationsNonprofit/public-corpus-tools.git
   ```

2. Install Python and Pip: Make sure you have Python and pip (Python package installer) installed on your system. You can download Python from the official website (https://www.python.org/) and pip is usually included in Python 3.4 and later versions.

3. Create a Virtual Environment (Optional but Recommended): It's a good practice to create a virtual environment to isolate this project's dependencies. Navigate to the project's root directory and run the following commands to create a virtual environment named ".venv":

   ```
   pip install virtualenv
   virtualenv .venv
   source .venv/bin/activate
   ```

4. Install Dependencies: While in the project's root directory and with the virtual environment activated (if you created one), you should now install the package itself along with its dependencies using the setup.py configuration. Run the following command:

   ```
   pip install -e .
   ```

   \*\* Note: The previous method of installing dependencies directly from the requirements.txt file using `pip install -r requirements.txt` is considered deprecated but can still be used if necessary.\_

   The command pip install -e . is used to install a Python package in "editable" mode from the current directory (denoted by .). Here's what happens when you run this command:

   1. Editable Mode: The -e flag stands for "editable". This mode means that the package is installed in a way that allows you to edit the source code directly without having to reinstall the package every time you make changes. It's particularly useful for development purposes.

   2. Current Directory: The . refers to the current directory. This assumes that there is a setup.py file in the current directory which contains the package information needed for the installation.


