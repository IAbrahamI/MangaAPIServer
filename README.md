MangaAPI Server setup

Setting Up a Python Virtual Environment and Installing Dependencies
Introduction

This README provides instructions on how to create a virtual environment using Python 3 and install required dependencies from a requirements.txt file.
Prerequisites

Ensure the following are installed on your system:

    Python 3: Download from Python's official website if not installed.
    pip: Typically included with Python 3 installations.

Steps to Set Up a Virtual Environment and Install Dependencies
1. Navigate to Your Project Directory

Open a terminal or command prompt and navigate to the directory where your project is located:

cd /path/to/your/project

2. Create a Virtual Environment

Run the following command to create a virtual environment:

python3 -m venv venv

Here:

    venv is the name of the virtual environment folder. You can replace it with any name you prefer.

3. Activate the Virtual Environment

    On Linux/MacOS:

source venv/bin/activate

On Windows:

    .\venv\Scripts\activate

Once activated, you should see the environment name (e.g., (venv)) in your terminal prompt.
4. Install Dependencies

With the virtual environment active, run the following command to install the required dependencies from the requirements.txt file:

pip install -r requirements.txt

5. Deactivate the Virtual Environment (Optional)

When you're done working in the virtual environment, deactivate it using:

deactivate

Additional Notes

    Upgrading pip: It’s a good idea to ensure pip is up to date before installing dependencies:

pip install --upgrade pip

Checking Installed Packages: To verify the installed packages in the environment:

pip list

Re-activating the Virtual Environment: If you close the terminal or deactivate the environment, simply re-activate it as shown in step 3.