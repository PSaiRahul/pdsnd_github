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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city =''
    while city not in CITY_DATA.keys():
        print("\nWelcome to this program. Please choose your city:")
        print("\n1. Chicago 2. New York City 3. Washington")
    
        city = input('Name the city you want to analyze the data (chicago, new york city, washington): ').lower()

        if city not in CITY_DATA.keys():
            print("\nPlease check your input, it doesn\'t appear to be conforming to any of the accepted input formats.")
            print("\nRestarting...")
        MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nPlease enter the month, between January to June, for which you're seeking the data:")
    # get user input for month (all, january, february, ... , june)
        month = input('Name the month to filter by or "all" for everything: ').lower()
        if month not in MONTH_DATA.keys():
            print("\nInvalid input. Please try again in the accepted input format.")
            print("\nRestarting...")
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nPlease enter a day in the week of your choice for which you're seeking the data:")
        
        day = input('Name of the day of week to filter by or "all" for everything: ').lower()

        if day not in DAY_LIST:
            print("\nInvalid input. Please try again in one of the accepted input formats.")
            print("\nRestarting...")
        
        
    print('-'*40)
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
    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
# extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
# get user input for day of week (all, monday, tuesday, ... sunday)
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
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    # display the most common month
    popular_month = months[df['month'].mode()[0] - 1].title()
    print(f"Most Popular Month: {popular_month}")

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print(f"\nMost Popular Day: {popular_day}")

    df['hour'] = df['Start Time'].dt.hour
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print(f"\nMost Popular Start Hour: {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_stations = df['Start Station'].value_counts().index
    popular_start_station = popular_start_stations[0]
    print(f"The most popular start station: {popular_start_station}")

    # display most commonly used end station
    popular_End_stations = df['End Station'].value_counts().index
    popular_End_station = popular_End_stations[0]
    print(f"\nThe most popular end station: {popular_End_station}")

    # display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    popular_stations_combo = df['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of trips are from {popular_stations_combo}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    # for splitting the total time into hours, minutes and seconds
    minutes, seconds = divmod(total_travel_time, 60)
    hours, minutes = divmod(minutes, 60)
    print(f"The total trip duration is {hours} hours, {minutes} minutes and {seconds} seconds.")

    # display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    # for splitting the total time into hours, minutes and seconds
    mins, sec = divmod(average_duration, 60)
    
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print(f"The types of users by number are given below:\n\n{user_types}")

    # Display counts of gender
    #Try and excpet block is written to mitigate the issue of not having the column in all city data files
    
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")

    # Display earliest, most recent, and most common year of birth
    #Try and excpet block is written to mitigate the issue of not having the column in all city data files
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There is no 'Birth Year' column in this file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_display(df):
    """Displays 5 rows of raw data for the selected city."""
    raw_data = ''
    response = ['yes', 'no']
    count = 0
    
    while raw_data not in response:
        raw_data = input("\nDo you wish to view the raw data? [Yes/No]").lower()
        if raw_data == 'yes':
            print(df.head())
        elif raw_data not in response:
            print("\nPlease check your input.")
            print("\nRestarting...\n")

    while raw_data == 'yes':
        raw_data = input("\n Do you wish to view more raw data? [Yes/No]").lower()
        count += 5
        if raw_data == 'yes':
            print(df[count:count+5])
        elif raw_data == 'no':
            break
            
    print('-'*40)
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        raw_data_display(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
