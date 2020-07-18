import time
import pandas as pd
import numpy as np
line=0
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
    city = input("Choose the city to analyze, chicago, new york city or washington: ").lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("Please enter one city:chicago, new york city or washington: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("please choose the month you want to analyze or all for no month filter: ").lower()
    while month not in ('january','february','march','april','may','june','all'):
        month=input('Please choose one month from this list : january, february, march, april, may, june').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = print("please choose the day to analyze or all for no day filter: ")
    while day not in ('saturday','sunday','monday','tuesday','wednesday','thursday','friday','all'):
        day = input("Please enter a correct day").lower()

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
    df = pd.read_csv(CITY_DATA[city])
    # we convert data in column Start_time to date time type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # now we can extract the data in each row of Start_time column and creat month, day of week and hour columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # we will need hour column to calculate statistics in the next function
    df['hour']=df['Start Time'].dt.hour
    # In this bloc, we filter data by month and day
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        # we created a list of months (data available only from january to june)
        # june= months.index(june)+1 >> june=5+1 >> june =6 (because list index start from 0 , so june index's in the list is 5)
        month = months.index(month) +1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    # start_time returns the duration of response calculation
    start_time = time.time()

    # TO DO: display the most common month
    common_month=df['month'].mode()[0]
    print('The most common month is: ',common_month)

    # TO DO: display the most common day of week
    common_day=df['day_of_week'].mode()[0]
    print('The most common day of week is: ',common_day)

    # TO DO: display the most common start hour
    common_start_hour=df['hour'].mode()[0]
    print('The most common start hour is: ',common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    commonly_used_start_station=df['Start Station'].mode()[0]
    print('Most commonly used start station is: ',commonly_used_start_station)

    # TO DO: display most commonly used end station
    commonly_used_end_station=df['End Station'].mode()[0]
    print('Most commonly used end station is: ',commonly_used_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    # first, we need to fuse both start and end columns in one
    df['Start End'] = df['Start Station'] + ' >> ' + df['End Station']
    commonly_used_start_end_station = df['Start End'].mode()[0]
    print('The most frequent combination of start station and end station trip is:\n ',commonly_used_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time=sum(df['Trip Duration'])
    print('Total travel time is: ',total_travel_time, 'seconds')

    # TO DO: display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print('Mean travel time is: ',mean_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types=df['User Type'].value_counts()
    print('Counts of user types:\n',user_types)

    # only washington city doesn't have gender and year of birth columns
    if city=='washington':
        print('{} city has no user statistics'.format(city))
    else:
        # TO DO: Display counts of gender
        gender=df['Gender'].value_counts()
        print('Counts of gender:\n',gender)

        # TO DO: Display earliest, most recent, and most common year of birth
        #the earliest year of birth
        earliest_year=min(df['Birth Year'])
        print('The earliest year of birth is: ',earliest_year)

        #the most recent year of Birth
        recent_year=max(df['Birth Year'])
        print('the most recent year of birth is: ',recent_year)

        #the most common year of birth
        most_common_years=df['Birth Year'].mode()[0]
        print('The most common year of birth is: ',most_common_years)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df,city):
    answer=input('Do you want to see 5 lines of raw data, Enter yes or no\n')
    #we declare line as global variable and we had previously define it ^ in line N°4
    global line
    while True:
        if answer =='yes':
            if city=='chicago' or city=='new york city':
                # we use loc to access 5 lines in each loop
                print(df.loc[0:line+4,['Start Time','End Time','Trip Duration','Start Station','End Station','User Type','Gender','Birth Year']])
                # we increment line by 4 because index start in 0
                line=line+4
                # we return the function so that it asks again the user if he wants see more 5 lines
                return raw_data(df,city)
            else:
                #this is the case of washington, because it doesn't contain gender and birth year columns
                print(df.loc[0:line+4,['Start Time','End Time','Trip Duration','Start Station','End Station','User Type']])
                # we increment line by 4 as we did previously
                line=line+4
                # we return the function so that it asks again the user if he wants see more 5 lines
                return raw_data(df,city)
        elif answer=='no':
            # in this case the function returns nothing
            return

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
