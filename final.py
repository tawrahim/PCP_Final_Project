#!/usr/bin/python3

# final.py
# Description:
#
#   This program operates and displays consumer complaints by various criteria.
#   For each question asked, a function was used to aggregate and display that data.
#   Constants declared are used as indexes into the data set list, as well as flags
#   for function calls.
#
#   Some utility functions were written for code re-use. The build_up_data_set()
#   provides a function to reduce the number of iterations through the data set
#   and graph_points() is a function to plot bar charts in a standardized way.
#
#   Other functions are more complicated due to the representation of the data.
#   Where some collections need to be process multiple times, reducing the collection
#   to be smaller and more meaningful with each operation.
#
#   Graphs are represented mostly in bar and pie chart form. Each graph was picked
#   based on what was most appropriate for the given data. Some graphs also contain
#   sup-plots as a comparison tool.
# 
# Known Bugs:
#
#   None
#
# Author: Nicholas Quirk, Tawheed Raheem
# E-Mail: nquirk@student.fitchburgstate.edu, tabdulra@student.fitchburgstate.edu
# Course: CSC 7014 - Spring 2015
# Assignment: Final Project

import csv
from numpy.ma import arange
import pylab
import numpy
import matplotlib.pyplot as plt

# Constants indicating column index
COMPLAINT_ID_COLUMN = 0
PRODUCT_COLUMN = 1
SUB_PRODUCT_COLUMN = 2
ISSUE_COLUMN = 3
SUB_ISSUE_COLUMN = 4
SATE_COLUMN = 5
ZIP_CODE_COLUMN = 6
SUBMITTED_VIA_COLUMN = 7
DATE_RECEIVED_COLUMN = 8
DATE_SENT_COLUMN = 9
COMPANY_NAME_COLUMN = 10
COMPANY_RESPONSE_COLUMN = 11
TIMELY_RESPONSE_COLUMN = 12
CONSUMER_DISPUTED_COLUMN = 13

# Used as a parameter for compare_company_responses_by_year
COMPANY_SUCCESSFUL_RESPONSES = 'successful'
COMPANY_UNSUCCESSFUL_RESPONSES = 'unsuccessful'

# Implicitly immutable.
consumer_complaint_data = []

company_complaints_hash_map = {}
company_and_total_complaints_map = {}
company_break_down_of_complaints = {}
submit_type_with_date_map = {}


def add_entry_to_map(company_name, data_set):
    if company_name in company_complaints_hash_map:
        company_complaints_hash_map[company_name].append(data_set)
    else:
        company_complaints_hash_map[company_name] = [data_set]


# This function reads the contents of csv file
def read_contents_in_csv_file(file_name):
    with open(file_name) as f:
        reader = csv.reader(f)
        next(reader, None)  # skip the headers

        total_number_of_complaints = 0

        for line in reader:
            total_number_of_complaints += 1
            company_name = line[COMPANY_NAME_COLUMN]
            add_entry_to_map(company_name, line)
            consumer_complaint_data.append(line)


def submit_type_with_date(data_set):
    for x in data_set:
        k = x[SUBMITTED_VIA_COLUMN]
        v = x[DATE_RECEIVED_COLUMN]
        if k in submit_type_with_date_map:
            submit_type_with_date_map[k].append(v)
        else:
            submit_type_with_date_map[k] = [v]


def group_complaints_based_on_state(data_set):
    result = {}
    for x in data_set:
        state = x[SATE_COLUMN]
        if state == "":
            state = "N/A"
        if state in result:
            result[state] += 1
        else:
            result[state] = 1
    return result


# Our data set is very huge so it only makes sense that
# we don't go through our data set when not needed.
# This function is a greedy algorithm that solves that problem,
# we filter  all the data set we need in one pass through
def build_up_data_set():
    for company_name in company_complaints_hash_map:
        data_set_for_company = company_complaints_hash_map[company_name]
        submit_type_with_date(data_set_for_company)

        company_break_down_of_complaints[company_name] = group_complaints_based_on_state(data_set_for_company)
        company_and_total_complaints_map[company_name] = len(data_set_for_company)


