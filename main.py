import os
import pocket
import random
from twilio.rest import Client

# Developer Consumer Key
consumer_key = "{}".format(os.environ['POCKET_CONSUMER_KEY'])

# Access Token (generated elsewhere)
access_token = "{}".format(os.environ['POCKET_ACCESS_TOKEN'])

def getLibrary(response):
    return response[0]["list"]

def main():
    try:
        # Retrieve the current Pocket library.
        p = pocket.Pocket(consumer_key, access_token)
        response = p.get()

        # Randomly select an article.
        library = getLibrary(response)
        article = random.choice(list(library.values()))

        # Retrieve the article's:
        resolved_title = article["resolved_title"]
        resolved_url = article["resolved_url"]

        # String to send:
        body_message = "\n \"{}\" \n {}".format(resolved_title, resolved_url)

    except pocket.PocketException as error:
        # (i.e. if the access_token is old, catch the
        # error and text me the error that was sent.)
        print error
        body_message = error

    print body_message
    # Uncomment when you actually want to use the API --- note that it will
    # draw from your Twilio balance.
    account_sid = '{}'.format(os.environ['TWILIO_ACCOUNT_SID'])
    auth_token = '{}'.format(os.environ['TWILIO_AUTH_TOKEN'])
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=body_message,
                         from_=os.environ['TWILIO_NUMBER'],
                         to=os.environ['PERSONAL_NUM']
                     )

if __name__ == "__main__":
    main()
