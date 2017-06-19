# importing classes and variables from another file so that code is neat.
# spy details are stored in objects of classes, these objects are passed as parameters of functions used.
from spyDetails import spy, Spy, ChatMessage, friends
from steganography.steganography import Steganography
from colorama import init
init()
from termcolor import colored

# Intro message of the application.
existing_status_messages = ['My name is Bond, James Bond', 'Shaken, not stirred.', 'I am on duty']
print "Hello spy\nLet's get started"
existing_user = raw_input("Do you want to continue as " + spy.salutation + ' ' + spy.name + "(Y/N):  ")

special_words = ["SOS", "Save Me", "Help Me", "In Trouble", "Run", "They are after you", "Hide"]


# adding a status to spy profile.
def add_status(current_status_message):
    updated_status_message = None
    if spy.current_status_message is not None:
        print 'Your current status message is %s : .' % current_status_message
    else:
        print 'You don\'t have any status messages currently. '
    default = raw_input("Do you want to select from the older status (Y/N)? ")
    # Condition for adding new status.
    if default.upper() == 'N':
        new_status_message = raw_input("What status message do you want to set? ")
        if len(new_status_message) > 0:
            # adding the new status to the existing message list
            existing_status_messages.append(new_status_message)
            updated_status_message = new_status_message
    elif default.upper() == 'Y':
        message_position = 1
        # loop for displaying all the statuses in the status list so that the user can choose.
        for message in existing_status_messages:
            print "%d) %s" % (message_position, message)
            message_position += 1
        selected_message = int(raw_input("Enter the Message Number you want to select : "))
        # checking if the selected message index is less than the total messages
        while len(existing_status_messages) < selected_message:
            print "Please select a valid option from 1 to %d." % len(existing_status_messages)
        updated_status_message = existing_status_messages[selected_message - 1]

    if updated_status_message:
        print "Your new updated message is: %s." % updated_status_message
    else:
        print 'Status message was not updated.'
    return updated_status_message


# Function for adding friends for a user
def add_friend():
    # Defining new friends as objects of Spy class.
    new_friend = Spy('', '', 0, 0.0)
    new_friend.name = raw_input("Please add your friend's name : ")
    new_friend.salutation = raw_input("Are they Mr. or Ms.? : ")

    new_friend.name = new_friend.salutation + " " + new_friend.name

    new_friend.age = int(raw_input("Please enter friends age : "))

    new_friend.rating = float(raw_input("Please enter friends rating : "))

    # Condition for adding friends above a threshold repo.
    if len(new_friend.name) > 0 and new_friend.age > 12 and new_friend.rating >= 2.5:
        friends.append(new_friend)
        print "Friend added with following credentials : Name - %s, age - %d, rating - %.2f" % (new_friend.name, new_friend.age, new_friend.rating)
    else:
        print 'Sorry! Invalid entry. We can\'t add spy with the details you provided'

    return len(friends)


# Function for selecting friend from the friends list so that operations like sending and reading messages can be performed.
def select_friend():
    item_number = 0
    # Loop for selecting friend from the list.
    for friend in friends:
        print '%d. %s aged %d with rating %.2f is online.' % (item_number + 1, friend.name, friend.rating, friend.age)
        # item_number is increased by 1 to eliminate zero indexing.
        item_number = item_number + 1
    friend_choice = raw_input("Choose the serial number of a friend from your friends list : ")
    friend_choice_position = int(friend_choice) - 1
    return friend_choice_position


# Sending a message to the friend selected from select_friend function.
def send_message():
    friend_choice = select_friend()
    original_image = raw_input("What is the name of the image? : ")
    # variable to store the encoded image
    output_path = "output.jpg"
    text = raw_input("What do you want to say? : ")
    while len(text) == 0:
        text = raw_input("You can't send a empty message : ")
    # Concealing text into image using Steganography.
    Steganography.encode(original_image, output_path, text)
    new_chat = ChatMessage(text, True)
    # Saving the message to be sent in friends' list.Each friend is an object of the Spy class.
    friends[friend_choice].chats.append(new_chat)
    print "Your secret message image is ready!"