# This function returns an ordered list of company name
# and the total number of complaints logged against them
# Each of the list item contains a tuple in the format
# (companyName, #Complaints)
# The returned list is from the lowest to the highest
def get_all_companies_and_the_number_of_complaints_logged_against_them():
    return sorted(company_and_total_complaints_map.items(), key=lambda x: x[1])


# Find the 5 companies with the highest successful or unsuccessful reponses.
# A response category flag is passed in for the purpose of selecting the desired output.
def compare_company_responses_by_year(response_category):

    company_year_successes = {}

    # Build a map of company-year -> successful response count
    for complaint in consumer_complaint_data:

        if response_category == COMPANY_SUCCESSFUL_RESPONSES:
            # Closed with X is a successful response to the customer
            if not complaint[COMPANY_RESPONSE_COLUMN].find('Closed with ') == -1:

                # mapKey is companyName-YYYY
                mapKey = complaint[COMPANY_NAME_COLUMN]+'-'+(complaint[DATE_SENT_COLUMN][6:])
                if company_year_successes.get(mapKey) is not None:
                    company_year_successes[mapKey] = company_year_successes[mapKey]+1
                else:
                    company_year_successes[mapKey] = 1
        elif response_category == COMPANY_UNSUCCESSFUL_RESPONSES:

            if complaint[COMPANY_RESPONSE_COLUMN].find('Closed with ') == -1:

                mapKey = complaint[COMPANY_NAME_COLUMN]+'-'+(complaint[DATE_SENT_COLUMN][6:])
                if company_year_successes.get(mapKey) is not None:
                    company_year_successes[mapKey] = company_year_successes[mapKey]+1
                else:
                    company_year_successes[mapKey] = 1

    # Convert the map into a list of tuples (response count, company-year)        
    company_year_successes_list = []
    for successKey in company_year_successes:
        company_year_successes_list.append((company_year_successes[successKey], successKey))

    top_companies = set()

    # Sort the list of tuples in reverse order, then take the top 5.
    company_year_successes_list.sort(key=lambda x:x[0], reverse=True)

    for entry in company_year_successes_list:
        company = entry[1].split('-')[0]
        if len(top_companies) == 5:
            break
        else:
            top_companies.add(company)

    # Create two maps which will hold a list of entries for each company.
    # This part is done so we can sort the counts by year.
    # company -> [years]
    # company -> [counts]
    company_year_success_series = {}
    company_year_success_count_series = {}

    for entry in company_year_successes_list:
        company = entry[1].split('-')[0]
        year = entry[1].split('-')[1]
        response_count = entry[0]
        company_set = set()
        company_set.add(company)
        if len(company_set.intersection(top_companies)) == 1:

            if company_year_success_series.get(company) is None:
                company_year_success_series[company] = [year]
                company_year_success_count_series[company] = [response_count]
            else:
                company_year_success_series.get(company).append(year)
                company_year_success_count_series.get(company).append(response_count)

    company_year_successes = {}

    # Create a list of tuples for sorting. Zip the company -> [years] and company -> [counts] together.
    for company in company_year_success_series:
        company_year_successes[company] = list(zip(company_year_success_series[company], company_year_success_count_series[company]))
        company_year_successes[company].sort()

    companies_legend = []
    plot_x = []
    plot_x_labels = set()
    company_count = 0

    # Create the lists necessary to plot the years on the x-axis,
    # where companies fall in year buckets.
    # Plot the counts on the y-axis.
    for company in company_year_successes:

        years = []
        counts = []
        companies_legend.append(company)
        
        for values in company_year_successes[company]:
            years.append(values[0])
            counts.append(values[1])
            plot_x_labels.add(values[0])

        width = 0.1
        plot_x = numpy.arange(1, len(years)+1)
        a = plot_x + (company_count*0.1)
        pylab.bar(a, counts, width, color=get_random_color())

        company_count += 1
    
    pylab.legend(companies_legend)
    labels = list(plot_x_labels)
    labels.sort()
    pylab.xticks(plot_x, labels)
    pylab.xlabel('years')
    if response_category == COMPANY_SUCCESSFUL_RESPONSES:
        pylab.ylabel('Customer Complaint Resolution Counts')
    elif response_category == COMPANY_UNSUCCESSFUL_RESPONSES:
        pylab.ylabel('Unresolved Complaint Counts')
    
    if response_category == COMPANY_SUCCESSFUL_RESPONSES:
        pylab.title('Closed Responses')
    elif response_category == COMPANY_UNSUCCESSFUL_RESPONSES:
        pylab.title('Unresolved Responses.')
    pylab.show()

