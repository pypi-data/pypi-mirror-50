## listdir.py
Generates a zip file that contains the CSV file (if there are no specified file), the csv / file includes the following:
1. The parent directory of the file
2. The file name
3. The size of the file
4. The MD5 value of the file
5. The SHA1 value of the file
This includes all the files that exist within a given directory

Basic syntax in command line
> python listdir.py [-h] [-d] [-t] [directory] [file_name]

Added two (2) optional arguments:
```
-d, --date Add the date today in final output file name
-t, --time Add the time today in final output file name
```
```
Both arguments are optional. There are default values for Directory and File Name and you can change it in the config.ini
```

```
Note:
  - You can prove any name for the csv file without adding the .csv extension
  - Remove any succeeding backslash from the end of the directory to avoid any errors
```