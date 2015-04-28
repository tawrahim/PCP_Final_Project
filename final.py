#!/usr/bin/python3

import csv
import pylab
import numpy

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

# Implicitly immutable.
consumer_complaint_data = []

company_complaints_hash_map = {}
most_complained_by_product_map = {}
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

        print("Total number of complaints is: " + str(total_number_of_complaints))


# Question 2
def submit_type_with_date(data_set):
    for x in data_set:
        k = x[SUBMITTED_VIA_COLUMN]
        v = x[DATE_RECEIVED_COLUMN]
        if k in submit_type_with_date_map:
            submit_type_with_date_map[k].append(v)
        else:
            submit_type_with_date_map[k] = [v]


# Helper function used by question 1
def group_complaints_based_on_state(data_set):
    result = {}
    for x in data_set:
        state = x[SATE_COLUMN]
        if state in result:
            result[state] += 1
        else:
            result[state] = 1
    for s in result:
        if s == "":
            print("N/S" + " " * 4 + str(result[s]))
        else:
            print(s + " " * 5 + str(result[s]))


# Question 1: Total number of complaints by company by region
def total_number_of_complaints_based_on_company():
    x_axis = []
    y_axis = []
    print("Company Name                                                  #Of Complaints")
    print("----------------------------------------------------------------------------")
    for company_name in company_complaints_hash_map:
        data_set_for_company = company_complaints_hash_map[company_name]
        submit_type_with_date(data_set_for_company)

        max_spaces = 68
        number_of_complaints = len(data_set_for_company)
        x_axis.append(company_name)
        y_axis.append(number_of_complaints)
        print(str(company_name) + str(" "*(max_spaces - len(company_name)) +
                                      str(number_of_complaints)))
        group_complaints_based_on_state(data_set_for_company)

        most_complained_by_product_map[company_name] = number_of_complaints
    # Plot the points on a graph
    # pylab.plot(y_axis)
    # pylab.xticks(y_axis, x_axis)


# Question 3
def print_most_complained_about_product():
    print()
    print("Products and their complains")
    print("----------------------------")
    max_spaces = 68
    sorted_list = sorted(most_complained_by_product_map.items(), key=lambda x: x[1])
    for k in sorted_list:
        print(k[0] + str(" "*(max_spaces - len(k[0]))) + str(k[1]))


# Find the 5 companies with the highest successful responses.
# Find total successful responses for each company for every year.
# Create two maps, where the keys are the company name, 1 map holds a list of years, the other map holds a list of
#   total successful response for that year.
# TODO: Plot the 5 companies on a graph. y-axis is companies, y-axis is response count.
# TODO: Make the constant 5 a variable passed into the function, so we can include more companies if performance allows.
def compare_company_responses_by_year():

    company_year_successes = {}

    for complaint in consumer_complaint_data:

        # Closed with X is a successful response to the customer
        if not complaint[COMPANY_RESPONSE_COLUMN].find('Closed with ') == -1:

            # mapKey is companyName-YYYY
            mapKey = complaint[COMPANY_NAME_COLUMN]+'-'+(complaint[DATE_SENT_COLUMN][6:])
            if company_year_successes.get(mapKey) is not None:
                company_year_successes[mapKey] = company_year_successes[mapKey]+1
            else:
                company_year_successes[mapKey] = 1

    company_year_successes_list = []
    for successKey in company_year_successes:
        company_year_successes_list.append((company_year_successes[successKey], successKey))

    top_companies = set()

    company_year_successes_list.sort(key=lambda x:x[0], reverse=True)

    for entry in company_year_successes_list:
        company = entry[1].split('-')[0]
        if len(top_companies) == 5:
            break
        else:
            top_companies.add(company)

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
    
    # create a list of tuples for sorting...
    for company in company_year_success_series:
        #company_year_successes.append((company_year_success_series[company], company_year_success_count_series[company]))
        #print(company, company_year_success_series[company], company_year_success_count_series[company])
        company_year_successes[company] = list(zip(company_year_success_series[company], company_year_success_count_series[company]))
        #company_year_successes[company].sort(key=lambda x:x[0], reverse=False)
        company_year_successes[company].sort()

    companies_legend = []
    plot_x = []
    plot_x_labels = set()
    company_count = 0
    for company in company_year_successes:

        years = []
        counts = []
        companies_legend.append(company)
        
    
        for values in company_year_successes[company]:
            years.append(values[0])
            counts.append(values[1])
            plot_x_labels.add(values[0])

        width = 0.25
        plot_x = numpy.arange(1, len(years)+1)
        pylab.bar(plot_x + (company_count*0.1), counts, 0.1, color=get_random_color())

        company_count = company_count + 1
    
    pylab.legend(companies_legend)
    labels = list(plot_x_labels)
    labels.sort()
    pylab.xticks(plot_x, labels)
    pylab.xlabel('years')
    pylab.ylabel('Successful Customer Complaint Resolution Counts')
    pylab.show()