# Finds the top 5 complatins by year and displays a pie chart for each year.
def compare_complaints_by_year():

    # Collect all complaints into a map of complaint -> count.
    complaints_count = {}
    for complaint in consumer_complaint_data:
        customer_issue = complaint[ISSUE_COLUMN]
        if complaints_count.get(customer_issue) is not None:
            complaints_count[customer_issue] = complaints_count[customer_issue]+1
        else:
            complaints_count[customer_issue] = 1

    # Put complains into a list of tuples.
    complaints_count_list = []
    for complaint in complaints_count:
        complaints_count_list.append((complaints_count[complaint], complaint))

    # Take the top 5 complaints by sorting in reverse order, then taking the first 5.
    top_complaints = set()

    complaints_count_list.sort(key=lambda x:x[0], reverse=True)

    for entry in complaints_count_list:
        complaint = entry[1]
        if len(top_complaints) == 5:
            break
        else:
            top_complaints.add(complaint)

    # Given our top complaints, now find the complaints by year.
    # Populate a map of maps: YYYY -> complaint -> complaint count.
    company_year_complaints = {}
    
    for complaint in consumer_complaint_data:

        customer_issue = complaint[ISSUE_COLUMN]
        mapKey = complaint[DATE_SENT_COLUMN][6:]

        complaint_set = set()
        complaint_set.add(customer_issue)
        if len(complaint_set.intersection(top_complaints)) == 1:

            if company_year_complaints.get(mapKey) is not None:
                if company_year_complaints.get(mapKey).get(customer_issue) is not None:
                    company_year_complaints[mapKey][customer_issue] = company_year_complaints[mapKey][customer_issue]+1
                else:
                    company_year_complaints[mapKey][customer_issue] = 1
            else:
                company_year_complaints[mapKey] = {customer_issue: 1}

    year_set = set()
    for year in company_year_complaints:
        year_set.add(year)

    graph_year_list = []
    for year in year_set:
        graph_year_list.append(year)

    graph_year_list.sort()
    
    subplot_count = 1
    
    graph_colors = []

    while not (len(graph_colors) == 5):
        graph_colors.append(get_random_color())

    # For each year, create a pie sub-plot and graph it.
    for year in graph_year_list:

        complaint_desc = []
        complaint_count = []

        for complaint in company_year_complaints[year]:
            complaint_desc.append(complaint+" - "+str(company_year_complaints[year][complaint]))
            complaint_count.append(company_year_complaints[year][complaint])

        plt.subplot(len(graph_year_list),1,subplot_count)
        subplot_count = subplot_count + 1
        plt.title(year)
        patches, texts = plt.pie(complaint_count, colors=graph_colors)
        plt.legend(patches, complaint_desc, loc="best")

    plt.suptitle('Top 5 Complaints by Year')
    plt.show()

