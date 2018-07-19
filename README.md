# Project Structure
## Folder
 1. __companyList:__ contains CSV format files of company names
 2. __json:__ configuration of program
    - actions.json: define search criteria
    - config.json: define directory path for example "download directory" and name of "companyFile" in folder __"companyList"__
    - error.json: record the failure points (auto generated)
 3. __download:__ completed downloads will contain a folder of PDF and a CSV file.   
 4. __temp:__ incompleted / interrupted files. These files are merged after finishing.

## How to Run
- __RUN-testSearch.bat__: Double-click to run this file. Test your search criteria in __actions.json__
- __RUN.bat__: Double-click to run this file. Loop over all files in company names and download files. If download fails, re-run this file to continue the program.

## Issues
- [ ] 7/19: Add function "merging incompleted files"
- [ ] 7/19: Select "NOT" won't work in some cases
