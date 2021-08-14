"""
Please see readme to get a full project description, files used and references
"""
import time
#project has been accepted
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#Show all columns
pd.set_option('display.max_columns', None)
 #Show all lines
pd.set_option('display.max_rows', None)
 # value display length
pd.set_option('max_colwidth',50)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    y="no"
    while y=="no":
        print('Hello! Let\'s explore some US bikeshare data!')
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        dict_city_names={'chi':'chicago','was':'washington','new':'new york city'}
        check=0
        while check==0:
            city=input("Please enter the city that you are interested in looking at? (Chicago, Washington or New york City)"
                    "\n(You can type the whole city name or just the first 3 letters - Example: chi = Chicago)\n>>")
            city=city.strip().replace(' ','_').lower()
            if len(city)==3:
                if city not in dict_city_names:
                    print("The city you entered seems wrong! Please try again or restart the program!")
                else:
                    city=dict_city_names[city]
                    check=1

            elif city in dict_city_names.values():
             check=1
            else:
                print("The city you entered seems wrong! Please try again or restart the program!")
        # get user input for month (all, january, february, ... , june)
        # create a dictionary here to map shorcuts for month names
        dict_month_names = {'jan': 'january', 'feb': 'february', 'mar': 'march','may': 'may','jun': 'june','all':'all'}
        check = 0
        while check == 0:
            month1 = input("Please enter the month you want to analyze! -- OR -- Enter \"all\" for no month filter!\n"
                      "(You can type the whole month name or just the first 3 letters - Example: Jan = January)\n>>")
            month1 = month1.strip().replace(' ', '_').lower()
            if len(month1)==3:
                if month1 not in dict_month_names:
                    print("The month you entered seems wrong! Please try again or restart the program!")
                else:
                    month1=dict_month_names[month1]
                    check=1
            elif month1 in dict_month_names.values():
                check = 1
            else:
                print("The month you entered seems wrong! Please try again or restart the program!")
        #if month1 != 'all':
            # use the index of the months list to get the corresponding int
            #months = list(dict_month_names.values())
            #month = months.index(month1)+1
        # get user input for day of week (all, monday, tuesday, ... sunday)
        # create a dictionary here to map shorcuts for day names
        dict_day_names = {'mon':'monday','tue':'tuesday','wed':'wednesday','thu':'thursday','fri':'friday','sat':'saturday','sun':'sunday','all':'all'}
        check=0
        while check == 0:
            day1 = input("Please enter the day you want to analyze! -- OR -- Enter \"all\" for no day filter!\n"
                         "(You can type the whole day name or just the first 3 letters - Example: Mon = Monday)\n>>")
            day1 = day1.strip().replace(' ', '_').lower()
            if len(day1)==3:
                if day1 not in dict_day_names:
                    print("The day you entered seems wrong! Please try again or restart the program!")
                else:
                    day1=dict_day_names[day1]
                    check=1
            elif day1 in dict_day_names.values():
             check=1
            else:
             print("The day you entered seems wrong! Please try again or restart the program!")
        #if day1 != 'all':
            #days=list(dict_day_names.values())
            #day = days.index(day1) + 1

        print("You have chosen the:\nCity of "+str(city.title())+'\nthe month of: '+str(month1.title())+'\nand day: '+str(day1.title())+'\n')
        y=input("Is this correct? Type \"yes\" or \"no\" on the next line(\"no\" will restart the program)\n>> ")
        y=y.strip().replace(' ', '_').lower()
    print('-'*60)
    if month1!='all':
        month=month1.title()
    else:
        month=month1
    if day1!='all':
        day=day1.title()
    else:
        day=day1
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name() # 1 is monday
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df.loc[df['month']==month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week']==day]


    i=0
    j=5
    response = input(
        "Do you want to see 5 lines of raw data for the filters you have specified?\nEnter \"yes\" or \"no\" to continue into the analysis!\n>> ")
    response = response.strip().replace(' ', '_').lower()
    while response == 'yes':

        print(df.iloc[i:j,:])
        i+=5
        j+=5
        response = input(
            "Do you want to see 5 lines of raw data for the filters you have specified?\nEnter \"yes\" or \"no\" to continue into the analysis!\n>> ")
        response = response.strip().replace(' ', '_').lower()



    return df,city,month,day

def time_stats(df,city,month,day):
    """Displays statistics on the most frequent times of travel."""
    if month!='all'and day!='all':
        print('\nCalculating The Most Frequent Times of Travel for the City of {}, for the month of {} and for {}s...\n'.format(city.title(),month,day))
        start_time = time.time()
        # display the most common start hour
        most_common_start_hour = df.mode()['hour'][0]
        count_most_common_hour = (df.groupby(['hour'])['Start Time'].count()).max()
        print("The most common hour of the day is the {}th hour, the Count was: {}".format(int(most_common_start_hour),count_most_common_hour))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('--' * 60)

    elif month=='all':
        print('\nCalculating The Most Frequent Times of Travel for the City of {}, for {} months and for {}s...\n'.format(city.title(), month, day))
        start_time = time.time()
        most_common_month = df.mode()['month'][0]
        count_most_common_month = (df.groupby(['month'])['Start Time'].count()).max()
        # na_start_time=df["Start Time"].isna().sum()
        # print("here: "+str(na_start_time))

        print("The most common month is: " + str(most_common_month) + ", the Count was: " + str(count_most_common_month))
        # print(count_month)

        # display the most common start hour
        most_common_start_hour = df.mode()['hour'][0]
        count_most_common_hour = (df.groupby(['hour'])['Start Time'].count()).max()
        print("The most common hour of the day is the {}th hour, the Count was: {}".format(int(most_common_start_hour),count_most_common_hour))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('--' * 60)

    elif day=='all':
        print('\nCalculating The Most Frequent Times of Travel for the City of {}, for the month of {} and for {} days...\n'.format(city.title(), month, day))
        start_time = time.time()
        # display the most common day of week
        most_common_day_of_week = df.mode()['day_of_week'][0]
        count_most_common_day = (df.groupby(['day_of_week'])['Start Time'].count()).max()
        print("The most common day of week is:" + str(most_common_day_of_week) + ", the Count was:" + str(count_most_common_day))

        # display the most common start hour
        most_common_start_hour = df.mode()['hour'][0]
        count_most_common_hour = (df.groupby(['hour'])['Start Time'].count()).max()
        print("The most common hour of the day is the {}th hour, the Count was: {}".format(int(most_common_start_hour),count_most_common_hour))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('--' * 60)

    elif month=='all'and day=='all':
        print('\nCalculating The Most Frequent Times of Travel for the City of {}, for {} months and for {} days...\n'.format(city.title(),month,day))
        start_time = time.time()
        # display the most common month
        most_common_month = df.mode()['month'][0]
        count_most_common_month = (df.groupby(['month'])['Start Time'].count()).max()
        # na_start_time=df["Start Time"].isna().sum()
        # print("here: "+str(na_start_time))

        print("The most common month is: " + str(most_common_month) + ", the Count was: " + str(count_most_common_month))
        # print(count_month)

        # display the most common day of week
        most_common_day_of_week = df.mode()['day_of_week'][0]
        count_most_common_day = (df.groupby(['day_of_week'])['Start Time'].count()).max()
        print("The most common day of week is:" + str(most_common_day_of_week) + ", the Count was:" + str(
            count_most_common_day))

        # display the most common start hour
        most_common_start_hour = df.mode()['hour'][0]
        count_most_common_hour = (df.groupby(['hour'])['Start Time'].count()).max()
        print("The most common hour of the day is the {}th hour, the Count was: {}".format(int(most_common_start_hour),count_most_common_hour))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('--' * 60)


    response= input("POPULAR TRAVEL TIMES: Do you want to go into the data visualization part of the program ?\nInput \"yes\" or \"no\" ! \n(VERY IMPORTANT: make sure the matplotlib and numpy package is installed for this to work!) \n>> ")
    response = response.strip().replace(' ', '_').lower()
    while response=='yes':
        try:


            comp_month = df.groupby(['month'])['Start Time'].count()
            comp_day = df.groupby(['day_of_week'])['Start Time'].count()
            comp_hour = df.groupby(['hour'])['Start Time'].count()

            fig,s=plt.subplots(nrows=1, ncols=3)
            comp_month.plot(ax=s[0],kind='pie',autopct="%.2f",title="Comparing months:Trips as a % of Total \n[Filter:{},{},{}]".format(city,month,day), ylabel="")
            comp_day.plot(ax=s[1],kind='pie', autopct="%.2f",title="Comparing days of the week: Trips as a % of Total\n[Filter:{},{},{}]".format(city,month,day),ylabel="")






            comp_hour.plot(ax=s[2],kind='bar',ylabel="Number of Trips",title="Hour of the day comparison \n[Filter:{},{},{}]".format(city,month,day),figsize=(18,6))
            print("---------------Close the figure to proceed! OR Restart the program!-------------")
            plt.show()

            count_month_day= df.groupby(['month','day_of_week'])['Start Time'].count()
            count_month_day=count_month_day.reindex(["January","February","March","April","May","June"],level=0)
            count_month_day = count_month_day.reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"], level=1)
            count_month_day.unstack().plot(kind='bar', stacked=False, figsize=(10, 6), xlabel='Month', ylabel='Count',title="Month/Day Comaparison \n[Filter:{},{},{}]".format(city,month,day))
            print("---------------Close the figure to proceed! OR Restart the program!-------------")
            plt.show()

            #plt.figure(5)
            #count_hour_day = df.groupby(['day_of_week', 'hour'])['Start Time'].count()
            #count_hour_day = count_hour_day.reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], level=0)
            #count_hour_day_un=count_hour_day.unstack()
            #print(count_hour_day_un)
            #print(count_hour_day_un.shape[0])
            #print(count_hour_day_un.iloc[0,:].nlargest(5))
            #for k in range(count_hour_day_un.shape[0]):
            #    fifth_lar=count_hour_day_un.iloc[k,:].nlargest(5).iloc[-1]
            #    for j in range(count_hour_day_un.shape[1]):
            #        if count_hour_day_un.iloc[k,j]<fifth_lar:
            #            count_hour_day_un.iloc[k, j]=np.nan

            #count_hour_day_un.plot(kind='barh', stacked=False, figsize=(15, 12), xlabel='Month', ylabel='Number of trips',title="Day/Hour Comaparison (Only 5 most popular hours)\n[Filter:{},{},{}]".format(city,month,day))
            #print("---------------Close the figure to proceed! OR Restart the program!-------------")
            #plt.show()
            response='no'
        except NameError:
            print("Error: Make sure matplotlib.pyplot (as plt) and numpy (as np) are both properly imported!")
            response='no'
        #except:
           # print("Skip the visualization part! Something else is wrong")
            #response='no'



def station_stats(df,city,month,day):
    """Displays statistics on the most popular stations and trip."""
    if month!='all'and day!='all':
        print('\nCalculating The Most Popular Stations and Trip the City of {}, for the month of {} and for {}s...\n.'.format(city.title(),month,day))
    elif month=='all':
        print('\nCalculating The Most Popular Stations and Trip for the City of {}, for {} months and for {}s...\n.'.format(city.title(), month, day))
    elif day=='all':
        print('\nCalculating The Most Popular Stations and Trip for the City of {}, for the month of {} and for {} days...\n.'.format(city.title(), month, day))
    elif month=='all'and day=='all':
        print('\nCalculating The Most Popular Stations and Trip for the City of {}, for {} months and for {} days...\n.'.format(city.title(),month,day))


    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df.mode()['Start Station'][0]
    count_start_station=df.groupby(['Start Station'])['Start Time'].count().max()
    print("The most common start station is: {}, the Count was: {}".format(most_common_start_station,count_start_station))
    #print(count_start_station)


    # display most commonly used end station
    most_common_end_station = df.mode()['End Station'][0]
    count_end_station = df.groupby(['End Station'])['Start Time'].count().max()
    print("The most common end station is: {}, the Count was: {}".format(most_common_end_station,count_end_station))

    # display most frequent combination of start station and end station trip

    most_combo=df.groupby(["Start Station",'End Station']).size().idxmax()
    print("The most frequent combination of start and end station is: {}".format(most_combo))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('--'*60)

    response = input(
        "POPULAR STATIONS AND TRIP: Do you want to go into the data visualization part of the program ?\nInput \"yes\" or \"no\" ! \n(VERY IMPORTANT: make sure the matplotlib and numpy package is installed for this to work!) \n>> ")
    response = response.strip().replace(' ', '_').lower()
    while response == 'yes':
        try:
            comp_month = df.groupby(['Start Station','month'])['Start Time'].count()
            comp_month=comp_month.reindex(["January","February","March","April","May","June"],level='month')
            comp_month1=comp_month.unstack()
            #print(comp_month.unstack())
            o1=comp_month1.max()
            o2=comp_month1.idxmax()
            #print(o1)
            #print(o2)
            final_comp_month=pd.concat([o1,o2],axis=1).rename(columns={0:'Counts',1:'Station'})
            #print(final_comp_month)

            ax=final_comp_month.plot(kind='bar')
            i = 0
            for lbl in ax.patches:

                ax.annotate(final_comp_month.iloc[i]['Station'], (lbl.get_x()+0.2, lbl.get_y()+100), color='black',rotation=90)
                i += 1

            plt.ylabel("Count")
            plt.title("Most common Start Stations for each month \n[Filter:{},{},{}]".format(city, month, day))
            print("---------------Close the figure to proceed! OR Restart the program!-------------")
            plt.show()

            comp_day = df.groupby(['Start Station', 'day_of_week'])['Start Time'].count()
            comp_day=comp_day.reindex(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],level='day_of_week')
            comp_day1 = comp_day.unstack()
            # print(comp_month.unstack())
            o1 = comp_day1.max()
            o2 = comp_day1.idxmax()
            final_comp_day = pd.concat([o1, o2], axis=1).rename(columns={0: 'Counts', 1: 'Station'})
            #print(final_comp_day)

            ax1 = final_comp_day.plot(kind='bar')
            i = 0
            for lbl in ax1.patches:
                ax1.annotate(final_comp_day.iloc[i]['Station'], (lbl.get_x() + 0.2, lbl.get_y() + 20), color='black',
                            rotation=90)
                i += 1

            plt.ylabel("Count")
            plt.title("Most common Start Stations for each day \n[Filter:{},{},{}]".format(city, month, day))
            print("---------------Close the figure to proceed! OR Restart the program!-------------")
            plt.show()

            comp_hour = df.groupby(['Start Station', 'hour'])['Start Time'].count()
            comp_hour1 = comp_hour.unstack()
            # print(comp_month.unstack())
            o1 = comp_hour1.max()
            o2 = comp_hour1.idxmax()
            final_comp_hour = pd.concat([o1, o2], axis=1).rename(columns={0: 'Counts', 1: 'Station'})
            #print(final_comp_hour)

            ax2 = final_comp_hour.plot(kind='bar',figsize=(15,10))
            i = 0
            for lbl in ax2.patches:
                ax2.annotate(final_comp_hour.iloc[i]['Station'], (lbl.get_x() + 0.2, lbl.get_y() + 10), color='black',
                             rotation=90)
                i += 1

            plt.ylabel("Count")
            plt.title("Most common Start Stations for each hour \n[Filter:{},{},{}]".format(city, month, day))
            print("---------------Close the figure to proceed! OR Restart the program!-------------")
            plt.show()

            response = 'no'
        except NameError:
            print("Error: Make sure matplotlib.pyplot (as plt) and numpy (as np) are both properly imported!")
            response = 'no'
        except:
            print("Skip the visualization part! Something else is wrong")
            response = 'no'