# Counts the submitted via for each year and graphs a pie chart for each year.
def find_submitted_via_by_year():

    submit_via_by_year = {}

    # Create a map to count the submitted via by year: submitted year -> submitted via -> count
    for complaint in consumer_complaint_data:

        complaint_via = complaint[SUBMITTED_VIA_COLUMN]
        complaint_year = complaint[DATE_SENT_COLUMN][6:]

        if submit_via_by_year.get(complaint_year) is not None:
            if submit_via_by_year[complaint_year].get(complaint_via) is not None:
                submit_via_by_year[complaint_year][complaint_via] = submit_via_by_year[complaint_year][complaint_via] + 1
            else:
                submit_via_by_year[complaint_year][complaint_via] = 1
        else:
            submit_via_by_year[complaint_year] = {complaint_via : 1}

    # Use a set to find all unique years.
    submitted_years_set = set()

    for submitted_year in submit_via_by_year:
        submitted_years_set.add(submitted_year)

    # Turn the above set into a list so we can sort the years
    # prior to graphing.
    submitted_years_list = []
    for submitted_year in submitted_years_set:
        submitted_years_list.append(submitted_year)
    submitted_years_list.sort()
    
    subplot_count = 1

    graph_colors = []

    while not (len(graph_colors) == 6):
        graph_colors.append(get_random_color())

    # Graph each submitted year on a sub-plot with a legend.
    for submit_year in submitted_years_list:
        
        via_counts = []
        via_type = []
        
        for submitted_via in submit_via_by_year[submit_year]:
            via_counts.append(submit_via_by_year[submit_year][submitted_via])
            via_type.append(submitted_via+' - '+str(submit_via_by_year[submit_year][submitted_via]))

        plt.subplot(len(submitted_years_set),1,subplot_count)
        subplot_count = subplot_count + 1
        plt.title(submit_year)
        patches, texts = plt.pie(via_counts, colors=graph_colors)
        plt.legend(patches, via_type, loc="best")

    plt.suptitle('Complaints Submitted Via by Year')
    plt.show()


# Utility function to generate a random color for graping.
# The colors this returns are generally better than the defaults.
def get_random_color():
    n = 50
    return numpy.random.rand(n)


# Function to graph data in bar chart form.
def graph_points(x_labels, y_labels, title, xlabel, ylabel):
    colors_array = []

    for _ in x_labels:
        colors_array.append(get_random_color())

    width = 0.35
    ind = arange(len(x_labels))
    plt.bar(ind, y_labels, width, color=colors_array)

    pylab.xticks(ind+width/2, x_labels)
    plt.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    pylab.show()


def graph_top_n_complained_about_product(n):
    data_set = get_all_companies_and_the_number_of_complaints_logged_against_them()[-n:]

    x_labels = []
    y_labels = []
    for x in data_set:
        x_labels.append(x[0])
        y_labels.append(x[1])

    graph_points(x_labels, y_labels, "Top 5 most complained about companies", "Company Name", "Number of complaints")


def graph_company_distribution_of_complaints_based_on_states(company_name):
    data_set = company_break_down_of_complaints[company_name]

    # We cant possibly show all 50 states on the graph so we show a small sample size
    number_of_states_to_show = 20

    x_labels = []
    y_labels = []
    for x in data_set:
        y_labels.append(data_set[x])
        x_labels.append(x)

    graph_points(x_labels[0:number_of_states_to_show], y_labels[0:number_of_states_to_show], "Break down of " +
                 company_name + "'s complaints by " + str(number_of_states_to_show) + " states ",
                 "State Name", "Number of complaints in State")


def graph_count_of_submission_type():
    data_set = submit_type_with_date_map

    x_labels = []
    y_labels = []
    for x in data_set:
        y_labels.append(len(data_set[x]))
        x_labels.append(x)

    graph_points(x_labels, y_labels, " ", "Type of Submission", "Number of Submission")


def main():
    # Pass file name to this function for any pre-processing.
    read_contents_in_csv_file("Consumer_Complaints.csv")

    # Called to create additional data structures for aggregation by other functions.
    build_up_data_set()

    '''
    while True:
        print("Drilling down by state level. ")
        print("Example of valid companies are: ")
        print("------------------------------")
        print()

        companies = company_break_down_of_complaints.keys()
        for name in companies[0:10]:
            print(name)

        user_input = input("Enter a name of a company: ")
        print(user_input)
        if user_input in company_break_down_of_complaints:
            graph_company_distribution_of_complaints_based_on_states(user_input)
        else:
            print("The company you entered is not valid, example of valid companies are: ")
            for name in companies[0:10]:
                print(name)
            continue

        if user_input == "done":
            return
    '''

    # Aggregation and graphing functions.
    graph_top_n_complained_about_product(5)
    graph_company_distribution_of_complaints_based_on_states("Citibank")
    graph_count_of_submission_type()
    compare_company_responses_by_year(COMPANY_SUCCESSFUL_RESPONSES)
    compare_company_responses_by_year(COMPANY_UNSUCCESSFUL_RESPONSES)
    compare_complaints_by_year()
    find_submitted_via_by_year()


# Entry point of the app
if __name__ == '__main__':
    main()
