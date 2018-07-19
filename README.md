# Project Structure
## Folder
 1. __companyList:__ contains CSV format files of company names
 2. __json:__ configuration of program
    - actions.json: define search criteria
    - config.json: define directory path for example "download directory" and name of "companyFile" in folder __"companyList"__
    - error.json: record the failure points (auto generated)
 3. __download:__ completed downloads will contain a folder of PDF and a CSV file.   
 4. __temp:__ incompleted / interrupted files. These files are merged after finishing.

## Software Installation:
  1. Install Python >= 3.4:
    - https://www.python.org/getit/, double click to execute the installer
    - Select __"Add Python to PATH"__ then __Install Now__
    - Hit "Next" or "Ok" to finish installation.
  2. Firefox Driver:
    - Download FireFox Browser https://www.mozilla.org/en-US/firefox/new/ then install FireFox.
    - Unzip folder of geckodriver
    - Now we need to add GeckoDriver to PATH of window
    - Press "Window" button and type __Edit the system environment variables__, hit Enter then in tab "Advanced" choose __Environment Variables__
    - Then in System Variables, find __Path__ then Double-click to edit.
    - In window of __Edit environment variable__, press __Browse..__ then choose the path of unzip GeckoDriver.
    - Hit "Enter" to finish procedure.

## How to Run
- __install.bat__ to install needed libraries. If you see "Windows Protected your PC", choose "More info" then "Run anyway"
- Edit __config.json__  to match your directory (you must replace all "\\" with " \\\ ")  
- Edit __actions.json__ to match your search criteria.
- __RUN-testSearch.bat__: Double-click to run this file. Test your search criteria in __actions.json__
- __RUN.bat__: Double-click to run this file. Loop over all files in company names and download files. If download fails, re-run this file to continue the program.

__Note__ If something interrupts the process, hit "Ctrl + C" to terminate the process.

## Issues
- [ ] 7/19: Add function "merging incompleted files"
- [ ] 7/19: Select "NOT" won't work in some cases
