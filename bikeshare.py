import time
import pandas as pd
import numpy as np

#loading csv files
dir_chicago = chicago.csv
dir_new_york_city = new_york_city.csv
dir_washington = washington.csv

#creating a dictionary for each csv file
CITY_DATA = { 'chicago': dir_chicago,
              'new york': dir_new_york_city,
              'washington': dir_washington}
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
    while True:
        city = input("Which city would you like to explore the data: Chicago, New York, or Washington?").lower()
        if city in CITY_DATA:
            break
        else:
            print("That's not a valid answer. Please choose one city among the choices.")

    # get user input for month (all, january, february, ... , june)
    valid_months = ["january", "february", "march", "april", "may", "june", "all"]
    while True:
        month = input("Which month(s) would you like to explore the data: January, February, March, April, May, June, or ALL?").lower()
        if month in valid_months:
            break
        else:
            print("That's not a valid answer. Please choose a month among the choices or ALL.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday", "all"]
    while True:
        day = input("Which day(s) would you like to explore the data: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or ALL?").lower()
        if day in valid_days:
            break
        else:
            print("That's not a valid answer. Please choose a day among the choices or ALL.")

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
    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    month_dict ={1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June"}
    print("The most popular month is", month_dict[popular_month] + ".")
    # display the most common day of week
    popular_day = df['day'].mode()[0]
    print("The most popular day is", popular_day + ".")
    # display the most common start hour
    popular_start_hour = df['Start Time'].dt.hour.mode()[0]
    hour_dict = {0:"12 AM", 1:"1 AM", 2: "2 AM", 3: "3 AM", 4: "4 AM", 5: "5 AM", 6: "6 AM", 7: "7 AM", 8: "8 AM",
                 9:"9 AM", 10: "10 AM", 11: "11 AM", 12: "12 PM", 13: "1 PM", 14: "2 PM", 15: "3 PM", 16: "4 PM",
                 17: "5 PM", 18: "6 PM", 19: "7 PM", 20: "8 PM", 21: "9 PM", 22: "10 PM", 23: "11 PM"}
    print("The most popular start hour is", hour_dict[popular_start_hour] + ".")
    print("\nCalculation of time statistics took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return popular_month, popular_day, popular_start_hour

#print(time_stats(load_data('new york','all','all')))

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most popular start station is", popular_start_station + ".")
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most popular end station is", popular_end_station + ".")
    # display most frequent combination of start station and end station trip
    popular_start_end = df.groupby(['Start Station','End Station']).size().idxmax()
    print("The most popular start and end stations are {} and {}.".format(popular_start_end[0],popular_start_end[1]))
    print("\nCalculation of station statistics took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return popular_start_station, popular_end_station, popular_start_end

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in years
    total_travel_time_year = df["Trip Duration"].sum()/(3600*24*365)
    print("The total travel time is {} year(s).".format(total_travel_time_year))
    # display mean travel time in min
    mean_travel_time_min = df["Trip Duration"].mean()/60
    print("The average travel time is {} minutes.".format(mean_travel_time_min))
    print("\nCalculation of trip duration statistics took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return total_travel_time_year, mean_travel_time_min

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("There are {} subscribers and {} customers.".format(user_types['Subscriber'], user_types['Customer']))

    # Display counts of gender
    if "Gender" in df:
        gender = df['Gender'].value_counts()
        print("There are {} males and {} females.".format(gender['Male'], gender['Female']))
        # Display earliest, most recent, and most common year of birth
        earliest_birth = int(df['Birth Year'].min())
        recent_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode()[0])
        print("The earliest, most recent, and most common birth years are {}, {} and {}, respectively.".format(
            earliest_birth, recent_birth, common_birth))
        print("\nCalculation of user statistics took %s seconds." % (time.time() - start_time))
        print('-' * 40)
        return user_types, gender, earliest_birth, recent_birth, common_birth
    else:
        print("No gender and birth year data for Washington.")
        return user_types
    
def display_raw_data(df):
  """
    Asks user if they want to see 5 lines of raw data.
    Returns the 5 lines of raw data if user inputs `yes`. Iterate until user response with a `no`

    """

    data = 0

    while True:
        answer = input('Would you like to see 5 lines of raw data? Enter yes or no: ')
        if answer.lower() == 'yes':
            print(df[data : data+5])
            data += 5

        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

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
