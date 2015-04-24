import csv

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

# Implicity immutable.
consumer_complaint_data = []

company_complaints_hash_map = {}


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

        for line in reader:
            company_name = line[COMPANY_NAME_COLUMN]
            add_entry_to_map(company_name, line)
            consumer_complaint_data.append(line)


# Question 1: Total number of complaints by company by region
def total_number_of_complaints_by_region():
    pass

# Find the 5 companies with the higest successful responses.
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


    for k in company_year_success_series:
        print(k, company_year_success_series[k], company_year_success_count_series[k])


def compare_company_complaints_by_year():

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
    print(top_complaints)


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

    for k1 in company_year_complaints:
        for k2 in company_year_complaints[k1]:
            if company_year_complaints[k1][k2] > 50:
                print(k1, company_year_complaints[k1])

def main():
    read_contents_in_csv_file("Consumer_Complaints.csv")

    compare_company_responses_by_year()
    compare_company_complaints_by_year()


# Entry point of the app
if __name__ == '__main__':
    main()
    print("")
