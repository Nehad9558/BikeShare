import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months=('january', 'february', 'march', 'april', 'may', 'june', 'all')
days=('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all')
  
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
    
    while True:
        city = input('Which city do you want to explore chicago, new york or washington?').lower()
        if city in CITY_DATA:
            break

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = input('can you provide us the month name?').lower()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    day = input('can you type one of the day of week you want to analyze?').lower()
    
    if month == '' and day == '':
        return city, months, days
    elif month == '' and day != '':
        return city, months, day
    elif month != '' and day == '':
        return city, month, days
    else:
        return city, month, day 

    print('-'*40)
        
    print(city, month, day)
    return city, month, day


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print(most_common_month,most_common_day_of_week,most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_commonly_start_station = df['Start Station'].value_counts().idxmax()

    # display most commonly used end station
    most_commonly_end_station = df['End Station'].value_counts().idxmax()

    # display most frequent combination of start station and end station trip
    most_frequent_start_end_station = df[['Start Station', 'End Station']].mode().iloc[0]
    print(most_commonly_start_station,most_commonly_end_station,most_frequent_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()

    # display mean travel time
    mean = df['Trip Duration'].mean()
    print(total,mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    # Display counts of gender
    gender = df['Gender'].value_counts()
    print(gender)

    # Display counts of gender
    try:    
       gender_count = df['Gender'].value_counts().to_frame()
       print('Bike riders gender:\n' ,gender_count)
    except KeyError:
       print("\nGender Types:\nNo data available for this month.")

    # Display earliest, most recent, and most common year of birth
    try:
       Earliest_Year = df['Birth Year'].min()
       print('\nEarliest Year:', Earliest_Year)
       Most_Recent_Year = df['Birth Year'].max()
       print('\nMost Recent Year:', Most_Recent_Year)
       Most_Common_Year = df['Birth Year'].value_counts().idxmax()
       print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
       print("\n\nSorry, No data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def display_raw_data(city):
    """
    The fuction takes the city name from get_filters fuction as input 
    and returns the raw data of that city by chunks of 5 rows.
    Args:
        (str) city - name of the city to return the raw data.
    Returns:
        df - raw data of that city by chunks of 5 rows.
    """
    print('\nRaw data is available to check... \n')

    display_raw = input("you want to have a look on more raw data? Type Yes or No\n").strip().lower()
    
    while display_raw == 'yes':
          try:
          
             for chunk in pd.read_csv(CITY_DATA[city], chunksize=5):
                print(chunk) 
                # repeating the question
                display_raw = input("you want to have a look on more raw data? Type Yes or No\n").strip().lower()
                if display_raw != 'yes':
                    print('Thank You')
                    break
             break
          except KeyboardInterrupt:
            clear()
            print('Thank you.')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
