#!/usr/bin/python3
# coding: utf-8



from bs4 import BeautifulSoup
import requests, lxml
import pandas as pd
import os.path
from datetime import date, datetime
import time


def Initiate_BK_DF():
    
    columns = ['Date', 'Review', 'Platform']
    df_BK = pd.DataFrame(columns = columns)
    Save_BK_Data(df_BK)



def Get_BK_Data(pd_df):
    
    pages = range(0, 255, 15)
    i = 0

    for page in pages:

        r = requests.get('https://www.tripadvisor.com/Restaurant_Review-g186338-d804929-Reviews-or' + str(page) + '-Burger_King-London_England.html', headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
        html_data = r.text
        
        soup = BeautifulSoup(html_data, "lxml")

        reviews = soup.find_all(attrs= {"class":"review-container"})
        
        for review in reviews:

            review_entry = review.find(attrs={"class":"entry"}).text

            review_date = review.find(attrs={"class":"ratingDate"})['title']
            review_date = datetime.strptime(review_date, '%B %d, %Y')
            
            row = pd.DataFrame({'Date':[review_date], 'Review':[review_entry], 'Platform':["TripAdvisor"]}, index=[i])
            pd_df = pd.concat([pd_df, row])

            i += 1
    
    return pd_df



def Save_BK_Data(pd_df):
    
    print("Saving data to df_Reviews_BK")
    pd_df.to_pickle('df_Reviews_BK')
    pd_df.to_csv('df_Reviews_BK.csv')
    with pd.ExcelWriter('df_Review_BK.xlsx') as writer:
        pd_df.to_excel(writer)



def Daily_Func():
    if os.path.exists('df_Reviews_BK'):
        #df_BK = Get_BK_Data(pd.read_pickle('df_Reviews_BK'))

        print("Dataframe found. Deleting old Dataframes.")
        try:
            os.remove('df_Reviews_BK')
            os.remove('df_Reviews_BK.csv')
            os.remove('df_Review_BK.xlsx')
            os.rmdir('__pycache__')
        except OSError as error:
            print(error)
        


        time.sleep(5)

        print('creating a new Dataframe')
        Initiate_BK_DF()

        df_BK = Get_BK_Data(pd.read_pickle('df_Reviews_BK'))
        Save_BK_Data(df_BK)


    else:
        print("Dataframe not found. \nCreating a new Dataframe.")
        Initiate_BK_DF()
        Daily_Func()
    
    return 0

# if __name__ == "__main__":
#     Get_BK_Data()
#     print("Done")