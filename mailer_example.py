import pandas as pd
import MailerService as MailerService
import time

FILE_PATH = "Example.xlsx"
# Optional, Will prompt user if None (Both email and pass)
LOGIN_EMAIL= None
LOGIN_PASSWORD= None # Set a new App password from https://myaccount.google.com/apppasswords

def load_data(file_path):
    df = pd.read_excel(file_path)  # You can also use pd.read_csv for CSV files
    return df 

if __name__ == "__main__":
    with MailerService.MailerService(LOGIN_EMAIL,LOGIN_PASSWORD) as mailer :
        data = load_data(FILE_PATH)
        for index, row in data.iterrows() :
            email,name = str(row['EMAIL']),str(row['NAME']) # Change Column names
            to_email = email
            subject = f'This is an example mail to {name}' # Change subject
            message_list = [(f'Hello {name}','plain')] # Change message with their mime types
            attachments_list = ['dog2.jpg'] # Change with the file paths
            mailer.send_email(to_email,subject,message_list,attachments_list)
            # time.sleep(15) # To add delay between mails to not get spam listed