def compare_company_complaints_by_year(graph_year):

    # collect all complaints into a map of complaint -> count
    complaints_count = {}
    for complaint in consumer_complaint_data:
        customer_issue = complaint[ISSUE_COLUMN]
        if complaints_count.get(customer_issue) is not None:
            complaints_count[customer_issue] = complaints_count[customer_issue]+1
        else:
            complaints_count[customer_issue] = 1

    # put complains into a list of tuples
    complaints_count_list = []
    for complaint in complaints_count:
        complaints_count_list.append((complaints_count[complaint], complaint))

    # take the top 5 complaints
    top_complaints = set()

    complaints_count_list.sort(key=lambda x:x[0], reverse=True)

    for entry in complaints_count_list:
        complaint = entry[1]
        if len(top_complaints) == 5:
            break
        else:
            top_complaints.add(complaint)

    # debug for showing the complaints.
    # TODO: Remove
    # print(top_complaints)


    company_year_complaints = {}

    for complaint in consumer_complaint_data:

        customer_issue = complaint[ISSUE_COLUMN]
        mapKey = complaint[COMPANY_NAME_COLUMN]+'-'+(complaint[DATE_SENT_COLUMN][6:])

        complaint_set = set()
        complaint_set.add(customer_issue)
        if len(complaint_set.intersection(top_complaints)) == 1:

            if company_year_complaints.get(mapKey) is not None:
                if company_year_complaints.get(mapKey).get(customer_issue) is not None:
                    company_year_complaints[mapKey][customer_issue] = company_year_complaints[mapKey][customer_issue]+1
                else:
                    company_year_complaints[mapKey] = {customer_issue: 1}
            else:
                company_year_complaints[mapKey] = {customer_issue: 1}

    complaints_to_company_count = {}
    for company_year in company_year_complaints:
        company_name = company_year.split('-')[0]
        company_year_key = company_year.split('-')[1]

        if company_year_key == graph_year:
            for company_complaint in company_year_complaints[company_year]:
                if company_year_complaints[company_year][company_complaint] > 50:
                    if complaints_to_company_count.get(company_year_key) is not None:
                        complaints_to_company_count[company_year_key].append((company_complaint, company_year_complaints[company_year][company_complaint], company_name))
                    else:
                        complaints_to_company_count[company_year_key] = [(company_complaint, company_year_complaints[company_year][company_complaint], company_name)]
            #for k2 in company_year_complaints[k1]:
            #    if company_year_complaints[k1][k2] > 50:
            #        print(k1, company_year_complaints[k1])

    for k in complaints_to_company_count:
        complaints_to_company_count[k].sort()
        print(k, complaints_to_company_count[k])

def get_random_color():
    n = 50
    return numpy.random.rand(n)

def main():
    read_contents_in_csv_file("Consumer_Complaints.csv")
    compare_company_responses_by_year()
    compare_company_complaints_by_year('2015')
    #total_number_of_complaints_based_on_company()
    #print_most_complained_about_product()


# Entry point of the app
if __name__ == '__main__':
    main()
