# FilmFreeway-Web-Scraper
- Input: A csv file that contains links to filmfreeway festival submissions. The delimiters should be newline characters. Sample inputs are available in the repo under the folder titled "sample-inputs".
- Output: A spreadsheet that contains the name of the festivals, all the deadlines, user-chosen categories to submit to, and price for submitting your film to each category by the deadline. A sample output is also linked in the repo under the folder titled "sample-outputs".

Given a list of links to film festivals, this app web scrapes each link to retrieve important information (ie deadlines and possible categories) and saves that information in a csv file that can be downloaded by the user. The app also presents all the possible categories and descriptions for each film festival and allows the user to choose which categories they would like to submit to and how much they are willing to spend. This was created using python and is hosted on streamlit at https://filmfreeway-spreadsheet.streamlit.app/

Limitations
- This application only works for filmfreeway submission links
- Atleast ONE category must be chosen for each film festival
- The outputted csv/spreadsheet can be difficult to read and needs to be formatted

   

