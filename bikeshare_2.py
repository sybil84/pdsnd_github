import time
import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter
import calendar

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
    city = ''
    while city not in ['chicago', 'new york city', 'washington']:
        city = str(input('\nEnter a city: chicago, new york city or washington\n')).lower()

    # get user input for month (all, january, february, ... , june)
    months = [x.lower() for x in list(calendar.month_name)[1:]]
    months.append('all')
    month = ''
    while month not in months:
        month = str(input('\nEnter the full name of a month (example january) or all:\n')).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = [x.lower() for x in list(calendar.day_name)]
    day = ''
    while day not in days:
        day = str(input('\nEnter the full name of a day (example monday) or all:\n')).lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters the Start Time field by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    date_parser = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    df = pd.read_csv(CITY_DATA[city], parse_dates=['Start Time', 'End Time'], date_parser=date_parser)

    # Read the CSV file with custom date parsing
    if month != 'all':
        df = df[df['Start Time'].dt.strftime("%B").str.lower() == month]
    if day != 'all':
        df = df[df['Start Time'].dt.strftime("%A").str.lower() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_df = [x.strftime("%B") for x in list(df['Start Time'])]
    most_common_month = max(set(month_df), key=month_df.count)
    print("\nThe most common month for travel is " + most_common_month)

    # display the most common day of week
    day_df = [x.strftime("%A") for x in list(df['Start Time'])]
    most_common_day = max(set(day_df), key=day_df.count)
    print("\nThe most common day for travel is " + most_common_day)

    # display the most common start hour
    hour_df = [x.hour for x in list(df['Start Time'])]
    most_common_hour = max(set(hour_df), key=hour_df.count)
    print("\nThe most common hour for travel is " + str(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stations = list(df['Start Station'])
    most_common_start_station = Counter(start_stations).most_common(1)[0][0]
    print("\nThe most commonly used start station is " + most_common_start_station)

    # display most commonly used end station
    end_stations = list(df['End Station'])
    most_common_end_station = Counter(end_stations).most_common(1)[0][0]
    print("\nThe most commonly used end station is " + most_common_end_station)

    # display most frequent combination of start station and end station trip
    df['most_common_combo_station'] = df.apply(lambda x: x['Start Station'] + "-" + x['End Station'], axis=1)
    combo_stations = list(df['most_common_combo_station'])
    most_common_trip = Counter(combo_stations).most_common(1)[0][0]
    print("\nThe most common start and end station combo is " + most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is " + str(df['Trip Duration'].sum()))

    # display mean travel time
    print("The average travel time is " + str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nUsers grouped by type:")
    print(df.groupby('User Type').size())

    # Display counts of gender
    print("\nUsers grouped by gender:")
    print(df.groupby('Gender').size())

    # Display earliest, most recent, and most common year of birth
    print("\nEarliest Birth Year: " + str(min(df['Birth Year'])))
    print("\nLatest Birth Year: " + str(max(df['Birth Year'])))
    print("Most common birth year: " + str(Counter(df['Birth Year']).most_common(1)[0][0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


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
