# Sentiment Analysis Using Flask

This is a sentiment analysis project created using Flask.

This application has been created to simulate the understanding of sentiment across various medias such as text, url, audio or video.

<small>**Note**: Initially planning to complete text and url and then focus on other media types in the future.</small>

## Pseudocode

## Installation

1. **Clone the code from this repository:**

   ```
   https://github.com/edwinrlambert/Sentiment-Analysis-Using-Flask.git
   ```

2. **Create a virtual environment using the `virtualenv` command.**

   Virtual environments are created so that the libraries that are installed and used for this project won't impact any other libraries installed for other projects. This creates an encapsulation for the project, so that anything installed for this project can only be used for this project.

   Do the following in the terminal.

   **Installing virtualenv (this can be done globally)**

   ```py
   pip install virtualenv
   ```

   **Creating a virtual environment**

   ```py
   virtualenv project-name-env
   ```

   where `project-name-env` can be any name that you want to give. Example: `virtualenv sentiment-analysis-env`

   <small>Having **-env** at the end is not mandatory, that it gives an indication that helps us understand that this is a virtual environment directory.</small>

   **Activate the virtual environment to start using it.**

   ```
   project-name-env/Scripts/activate
   ```

3. **Install the necessary libraries of the project.**

    Use the **requirements.txt** file to install all the dependencies/libraries used in this project. 

    Since we're installing this in a virtual environment, all the libraries will be installed within this environment.

    To install packages from a **requirements.txt** file, you would use:

    ```py
    pip install -r requirements.txt
    ```

    This will install all of the packages listed in the requirements.txt file.

4. **Running the project**

    A flask project can be run using the following command:

    ```
    python app.py
    ```

    This will start the Flask development server. You should see output similar to this:

    ```
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```

    This means your Flask app is running on your local machine (localhost) on port 5000. You can access it by opening a web browser and navigating to http://127.0.0.1:5000.