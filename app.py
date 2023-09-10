import streamlit as st
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import pandas as pd
import numpy as np
from io import StringIO

festival_links=[]
uploaded_file = st.file_uploader("Choose a csv file that has filmfreeway links to film festivals", type={"csv", "txt"})
if uploaded_file is not None:
    # To read file as string:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    #st.write(string_data)
    festival_links= string_data.split("\n")

  
while uploaded_file is None:
    time.sleep(0.5)
#All the festivals we want to add into the spreadsheet
#festival_links=["https://filmfreeway.com/SlamdanceFilmFestival"]
categoryapplicationuniquekey=0
paymentoptionuniquekey=0
ans= "Placeholder"
Column_Headers=['Festival Name', 'Deadline Label', 'Deadline', 'Categories']
RowsToInsert= []
maxNumOfCategoriesChosen=0

#When the user is presented with the possible categories they can apply for, this function ensures that the user keeps getting prompted until an acceptable answer is given so the program does not break
def include_category():
    placeholder = st.empty()
    global categoryapplicationuniquekey

    with placeholder.container().form("category" + str(categoryapplicationuniquekey)):
        #st.write(str(categoryapplicationuniquekey))
        answer = st.radio(
        "Do you wish to apply to this category?",
        [":green[Yes]", ":red[No]"])
        submit_button = st.form_submit_button("Submit Final Answer")

        if submit_button:
            categoryapplicationuniquekey=categoryapplicationuniquekey+1 
            placeholder.empty() 
            if answer==":green[Yes]":
                return True
            else:
                return False
        

def choose_payment(paymentOptionsParam):
    placeholder = st.empty()
    global paymentoptionuniquekey
    with placeholder.container().form("payment" + str(paymentoptionuniquekey)):
        #let user choose multiple choice what they want
        choices=[]
        for index, item in enumerate(paymentOptionsParam):
            choices.append(index+1)
        answer = st.radio(
        "Which option do you choose? ",
        choices, horizontal=True)

        submit_button = st.form_submit_button("Submit Payment Choice")

        if submit_button:
            paymentoptionuniquekey= paymentoptionuniquekey+1
            placeholder.empty()
            return answer
        



        

    

#(1) Asks the user which categories they will submit to
#(2) Asks the user which payment method they would want to explore
def find_all_categories(row_index, col_index):
    global ans
    global maxNumOfCategoriesChosen
    CategoryNames = soup.findAll('span', attrs={'class':'festival-category-name'})
    
    #find description for the festival by finding the div nested 
    # within the profile-categories_content div
    CategoryDescriptions = [div.find('div') for div in soup.findAll('div', attrs={'class':'profile-categories__content'})]
    #loop through each category and see if the user wants to apply to it
    for name, description in zip(CategoryNames, CategoryDescriptions):
        
        st.markdown('<h3> Category: ' + name.text.strip() + '</h3>', unsafe_allow_html=True)
        st.markdown('<h5>' + description.text.strip() + '</h5>', unsafe_allow_html=True)
        ans = include_category()
        #If the user wants to apply to the category, ask for which payment option they want to explore
        while ans==None:
            #as long as there is no answer, execution is delayed by 0.5 seconds
            time.sleep(0.5)
        if ans==True:
            st.info("You are applying to this category")
            chosen_categories.append(name.text)
            #Access <ul class="ProfileDeadlines Small"> to get the payment options
            all_profile_deadlines= description.next.next.next
            #print(all_profile_deadlines.text)
            all_li = all_profile_deadlines.findChildren()
            paymentOptions=[]
            for index, current_li in enumerate(all_li):
                #if the current li is not outdated (aka if the deadline has NOT already passed), then consider it as viable payment option
                if 'is-outdated' not in current_li['class']:
                    #Only consider deadline and payment option
                    if 'CategoryName' in current_li['class'] or 'Fee' in current_li['class']:
                        #If the current element is a deadline label/name
                        if 'CategoryName' in current_li['class']:
                            currentDeadlineName = current_li.text.strip()
                            
                            st.markdown('<h6 style="color:purple"> For submitting your film to the ' + name.text + ' category by the '+ currentDeadlineName + ' deadline, here are the payment options </h6>', unsafe_allow_html=True)
                        #If the current element is a payment option, print it out and after printing it out, ask the user which payment option they want
                        elif 'Fee' in current_li['class']:
                            #st.write("\t\t" + str(len(paymentOptions)+1) + ". "+ current_li.text.replace('\n', ' '))
                            st.markdown("<h6 style='color:purple'>" + str(len(paymentOptions)+1) + ". "+ current_li.text.replace('\n', ' ')+ "</h6>", unsafe_allow_html=True)
                            
                            paymentOptions.append(current_li.text.replace('\n', ' '))
                            #if the next element is a category element, then that means there are no more payment options so you ask user for which payment option they want to go with
                            next = index + 1
                            if next <= len(all_li) :
                                #avoid index out of bounds error at the end
                                if (next==len(all_li) or 'Fee' not in all_li[next]['class']):
                                    user_ans= choose_payment(paymentOptions)
                                    while user_ans==None:
                                        time.sleep(0.5)
                                    if user_ans!=None:
                                        st.info("You chose option " + str(user_ans))
                                    #This way, you only append once per label
                                    if (col_index<=0):
                                        chosen_payment.append([]) 
                                    row_index=row_index+1
                                    chosen_payment[row_index].append(paymentOptions[user_ans-1])
                                    #clear the payment options so you can prepare for the next category's options
                                    paymentOptions=[]
                                    #increment to move onto the next deadline
            #increment to move onto the next category
            col_index=col_index+1; 
            row_index=-1; 
        elif ans==False:
            st.info("You are NOT applying to this category") 
                                        
                
    #st.write()
    #st.write("Here are the categories that you chose:")
    #for x in chosen_categories:
       # print(x) 
    if len(chosen_categories) >= maxNumOfCategoriesChosen:
        maxNumOfCategoriesChosen=len(chosen_categories)
    st.write("\n Here is how info is stored in 2D array")
    st.write(chosen_payment)
    return ans

