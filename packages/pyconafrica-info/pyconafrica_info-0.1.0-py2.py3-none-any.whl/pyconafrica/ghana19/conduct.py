"""
This file contains the code of conduct of the event.
"""
from colorama import init, Style, Back, Fore
init()

CODE = [
    {
        'category': 'Introduction',
        'content': \
"""We want all attendees to have an enjoyable experience at PyCon Africa. 
All attendees - delegates, speakers, volunteers, sponsors, exhibitors and 
organisers - are expected to abide by this Code of Conduct. 
If necessary, the organisers will act to enforce it.

All attendees are expected to show respect and courtesy to others throughout 
the conference and at all conference events. This includes social and fringe events, 
whether officially sponsored by PyCon Africa or not.
"""
    },
    {
        'category': 'Communication',
        'content': \
"""All communication should be appropriate for a general audience, 
which will include people from many different religions, cultures and nations.

Sexual language and imagery are not welcome.

Please be thoughtful when making jokes or discussing sensitive topics or issues 
that are likely to have a strong personal effect on some people. 
If in doubt, ask for advice or simply moderate your expression.
"""
    },
    {
        'category': 'Harassment',
        'content': \
"""PyCon Africa will not tolerate harassment in any form, or language, 
imagery or behaviour that are:

    -> sexist, racist or exclusionary
    -> intimidating or threatening
    -> insulting or unpleasant

Harassment can include any unwelcome behaviour directed at another person.
"""
    },
    {
        'category': 'In the event of a problem',
        'content': \
"""If you are troubled by the behaviour of another attendee at the conference, 
or are concerned that another attendee may be in distress, 
please speak immediately to any member of conference staff or 
contact our code of conduct liaison volunteers. 
See how to report a code of conduct concern.

Your concern will be heard in confidence, taken seriously, 
and dealt with according to a documented procedure for handling code of conduct reports.

Conference staff - volunteers and organisers - will be on hand throughout the conference. 
Any concern, whatever it is, will be immediately passed on to a member 
of the conference committee. The committee will investigate promptly and 
if necessary will take appropriate action. This could include:

    -> asking a violator of the Code of Conduct to leave the event immediately (no refunds will be forthcoming)
    -> passing on details of the incident to the Python Software Foundation
    -> informing the police about the incident

We will provide you with a written statement of the outcome, whatever it is."""
    }
    
]


def get_code():
    """
    This function returns the code of conduct.
    """
    return CODE

def print_code():
    """This function prints the code of conduct"""
    print("This is the PyCON AFRICA Ghana 2019 Code of Conduct")
    print("---------------------------------------------------\n")
    
    for entry in CODE:
        print(Back.WHITE + Fore.BLUE + ' {} '.format(entry['category']) + Back.RESET + Fore.RESET)
        print()
        print(entry['content'])
        print()
        
        
if __name__ == "__main__":
    print_code()