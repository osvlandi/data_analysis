import time
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('')
    print('Hello! Let\'s explore some US bikeshare data!')
    print('')

    # Get user input for city (chicago, new york city, washington). A while loop will handle invalid inputs.
    while True:
        try:
            city = str(input('Would you like to see data for Chicago, New York, Washington or all? ').title())
            break
        except ValueError:
            print('That is not a valid city!')
        except KeyboardInterrupt:
            print('No input taken')
            break

    # Get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('Which month? ').title())
            break
        except ValueError:
            print('That is not a valid month!')
        except KeyboardInterrupt:
            print('No input taken')
            break


    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('Which day of the week? ').title())
            break
        except ValueError:
            print('That is not a valid day of the week!')
        except KeyboardInterrupt:
            print('No input taken')
            break

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
    #Loads data for the chosen city:
    if city == 'All':
        df_from_each_file = (pd.read_csv(value) for key, value in CITY_DATA.items())
        df = pd.concat(df_from_each_file, ignore_index=True)
    else:
        df = pd.read_csv(CITY_DATA[city])

    # Converts the Start Time column to datetime:
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Creates a month column fom the Start Time column:
    df['month'] = df['Start Time'].dt.month_name()

    # Creates a day of the week column from the Start Time column:
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Creates a hour column from the Start Time column:
    df['hour'] = df['Start Time'].dt.hour

    # Filters by month:
    if month != 'All':
        df = df[df['month'] == month]

    # Filters by day of the week
    if day != 'All':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month
    try:
        common_month = df['month'].mode()[0]

        print('')
        print('Most common month: {}'.format(common_month))

    except:
        print('')
        print('No month data available!')

    # Displays the most common day of week
    try:
        common_day = df['day_of_week'].mode()[0]

        print('')
        print('Most common day of the week: {}'.format(common_day))

    except:
        print('')
        print('No day of the week data available!')


    # Displays the most common start hour
    try:
        common_start_hour = df['hour'].mode()[0]

        print('')
        print('Most common start hourt: {} hours'.format(common_start_hour))

    except:
        print('')
        print('No start hour data available!')

    print('')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    try:
        common_start_station = df['Start Station'].value_counts().idxmax()

        print('')
        print('Most common start station: {} '.format(common_start_station))

    except:
        print('')
        print('No start station data available!')

    # Displays most commonly used end station
    try:
        common_end_station = df['End Station'].value_counts().idxmax()
        print('')
        print('Most common end station: {} '.format(common_end_station))

    except:
        print('')
        print('No end station data available!')

    # Displays most frequent combination of start station and end station trip
    try:
        common_start_end_stations = df.groupby(['Start Station','End Station']).size().idxmax()

        print('')
        print('Most common combination of start and end stations: {}'.format(common_start_end_stations))

    except:
        print('')
        print('No start and end station data available!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    try:
        total_travel_time = df['Trip Duration'].sum()
        print('')
        print('Total travel time: {}'.format(total_travel_time))

    except:
        print('')
        print('No total time travel data available!')

    # Displays mean travel time
    try:
        mean_travel_time = df['Trip Duration'].mean()
        print('')
        print('Mean travel time: {}'.format(mean_travel_time))

    except:
        print('')
        print('No mean travel time data available!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #Prints a trip duration histogram
    try:
        fig = sns.displot(df['Trip Duration'])
        fig.savefig('trip_duration_distplot.png')

    except:
        print('')
        print('Could not print trip duration plot!')



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    try:
        user_count = df['User Type'].value_counts()

        print('')
        print('Count of user types: {}'.format(user_count))

    except:
        print('')
        print('No user type data available')

    # Displays counts of gender
    try:
        gender_count = df['Gender'].value_counts()

        print('')
        print('Count of genders: {}'.format(gender_count))

        print('')
        print('Printing Gender Countplot!')
        plot = sns.countplot(x='Gender', data=df)
        fig = plot.get_figure()
        fig.savefig('gender_count.png')


    except:
        print('')
        print('No gender data available!')

    # Displays earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]

        print('')
        print('Earliest year of birth: {}'.format(earliest_birth_year))

        print('')
        print('Most recent year of birth: {}'.format(most_recent_birth_year))

        print('')
        print('Most common year of birth: {}'.format(most_common_birth_year))

    except:
        print('')
        print('No birthday data available!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def data_explorer(df):
    start_point = 0
    end_point = 5

    #This makes sure that columns are not collapsed when displayed.
    pd.set_option('display.max_columns',200)

    while True:
        viewData = str(input("Would you like to see the raw data? Type 'Yes' or 'No' ")).lower()

        if (viewData == 'yes') or (viewData == 'y'):
            print(df[start_point : end_point])

            start_point += 5
            end_point += 5

        else:
            print('Ending data explorer')
            break



def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
        except:
            print('Invalid input!')
            break

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_explorer(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if (restart.lower() != 'yes') and (restart.lower() != 'y'):
            print('')
            print('See you later!')
            break


if __name__ == "__main__":
	main()