#get present date so that you can see if a deadline has already passed
present = datetime.now()

#go through each film festival link one at a time
currLinkIdx=0
while currLinkIdx<len(festival_links):
    
    #which categories the film will get submitted to
    chosen_categories= []
    #keep track of how many valid deadlines there are
    valid_deadline_labels=[]
    #For each valid deadline in each category, the user chooses a payment that appeals to them. 
    #Right now, I stored it as 2D Array because that is how it is getting displayed in the spreadsheet, where the rows are deadline labels and the categories are the columns
    chosen_payment = []
    row_idx=-1 #corresponds to valid_deadline_labels
    col_idx=0 #corresponds to chosen_categories
    Placeholder_Rows=[' ', ' ', ' ']
    #Placeholder_Rows=['debug', 'debug', 'debug']


    #save the page you want to scrape as a variable
    page_to_scrape = requests.get(festival_links[currLinkIdx].strip())
    #use beautiful soup to parse the data and save it in the variable soup
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")


    NameOfFestival= soup.find('a', attrs={"data-ga-label":"Festival Name"})
    #st.write("\nThe current festival is " + NameOfFestival.text + "\n")
    st.markdown('<h1 style="color:blue;">' + NameOfFestival.text + '</h1>', unsafe_allow_html=True)


    #Appends the chosen categories to the end of row_lines
    ans=find_all_categories(row_idx, col_idx)
    
    for x in chosen_categories:
        Placeholder_Rows.append(x)
    RowsToInsert.append(Placeholder_Rows)


    #FIND ALL THE ITEMS IN THE PAGE WITH A CLASS ATTRIBUTE OF 'TEXT'
    #AND STORE THE LIST AS A VARIABLE
    Deadlines = soup.findAll('time', attrs={'class':'ProfileFestival-datesDeadlines-time'})


    #FIND ALL THE ITEMS IN THE PAGE WITH A CLASS ATTRIBUTE OF 'AUTHOR'
    #AND STORE THE LIST AS A VARIABLE
    DeadlineLabels = soup.findAll('div', attrs={"class":"ProfileFestival-datesDeadlines-deadline"})


    #LOOP THROUGH BOTH LISTS USING THE 'ZIP' FUNCTION
    #AND PRINT AND FORMAT THE RESULTS
    numOfDeadlinesPrinted=0
    for deadline, deadlinelabel in zip(Deadlines, DeadlineLabels):
        #the event date does not follow strptime properties
        #notification date is unnecessary
        if(deadlinelabel.text.strip() != "Event Date" and deadlinelabel.text.strip() != "Notification Date"):
            #convert the date from text into datetime format
            currentdate= datetime.strptime(deadline.text.strip(), "%B %d, %Y")
            #if the deadline has not already passed then it is added to 
            # the file
            if (currentdate>present):
                #print(deadline.text + " - " + deadlinelabel.text)
                Spreadsheet_Row=[NameOfFestival.text.strip(), deadlinelabel.text.strip(), deadline.text.strip()]

                #insert the chosen budget at the end of each line for each category
                for x in chosen_payment[numOfDeadlinesPrinted]:
                    Spreadsheet_Row.append(x)
                
                RowsToInsert.append(Spreadsheet_Row)
                valid_deadline_labels.append(deadlinelabel.text.strip())
                numOfDeadlinesPrinted=numOfDeadlinesPrinted + 1

    #move onto the next festival link
    currLinkIdx=currLinkIdx+1
    #Insert empty row between new film festivals
    #RowsToInsert.append([' ', ' '])



#the number of columns is Festival Name, Deadline Label, Deadline, and all categories
numOfColumns= 4 + (maxNumOfCategoriesChosen-1)
#st.write("MaxNumberofCategoriesChosen is " + str(maxNumOfCategoriesChosen))
#st.write("number of columns is " + str(numOfColumns))
#make sure that the column headers are accurate
index=len(Column_Headers)
while(index<numOfColumns):
    Column_Headers.append(' ')
    #Column_Headers.append('debug')
    index=index+1
#st.write("These are column headers: ") #debug
#st.write(Column_Headers) #debug

#ensure each row has complete data filled into the columns
i=0
#len(RowsToInsert) is number of rows and len(RowsToInsert[i]) is length of the individual row
while(i<len(RowsToInsert)):
    #grab the current row and see how many elements are in it
    currRowLength = len(RowsToInsert[i])
    while currRowLength < numOfColumns:
        RowsToInsert[i].append(' ')
        #RowsToInsert[i].append('debug')
        currRowLength=currRowLength+1
    st.write("These are the rows: ")
    st.write(RowsToInsert[i]) #debug
    i=i+1


df = pd.DataFrame(np.array(RowsToInsert),
                   columns=Column_Headers)

#st.dataframe(df.style.highlight_max(axis=0))

#function to convert any dataframe to a csv file
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

#converting the sample dataframe
csv = convert_df(df)

#adding a download button to download csv file
st.download_button( 
    label="Download data as CSV. Open it in excel later :)",
    data=csv,
    file_name='Film_Festivals.csv',
    mime='text/csv',
)
