

# Mediven Raw Material Stock Card Summary


## Table of Contents
* [General Info](#General-Info)
* [Packages Involved](#Packages-Involved)
* [Setup](#Setup)
* [To-do/add-on features](#To-do/add-on-features)


## General Info

This project is created on self-iniative to provide the summary of raw material available in stock for ease the process of sales person to provide the stock level to the clients. This program will take ```Item Code``` input and will summarize the minimum amount ```(in box)``` that can be produce. Then, this output will be use to automatically update the ```Finished Goods Stock Card``` in the Google sheet. Google Sheet/Microsoft Excel will be act as data entry and client interface. Besides, this project will ease the process of procurement and maintaining the 
ex-stock level.

## Packages Involved

This project depend on:

#### 1. Packages

* Pandas - Ver 1.4.3
* Numpy - Ver 1.23.2

#### 2. Custom Modules/Packages

* ProDetect_class.py


## Setup    

#### For obtaining only the data for single item code or all items at once
1. Install the packages as listed above
2. Run the ```apps.py``` in command prompt or any terminal
3. Insert ```'Item Code'``` as per requested or ```ALL``` to show all items that available in raw stock card.

### For updating the Finished Goods Stock Card google sheet
1. Install the packages as listed above
2. Run ```dict_to_gsheet.py```
3. The program will update the google sheet automatically


## To-do/add-on features

* Modify the output of ```Limiting Factor Component``` to be tailored to the type of Item Code (For examples: PR-DOA-5 components are shared with PR-DOA-4 and PR-DOA-3, thus unrelated to the ```Item Code``` input will be not showed in the output).

    <label for="file">Progress:  </label> ![](https://geps.dev/progress/100)

* Integrated the output of ```ALL``` input into Finished Goods Stock Card in Google sheet.

    <label for="file">Progress:  </label> ![](https://geps.dev/progress/100)

* Differentiate between two type of default PR-DOA-5 (variant of AMP and KET)

    <label for="file">Progress:  </label> ![](https://geps.dev/progress/100)