# Reading a message to the selected friend from the select_friend function.
def read_message():
    sender = select_friend()
    output_path = raw_input("What is the name of the file? : ")
    # decoding the encoded message
    secret_text = Steganography.decode(output_path)
    number_of_words = secret_text.split()
    # condition to check if no message is sent by the friend
    if len(number_of_words) == 0:
        print "There was no encoded message."
    # condition to remove a friend who speaks too much
    elif len(number_of_words) > 100:
         del friends[sender]
        # appending the message to chat history if its not too long
    else:
        new_chat = ChatMessage(secret_text, False)
        # Saving the decoded message in the chats list for the corresponding friend.
        friends[sender].chats.append(new_chat)
        friends[sender].message_number += 1
        # to check if the message contains any special words
        for word in special_words:
            if word.upper() in secret_text.upper():
                print word + " message received"
        print "Your message has been saved."
        print "Your message is : %s." % secret_text
        # checking the average words spoken by each spy
        friends[sender].average_words= (friends[sender].average_words*(friends[sender].message_number-1) + len(number_of_words))/friends[sender].message_number

# Reading chat history
def read_chat_history():
    read_for = select_friend()
    if len(friends[read_for].chats) == 0:
        print "No previous chat history found."
    else:
        # Loop for traversing all the chats in the chats list for the selected friend.
        for chat in friends[read_for].chats:
            # Condition for showing time of message with the message.
            if chat.sent_by_me:
                print(
                    colored("[%s]", "blue") % chat.time.strftime("%d %B %Y") + colored("You said",
                                                                                       "red") + ": " + chat.message)
            else:
                print(colored("[%s]", "blue") % chat.time.strftime("%d %B %Y") + colored("%s", "red") % friends[
                    read_for].name + ": " + chat.message)


# Main function which implements the menu and takes in the detail of a new user or uses the details of the existing user
def start_chat(spy):
    current_status_message = None
    if 17 < spy.age < 41:
        print ("Authentication complete. \nWelcome %s \nage: %d\nrating: %.2f\nProud to have you on board" % (
            spy.name, spy.age, spy.rating))
        # Condition for showing the menu of the application through which the user can choose and perform different operations.
        show_menu = True
        while show_menu:
            menu_choices = "What do you want to do? \n1. Add a status update \n2. Add a friend \n3. Send a secret " \
                           "message \n4. Read a secret message \n5. Read Chats from a user \n6. Close Application " \
                           "\nEnter Your Choice : "
            menu_choice = raw_input(menu_choices)

            if len(menu_choice) > 0:
                menu_choice = int(menu_choice)

                if menu_choice == 1:
                    current_status_message = add_status(current_status_message)
                elif menu_choice == 2:
                    number_of_friends = add_friend()
                    print 'You have %d friends.' % number_of_friends
                elif menu_choice == 3:
                    send_message()
                elif menu_choice == 4:
                    read_message()
                elif menu_choice == 5:
                    read_chat_history()
                else:
                    show_menu = False
    elif spy.age < 18:
        print "You must be 18 to be a spy."
    elif spy.age > 40:
        print "Enjoy pension cheques getting lazy on your couch."

# If spy already exists then user can directly perform operations if not then the application asks for details.
if existing_user.upper() == "Y":
    start_chat(spy)
# Accepting Spy Credentials
else:
    spy = Spy('', '', 0, 0)
    spy.name = raw_input("What's your name? ")
    if len(spy.name) > 0:
        spy.salutation = raw_input("How shall I address you: Mr. or Ms. ? ")

        spy.name = spy.salutation + " " + spy.name
        print "Welcome " + spy.name

        print "Alright " + spy.name + " Let's get to know a little more about you before we proceed!"

        try:
            spy.age = int(raw_input("What's your age? [in integers eg:28]"))
        except ValueError:
            spy.age = int(raw_input("please enter age as integer [in integers eg:28]"))

        spy.rating = float(raw_input("What is your spy rating?"))
        while spy.rating < 0 or spy.rating > 5:
            spy.rating = float(raw_input("Please enter spy rating between 0-5 only: "))
        if spy.rating > 4.5:
            print 'Wow you are an amazing spy'
        elif 3.5 < spy.rating <= 4.5:
            print 'You are a great spy'
        elif 2.5 <= spy.rating <= 3.5:
            print 'You are a promising talent'
        else:
            print "Keep the good work going, you'll improve"

        start_chat(spy)

    else:
        print "Try again with a valid name"
# End
