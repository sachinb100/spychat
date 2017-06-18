#for deault user the app import the details from spy_class.
from spy_class import spy, Spy, ChatMessage, friends
from steganography.steganography import Steganography
from datetime import datetime
from colorama import init
from termcolor import colored, cprint
init()

STATUS_MESSAGES = ['Hey there I am using spychat', 'Busy in my work', 'At movie','The day is very good today','At party']


print "Hello! Let\'s get started"
#Asking the user if they want to continue with the default user or create their own.
question = "Do you want to continue as " + spy.salutation + " " + spy.name + " (Y/N)? "
existing = raw_input(question)

#Adding status of a spy
def add_status():

    updated_status_message = None

    if spy.current_status_message != None:
#app displaying current status message.
        print 'Your current status message is %s \n' % (spy.current_status_message)
    else:
        print 'You don\'t have any status message currently \n'

    default = raw_input("Do you want to select from the older status (y/n)? ")

    if default.upper() == "N":
        new_status_message = raw_input("What status message do you want to set? ")


        if len(new_status_message) > 0:
            STATUS_MESSAGES.append(new_status_message)
            updated_status_message = new_status_message

    elif default.upper() == 'Y':

        item_position = 1

        for message in STATUS_MESSAGES:
            print '%d. %s' % (item_position, message)
            item_position = item_position + 1

        message_selection = int(raw_input("\nChoose from the above messages "))


        if len(STATUS_MESSAGES) >= message_selection:
            updated_status_message = STATUS_MESSAGES[message_selection - 1]

    else:
        print 'The option you chose is not valid! Press either y or n.'
#printing updated message
    if updated_status_message:
        print 'Your updated status message is: %s' % (updated_status_message)
    else:
        print 'You current don\'t have a status update'

    return updated_status_message

#Adding new friend in a spy chat
def add_friend():

    new_friend = Spy('','',0,0.0)

    new_friend.name = raw_input("Please add your friend's name: ")
    new_friend.salutation = raw_input("Are they Mr. or Ms.?: ")

    #new_friend.name = new_friend.salutation + " " + new_friend.name

    new_friend.age = raw_input("Age?")
    new_friend.age = int(new_friend.age)

    new_friend.rating = raw_input("Spy rating?")
    new_friend.rating = float(new_friend.rating)

    if len(new_friend.name) > 0 and new_friend.age > 12 and new_friend.rating >= spy.rating:
        friends.append(new_friend)
        print 'Friend Added!'
    else:
        print 'Sorry! Invalid entry. We can\'t add spy with the details you provided'

    return len(friends)

#Selecting a friend from chat to communicate
def select_a_friend():
    item_number = 0

    for friend in friends:
        print '%d. %s %s aged %d with rating %.2f is online' % (item_number +1, friend.salutation, friend.name,
                                                   friend.age,
                                                   friend.rating)
        item_number = item_number + 1

    friend_choice = raw_input("Choose from your friends")

    friend_choice_position = int(friend_choice) - 1

    return friend_choice_position

#sending secret message to a friend through a image
def send_message():
  try:
    friend_choice = select_a_friend()

    original_image = raw_input("What is the name of the image?")
    output_path = "output.jpg"
    text = raw_input("What do you want to say? ")
    Steganography.encode(original_image, output_path, text)

    new_chat = ChatMessage(text,True)

    friends[friend_choice].chats.append(new_chat)

    print "Your secret message image is ready!"
  except TypeError:
      print "Your image does not contain any message."

#Reading secret message from a friend
def read_message():
 #calling select_a_friend method to get which friend is to be communicated with.
    sender = select_a_friend()
 #Ask the user for the name of the image they want to decode the message from.
    output_path = raw_input("What is the name of the file?")

    secret_text = Steganography.decode(output_path)
 #if image does not containing any message
    if not secret_text:
        print "Your image does not contain any message."


    new_chat = ChatMessage(secret_text,False)
    # Append the chat dictionary to chats key for the particular friend.
    friends[sender].chats.append(new_chat)

    print "Your secret message is:"
    print secret_text
    words=secret_text.split()
 #Remove a spy for speaking too much
    if len(words)>100:
        print "You are speaking too much."
        friends.remove(friends[sender])



# Method for Printing chat history from a particular friend
def read_chat_history():

    read_for = select_a_friend()

    print '\n'
#Adding  the message to a chat dictionary which should contain the message, time of the message and a boolean indicating whether the sender was you or a friend.
    for chat in friends[read_for].chats:
        #Print a colored output for reading chat history
        if chat.sent_by_me:
           print colored(chat.time.strftime("%d %B %Y %A %H: %M"),"blue")
           print colored("You said:","red")
           print colored(chat.message,"green")

        else:

            print colored(chat.time.strftime("%d %B %Y %A %H: %M"),"blue")
            print colored(friends[read_for].name,"red")
            print colored(chat.message,"green")

#start chatting from friends
def start_chat(spy):

    spy.name = spy.salutation + " " + spy.name


    if spy.age > 12 and spy.age < 50:

#printing welcome message for spy
        print "Authentication complete. Welcome " + spy.name + " age: " \
              + str(spy.age) + " and rating of: " + str(spy.rating) + " Proud to have you onboard"

        show_menu = True
#App displaying a menu for the user.
        while show_menu:
            menu_choices = "What do you want to do? \n 1. Add a status update \n 2. Add a friend \n 3. Send a secret message \n 4. Read a secret message \n 5. Read Chats from a user \n 6. Close Application \n"
            menu_choice = raw_input(menu_choices)

            if len(menu_choice) > 0:
                menu_choice = int(menu_choice)

                if menu_choice == 1:
                    spy.current_status_message = add_status()
                elif menu_choice == 2:
                    number_of_friends = add_friend()
                    print 'You have %d friends' % (number_of_friends)
                elif menu_choice == 3:
                    send_message()
                elif menu_choice == 4:
                    read_message()
                elif menu_choice == 5:
                    read_chat_history()
                else:
                    show_menu = False
#Dispalying meassage if spy age is not fufill
    else:
        print 'Sorry you are not of the correct age to be a spy'

if existing.upper() == "Y":
    start_chat(spy)

elif existing.upper() == "N" :

    spy = Spy('','',0,0.0)

#For custom user app ask the name
    spy.name = raw_input("Welcome to spy chat, you must tell me your spy name first: ")

    if len(spy.name) > 0:
#Ask the custom user the salutation he/she want
        spy.salutation = raw_input("Should I call you Mr. or Ms.?: ")
#Ask the user for their age
        spy.age = raw_input("What is your age?")
        spy.age = int(spy.age)

        spy.rating = raw_input("What is your spy rating?")
        spy.rating = float(spy.rating)
        if spy.rating>4.7:
            print "Great spy"
        elif spy.rating<4.7 and spy.rating>2.5:
            print "You are average spy rating"
        else:
            print "You can do better."

        start_chat(spy)
#If custom user enter invalid name then it display warning.
    else:
        print 'Please add a valid spy name'
else:
    print "Please enter y or n"
