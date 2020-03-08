import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters_city():
    """
    Asks user to specify a city to analyze.

    Returns:
        (str) city - name of the city to analyze
    """
    ask_city = "Enter name of the city to analyze: "
    valid_cities = "Chicago, New York City, Washington"
    error_city = "Sorry, that is an invalid city.\nUse one of these cities: "
    error_city += valid_cities

    while True:
        try:
            city = input(ask_city).strip().lower()
            if city in CITY_DATA:
                break
            print(error_city)
            continue
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        else:
            break

    return city.lower()

def get_filters_month():
    """
    Asks user to specify a month to analyze.

    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    """
    ask_month = "Enter name of the month to filter by, or \"all\" to apply "
    ask_month += "no month filter: "

    while True:
        try:
            month = input(ask_month).strip().title()
            if month == '':
                month = 'empty'
            if month == 'All':
                break
            if month in calendar.month_name:
                break
            if month in calendar.month_abbr:
                month_index = list(calendar.month_abbr).index(month.title())
                month = list(calendar.month_name)[month_index]
                break
            print("Sorry, that is an invalid month.")
            continue
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        else:
            break

    return month.lower()

def get_filters_day():
    """
    Asks user to specify a day to analyze.

    Returns:
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    ask_day = "Enter day of the week to filter by, or \"all\" to apply "
    ask_day += "no day of week filter: "

    while True:
        try:
            day = input(ask_day).strip().title()
            if day == '':
                day = 'empty'
            if day == 'All':
                break
            if day in calendar.day_name:
                break
            if day in calendar.day_abbr:
                break
            print("Sorry, that is an invalid day of the week.")
            continue
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        else:
            break

    return day.lower()

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('-'*40)
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    #HINT: Use a while loop to handle invalid inputs
    city = get_filters_city()

    # get user input for month (all, january, february, ... , june)
    month = get_filters_month()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_filters_day()

    print('-'*40)
    return city, month, day

def load_raw_data(city, month, day):
    """
    Loads raw data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city raw data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    if city == 'washington':
        df['Gender'] = np.nan
        df['Birth Year'] = np.nan

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = list(calendar.month_name).index(month.title())

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    #extract month from Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month
    # print the most common month
    print('Most common month: ', calendar.month_name[df['month'].mode()[0]])

    # display the most common day of week
    #extract month from Start Time column to create an month column
    df['week'] = df['Start Time'].dt.dayofweek
    # print the most common month
    print('Most common day of week: ', calendar.day_name[df['week'].mode()[0]])

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    print('Most common start hour: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most commonly used end station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    trip = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('Most frequent combination of start and end station trip: ', trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #duration data frame
    duration = df['Trip Duration']

    # display total travel time
    print('Total travel time: {:,.0f} hours'.format(duration.sum() / 60 / 60))

    # display mean travel time
    print('Mean travel time: {:,.0f} minutes'.format(duration.mean() / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:')
    for key, value in dict(df['User Type'].value_counts()).items():
        print('{:<12}'.format(key) + '{:>8,}'.format(value))

    # Display counts of gender
    print('\nCounts of gender:')
    for key, value in dict(df['Gender'].value_counts()).items():
        print('{:<8}'.format(key) + '{:>8,}'.format(value))

    # Display earliest, most recent, and most common year of birth
    birth = df['Birth Year']
    print('\nEarliest year of birth:    {:.0f}'.format(birth.min()))
    print('Most recent year of birth: {:.0f}'.format(birth.max()))
    print('Most common year of birth: {:.0f}'.format(birth.mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Asks user if they want to see the raw data in the data frame.
    """
    RAW_DATA_INCREMENT = 5
    ask_raw_data = "Do you want to see the raw data? Enter yes or no.\n"
    ask_more_data = 'Do you want to see {} more records? Enter yes or no.\n'.format(RAW_DATA_INCREMENT)
    error_response = "Sorry, that is an invalid response. "
    start = 0
    end = RAW_DATA_INCREMENT

    while True:
        try:
            # asking to display for raw data
            response = input(ask_raw_data).strip().lower()
            if response == 'yes':
                print(df[start:end])
                start += RAW_DATA_INCREMENT
                end += RAW_DATA_INCREMENT

                while True:
                    try:
                        # asking to display more raw data
                        response = input(ask_more_data).strip().lower()
                        if response == 'yes':
                            print(df[start:end])
                            start += RAW_DATA_INCREMENT
                            end += RAW_DATA_INCREMENT
                            continue
                        if response == 'no':
                            break
                        print(error_response)
                        continue
                    except ValueError:
                        print("Sorry, I didn't understand that.")
                        continue
                    else:
                        break
                break
            if response == 'no':
                break
            print(error_response)
            continue
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        else:
            break

def main():
    """
    Allows user to pick city, month, and day filters to be used to generate analysis
    of bike share data. Also can display the raw data used in the analysis.
    """
    while True:
        city, month, day = get_filters()
        df = load_raw_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
