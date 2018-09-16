import requests
import smtplib


def get_emails():
    emails = {}

    try:    
        email_file = open('emails2.txt', 'r')

        for line in email_file:
           (email, name) = line.split(',')
           emails[email] = name.split() 

    except FileNotFoundError as err:
        print(err) 

    return emails

def get_schedule():
    try:
        schedule_file = open('schedule.txt', 'r')

        schedule = schedule_file.read()
    except FileNotFoundError as err:
        print(err)

    return schedule

def get_weather_forecast():
    url = 'http://api.openweathermap.org/data/2.5/find?q=London&units=imperial&appid=aae1b9020bf8b6efb7ef83a430982fe8'
    weather_request = requests.get(url)
    weather_json = weather_request.json()

    print(weather_json)

    description = weather_json['list'][0]['weather'][0]['description']
    print(description)
    temp_min = weather_json['list'][0]['main']['temp_min']
    temp_max = weather_json['list'][0]['main']['temp_max']
    print(temp_min)
    print(temp_max)

    forecast = 'The city forecast for today is '
    forecast += description + ' with a high of ' + str(int(temp_max))
    forecast += ' and a low of ' + str(int(temp_min)) +'.'

    return forecast

def send_emails(emails, schedule, forecast):
    # Connect to the smtp server
    server = smtplib.SMTP(host='smtp.gmail.com', port='587')    # Start TLS encryption
    server.starttls()

    # Login
    password = input("What's your password?")
    from_email = 'mr.yemane@gmail.com'
    server.login(from_email, password)

    # Send to entire email list
    for to_email, name in emails.items():
        message = 'Subject: Daily forecast !\n'
        message += 'Hi ' + name[0] +' '+name[1] + '!\n\n'
        message += 'How are you doing today? Here is the forecast for the day and your schedule''\n'
        message += forecast + '\n\n'
        message += schedule + '\n\n'
        message += 'Have a great rest of your day!'
        server.sendmail(from_email, to_email, message)

    server.quit()

def main():
    emails = get_emails()
    print(emails)

    schedule = get_schedule()
    print(schedule)

    forecast = get_weather_forecast()
    print(forecast)

    send_emails(emails, schedule, forecast)
    print("Emails sent.")

main()
