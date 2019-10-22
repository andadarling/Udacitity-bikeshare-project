import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ['chicago','new york city', 'washington']
    input_city = input("which city would you like to see data for chicago, new york city or washington?: ").lower()
    while input_city.lower() not in city:
        print("this city does not exist, please try again!", end='')
        input_city = input("Please try again: ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    input_month = input("please select a month?'january', 'february', 'march', 'april', 'may', 'june' or all : ").lower()
    while input_month.lower() not in month:
        print("please check spelling and try again!", end='')
        input_month = input("please try again: ").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ['monday','tuesday', 'wednesday','thursday','friday','saturday','sunday','all']
    input_day = input("which day would you like to select:'monday','tuesday', 'wednesday','thursday','friday','saturday','sunday' or all?:" ).lower()
    while input_day.lower() not in day:
        print("please check spelling and try again!", end='')
        input_day = input("please try again: ").lower()

    print('-'*40)
    return input_city, input_month, input_day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
   
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month    
    commom_month = df['month'].mode()[0]
    print('The most commom month for start time is:',commom_month)

    # TO DO: display the most common day of week
    df['week'] = df['Start Time'].dt.dayofweek    
    commom_week = df['week'].mode()[0]
    print('The most common day of the week is {}.'.format(commom_week))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour    
    popular_hour = df['hour'].mode()[0]
    print('The most Popular Start Hour is:',popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    commom_start = df["Start Station"].mode()[0]#df['Start Station'].mode.to_string(index=False)
    print('The most commonly used start station is: ',commom_start)

    # TO DO: display most commonly used end station
    commom_end = df["End Station"].mode()[0]#df['End Station'].mode.to_string(index=False)
    print('The most commonly used end station is: ',commom_end)

    # TO DO: display most frequent combination of start station and end station trip 
    comb_start_end_station = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print('The most most frequent combination of start station and end station trip is: ',comb_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df["travel_time"] = df["End Time"] - df["Start Time"]
    
    # TO DO: display total travel time
    total_travel_time = df["travel_time"].sum()
    print('The total travel time is {} seconds.'.format(total_travel_time))

    # TO DO: display mean travel time
    average_travel_time = df["travel_time"].mean()
    print('The average travel time is {} seconds.'.format(average_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Count of User Type:\n",user_types)
    print("\n")

    # TO DO: Display counts of gender
    if "Gender" in df.columns:
        gender = df["Gender"].value_counts()
        print("Count of Gender Type: \n", gender)
        print("\n")
    else:
        print("Gender column does not exists")
        

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent= int(df['Birth Year'].max())
        most_commom = int(df['Birth Year'].mode())
        print('The oldest users are born in {}.'.format(earliest))
        print('The youngest users are born in {}.'.format(most_recent))
        print('The most commom birth year is {}.'.format(most_commom))
    else:
        print("Birth Year column does not exists")

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        
        display = input('\nWould you like to view individual trip data? '
                            'Enter \'yes\' or \'no\'.\n').lower()
        if display.lower() == 'yes':
            head = 0
            tail = 5
        # prints 5 columns of individual trips
            print(df[df.columns[0:-1]].iloc[head:tail])           
            display_more = input('\nWould you like to view more individual'
                                     ' trip data? Type \'yes\' or \'no\'.\n').lower()
            
            while display_more.lower() == 'yes':
                head += 5
                tail += 5
                print(df[df.columns[0:-1]].iloc[head:tail], end='')
                display_more = input('\nWould you like to view more individual'
                                     ' trip data? Type \'yes\' or \'no\'.\n').lower()
                if display_more.lower() == 'no':
                        break
             
            


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
