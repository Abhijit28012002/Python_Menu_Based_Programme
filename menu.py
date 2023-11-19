import os
import wikipedia
from twilio.rest import Client
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from geopy.geocoders import Nominatim
from pygooglenews import GoogleNews
import cv2
import openai

# Set Open AI API Key
openai.api_key="Paste your API Key"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

###########################################
# GeoLocation Function
def searchLocation(location):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(location)
    latitude = location.latitude
    longitude = location.longitude

    print(f"{bcolors.OKGREEN} Latitude: {latitude}, Longitude: {longitude}{bcolors.ENDC} ")

###########################################
# Wikipedia search Function
def wikipediaSearch():
        type_search= input("Search: ")
        info=wikipedia.summary(type_search,1)
        print(info)


###########################################

# chatgpt Function
def chatGPTSearch(queries):
    output = openai.Completion.create(
    prompt =queries,
    model="text-davinci-003"
    )
    FinalData = output["choices"][0]["text"]
    print(FinalData)

###########################################

# Tending News
def tendingNews(query):
    result=[]
    c=0
    gn = GoogleNews(lang = 'en')
    search = gn.search(query)
    newsitem = search['entries']
    for item in newsitem:
        story={
            'title': item.title,
            'link': item.link
        }
        result.append(story)
        c=c+1
        if c==5:
            return result

###########################################

# Send Whatsapp Message Function
def send_whatsapp_message(to_number, message_body):
    # Twilio Account SID and Auth Token
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Your Twilio WhatsApp number (you must enable it in your Twilio console)
    from_whatsapp_number = 'whatsapp:+14155238886'

    # Send the message
    message = client.messages.create(
        body=message_body,
        from_=from_whatsapp_number,
        to=f'whatsapp:{to_number}'
    )

    # Print the SID (unique ID) of the message
    print(f'Message sent with SID: {message.sid}')


###########################################


# Send SMS Function
def send_sms(to_number, message_body):
    # Twilio Account SID and Auth Token
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Your Twilio phone number
    from_phone_number = 'your_twilio_phone_number'

    # Send the SMS
    message = client.messages.create(
        body=message_body,
        from_=from_phone_number,
        to=to_number
    )

    # Print the SID (unique ID) of the message
    print(f'SMS sent with SID: {message.sid}')

###########################################


# Send Email function
def send_email(subject, body, to_email):
    # Sender's email address and password
    sender_email = 'your_email@gmail.com'
    password = 'your_password'

    # Recipient's email address
    receiver_email = to_email

    # Message setup
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, 'plain'))

    # SMTP server setup (for Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Establish a secure connection to the SMTP server
    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print(f'Email sent to {receiver_email} successfully.')


###########################################


# Video Player Function
def play_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Get the frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Create a window to display the video
    cv2.namedWindow('Video Player', cv2.WINDOW_NORMAL)

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Break the loop if the video has ended
        if not ret:
            break

        # Display the frame in the window
        cv2.imshow('Video Player', frame)

        # Wait for the next frame
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break

    # Release the video capture object and close the window
    cap.release()
    cv2.destroyAllWindows()


###########################################


# Main Function
def main():
    print(f"{bcolors.HEADER}\t\t\tMenu Driven Programme{bcolors.ENDC}")
    print(f"""{bcolors.OKBLUE}
        1. Open Notepad
        2. Open Chrome
        3. Send Whatsapp messages
        4. Send Email
        5. Send SMS
        6. ChatGPT Chat
        7. Search Geolocation
        8. Retrieve the Current Trend News
        9. Search Wikipedia Summary
        10. Video Player
        11. Exit
          {bcolors.ENDC}""")
    while True:
        choose = input(f"{bcolors.OKGREEN}Enter which operation you what to perform: {bcolors.ENDC}")
        if choose=='1':
            os.system("notepad")
        elif choose=='2':
            os.system("chrome")
        elif choose=='3':
            recipient_number = input("Enter Your Mobile Number: ")
            message = input("Enter Your Message: ")
            send_whatsapp_message(recipient_number, message)
        elif choose=='4':
            subject=input("Enter Subject of the email: ")
            body = input("Enter Body of the Email: ")
            recipient_email = input("Write Reciver Email Address: ")
            send_email(subject,body,recipient_email)
        elif choose=='5':
            number=input("Enter Mobile Number: ")
            message_body = input("Enter Message Body: ")
            send_sms(number, message_body)
        elif choose=='6':
            query = input("Enter Your Query: ")
            chatGPTSearch(query)
        elif choose=='7':
            location=input("Enter Location Name you want to know about: ")
            searchLocation(location)
        elif choose=='8':
            query= input("Enter News Type: ")
            result = tendingNews(query)
            for i in range(0,len(result)):
                print(f"{bcolors.OKCYAN}Title: {result[i]['title']}{bcolors.ENDC} \n{bcolors.OKBLUE}Link: {result[i]['link']}\n{bcolors.ENDC}")
        elif choose=='9':
            wikipediaSearch()
        elif choose=='10':
            video_input=input("The path to your video file: ")
            play_video(video_input)
        elif choose=='11':
            break
        else:
            print("Choose Valid option")
    

###########################################


if __name__=="__main__":
    main()
    

    