import argparse
from datetime import datetime
from json import load

# Keeping it static for initiating only once
todays_date = datetime.now()
def get_days_from_creation_date(creation_date):
    # Converting creation date into a date object
    date_format = "%Y-%m-%dT%H:%M:%S"
    created_date_object = datetime.strptime(creation_date, date_format)

    # Calculating no of days between todays date and creation date
    days_object = todays_date - created_date_object
    return days_object.days


def find_files_older_than_retention(file_path, retention_days, prefix):
    all_images_due_deletion = []
    prefixed_images_due_deletion = []
    with open(file_path) as fh:
        file_content = load(fh)
    for data in file_content:
        days_since_created = get_days_from_creation_date(data['creationTimestamp'].split('.')[0])
        if days_since_created >= retention_days:
            """We can use just simple counter here for counting images that are due for deletion but instead using list
               to store images for further processing if required
            """
            # count+=1
            all_images_due_deletion.append(data['name'])

            # if the image name always starts with a prefix we can use startswith or we can use below
            # if search_string in data['name']
            if data['name'].startswith(prefix):
                # As explained above using list for storing prefixed strings
                # string_count+=1
                prefixed_images_due_deletion.append(data['name'])
            # print(data['name']," : ", days)

    print("Total no of images that are due for deletion: ", len(all_images_due_deletion))
    print("Total no of images that are due for deletion starting with prefix '{0}': {1}".format(prefix, len(prefixed_images_due_deletion)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--retention_days', '-d', required=True, type=int,
                        help="A number that represents how long the file should stay in the bucket, after which it is deleted")
    parser.add_argument('--prefix', '-s', required=True, type=str, help="A prefix string for object name")
    parser.add_argument('--file_path', '-p', required=True, type=str, help="Path of a input file")
    args = parser.parse_args()

    # Calling main function
    find_files_older_than_retention(args.file_path, args.retention_days, args.prefix) 
	
	
	
	
	