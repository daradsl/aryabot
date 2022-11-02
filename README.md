# Aryabot Chatbot :wolf: :speech_balloon:


### Preparing the setup: 

- First you need to install Anaconda software
- Then create a new environment with python version 3.8
- So you activate this environment. And then run the command: `pip3 install rasa`
- Now you have a environment with Rasa ready to run the chatbot just missing install the libraries  

***  
### Libraries:

- BeautifulSoup -> `conda install bs4`
- Pandas -> `conda install pandas`
- Selenium -> `conda install selenium`
- Schedule -> `conda install -c conda-forge schedule`
- Unidecode -> `conda install unidecode`  

***
Now you need to clone this project, enter the project folder and follow the next steps

### To build the dataset that will be used by AryaBot
- You need to run: `python scraping.py`
This command will run the webscraping module and create an xlsx file with the dataset

### Some intents use actions to bring up-to-date information 
- To use them you need to start a separate server, using the same environment but with: `run rasa actions` command.

### Running the chatbot server:
- First you need to train your rasa model 
- For that use: rasa train command
- After that you can talk with the chatbot with the command: `rasa shell`  

</br>
</br>
</br>
</br>

### The Complete Flowchart

![Alt text](https://github.com/daradsl/aryabot/blob/master/fluxograma-completo.png?raw=true)
