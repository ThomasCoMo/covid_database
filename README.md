# covid_database

store covid data from europeen database and plot cases and deaths per country

## Preriquisites
* mysql
* python

## How-to

1. lauch mysql and run **createTable.sql**:
```bash
source createTable.sql;
```
2. then close mysql and run **first_init.py**, it will insert data for the first time in the database
```bash
python first_init.py
```
3. you can now have to data using **UI.py**:
```bash
python UI.py
```
4. this windows will open:

![1](https://user-images.githubusercontent.com/74672067/131140098-01961a19-090a-4b85-a319-5ff7cf073f7c.png)<br>
5. then select country and press button *select country and plot*, the windows is uptdated :
![2](https://user-images.githubusercontent.com/74672067/131140185-82110328-9700-4a2e-b17e-ae138b93e46a.png)<br>
6. you can select another country and press the same button it will update graphic.


## Update
to update data in database:
```bash
python update_data.py
```
