# FilmFreeway-Web-Scraper
- Input: A csv file that contains links to filmfreeway festival submissions. The delimiters should be newline characters. Sample inputs are available in the repo under the folder titled "sample-inputs".
- Output: A spreadsheet that contains the name of the festivals, all the deadlines, user-chosen categories to submit to, and price for submitting your film to each category by the deadline. A sample output is also linked in the repo under the folder titled "sample-outputs".

Given a list of links to film festivals, this app web scrapes each link to retrieve important information (ie deadlines and possible categories) and saves that information in a csv file that can be downloaded by the user. The app also presents all the possible categories and descriptions for each film festival and allows the user to choose which categories they would like to submit to and how much they are willing to spend. This was created using python and is hosted on streamlit at https://filmfreeway-spreadsheet.streamlit.app/

## Version 1 
### Limitations
- This application only works for filmfreeway submission links
- Atleast ONE category must be chosen for each film festival
- The outputted csv/spreadsheet can be difficult to read and needs to be formatted

## Version 2 (Current Version) 
### Updates :)
- You can now add a single link without needing to insert a csv file with multiple links  
- You do NOT need to submit to at least one category per film festival. If needed, you can select no categories for a film festival and program will not break
- Film Festival event dates and submission links are on the spreadsheet/csv file
- Downloaded data is formatted as xlxs as well, so the final resulting spreadsheet is more aesthetically pleasing
### Limitations :(
- Does not work for Sundance Film Festival because the deadlines do not apply for ALL the categories
- If you are uploading multiple links via csv, the delimiter between unique links MUST be a newline character, and the only contents of the csv can be the links and the new line delimiters between them. Otherwise, the website cannot read it. 
- Submission Format, WP, and location need to be manually added to the final data spreadsheet 
- The website still needs to be tested with other filmfreeway links

##Version 3
### Updates :)
- Rather than keeping all the text from previous categories, this new version deletes it and only keeps 2 lines that indicates whether or not you are applying to the category and which payment options you chose (if you are applying). This was achieved using st.empty() containers. This is also supposed to speed up the website when you are entering a lot of links

### Limitations :(
- Still need to test it out on festivals like Cannes 

##Version 4 (Current Version)
### Updates :)
- Cache-ing the request url and soup method to avoid too much storage at every re-run
- Rather than storing all the categories and descriptions in an array and traversing it, I created variables and am parsing by reassigning the variable to the next category/description
- Replaced the radio choices with buttons to avoid (1) storing too many session states (2) reruns
- I removed messages for “You are applying to x category” and “You are not applying to x category” to improve speed for festivals like Cannes
- Cannes no longer crashes even if you say yes to every category!
- If the user submits multiple filmfreeway links, rather than only allowing the user to download one big excel file at the end, I am asking them to download an excel file after each film festival so that not all progress is lost if the app crashes unexpectedly
- Rather than using xlsx writer, I am using openpyxl to create and download the word document because openpyxl allowed you to write to an existing excel file instead of creating my own

### Limitations :(
- Does not work for Sundance or Brooklyn because not all the deadlines apply to each category, so the program breaks
- Does not work for Cork or Montclair Film Festival because the website has not been updated, and last year's dates are still on the site. Since the website ignores past deadlines, the program will not pull any information from it
- It still needs to be tested some more to see how much data is getting used by streamlit, since we have a limit of 1 GB

### Future Work!
- Curently, the information is getting stored in a excel file that the user downloads on their device. In the future, I could store the information in a database so it is available for the user at any time (even if the excel file gets lost) and is synced between different users

   