def trip_duration_stats(df,city,month,day):
    """Displays statistics on the total and average trip duration."""
    if month!='all'and day!='all':
        print('\nCalculating Trip Duration for the City of {}, for the month of {} and for {}s...\n.'.format(city.title(),month,day))
    elif month=='all':
        print('\nCalculating Trip Duration for the City of {}, for {} months and for {}s...\n.'.format(city.title(), month, day))
    elif day=='all':
        print('\nCalculating Trip Duration for the City of {}, for the month of {} and for {} days...\n.'.format(city.title(), month, day))
    elif month=='all'and day=='all':
        print('\nCalculating Trip Duration for the City of {}, for {} months and for {} days...\n.'.format(city.title(),month,day))

    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print("The total travel time was: {} hours".format(total_travel_time/3600))
    # display mean travel time
    mean_travel_time=total_travel_time/(df['Trip Duration']).count()
    print("The Average travel time was: {} mins".format(mean_travel_time/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city,month,day):
    """Displays statistics on bikeshare users."""
    if month!='all'and day!='all':
        print('\nCalculating User Stats for the City of {}, for the month of {} and for {}s...\n.'.format(city.title(),month,day))
    elif month=='all':
        print('\nCalculating User Stats for the City of {}, for {} months and for {}s...\n.'.format(city.title(), month, day))
    elif day=='all':
        print('\nCalculating User Stats for the City of {}, for the month of {} and for {} days...\n.'.format(city.title(), month, day))
    elif month=='all'and day=='all':
        print('\nCalculating User Stats for the City of {}, for {} months and for {} days...\n.'.format(city.title(),month,day))

    start_time = time.time()

    # Display counts of user types
    count_usertype=df.groupby(['User Type']).count()
    print("The counts for each user types are:\n", count_usertype.iloc[:,0])



    # Display counts of gender
    if city=='new york city' or city=='chicago':
        gender_count=df.groupby(['Gender']).count()
        print("The counts for each gender are:\n",gender_count.iloc[:, 0])

        # Display earliest, most recent, and most common year of birth
        earliest_birth=int((df['Birth Year']).min())
        mostrecent_birth =int((df['Birth Year']).max())
        most_common_birth=int(df['Birth Year'].mode()[0])
        print("The earliest birth year is: {},\nthe most recent birth year is: {},\nand the most common birth year is:{}\n".format(earliest_birth,mostrecent_birth,most_common_birth))

    else:
        print('Gender counts and birth year data is not available for the City of Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))

    response = input(
        "USER INFO: Do you want to go into the data visualization part of the program ?\nInput \"yes\" or \"no\" ! \n(VERY IMPORTANT: make sure the matplotlib and numpy package is installed for this to work!) \n>> ")
    response = response.strip().replace(' ', '_').lower()
    while response == 'yes':
        try:


            if city == 'new york city' or city == 'chicago':
                count_user_month = df.groupby(['month', 'User Type'])['Start Time'].count()
                count_user_month = count_user_month.reindex(["January", "February", "March", "April", "May", "June"],
                                                    level='month')
                count_user_month = count_user_month.unstack()

                count_user_day = df.groupby(['day_of_week', 'User Type'])['Start Time'].count()
                count_user_day = count_user_day.reindex(
                    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], level='day_of_week')
                count_user_day = count_user_day.unstack()

                count_gender_month = df.groupby(['month', 'Gender'])['Start Time'].count()
                count_gender_month = count_gender_month.reindex(["January", "February", "March", "April", "May", "June"],level='month')
                count_gender_month = count_gender_month.unstack()

                count_gender_day = df.groupby(['day_of_week', 'Gender'])['Start Time'].count()
                count_gender_day = count_gender_day.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], level='day_of_week')
                count_gender_day = count_gender_day.unstack()

                count_user_month=count_user_month.join(count_gender_month[['Female', 'Male']])
                count_user_day=count_user_day.join(count_gender_day[['Female', 'Male']])

            else:
                count_user_month = df.groupby(['month', 'User Type'])['Start Time'].count()
                count_user_month = count_user_month.reindex(["January", "February", "March", "April", "May", "June"],
                                                    level='month')
                count_user_month = count_user_month.unstack()

                count_user_day = df.groupby(['day_of_week', 'User Type'])['Start Time'].count()
                count_user_day = count_user_day.reindex(
                    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], level='day_of_week')
                count_user_day = count_user_day.unstack()

            fig, axes = plt.subplots(nrows=1, ncols=2)
            count_user_month.plot(ax=axes[0], kind='bar', figsize=(13, 8), title='User type popularity vs month\n[Filter:{},{},{}]'.format(city, month, day))
            count_user_day.plot(ax=axes[1], kind='bar', figsize=(13, 8), title='User type popularity vs day\n[Filter:{},{},{}]'.format(city, month, day))
            plt.show()
            response='no'

        except NameError:
            print("Error: Make sure matplotlib.pyplot (as plt) and numpy (as np) are both properly imported!")
            response = 'no'
        except:
            print("Skip the visualization part! Something else is wrong")
            response = 'no'

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df,city, month, day = load_data(city, month, day)

        time_stats(df,city, month, day)
        station_stats(df,city, month, day)
        trip_duration_stats(df,city, month, day)
        user_stats(df,city, month, day)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
