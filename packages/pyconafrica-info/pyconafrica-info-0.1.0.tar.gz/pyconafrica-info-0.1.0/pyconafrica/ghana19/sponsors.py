"""
This file contains sponsors information
"""
from colorama import init, Style, Back, Fore
init()

SPONSORS = [
    {
        'type': 'Diamond',
        'list':[
            {
                'name': 'Python Software Foundation',
                'url': 'https://www.python.org/psf'
            },
            {
                'name': 'BriteCore',
                'url': 'http://britecore.com/'
            },
            {
                'name': 'Andela',
                'url': 'http://andela.com/'
            },
            {
                'name': 'Django Society UK',
                'url': ''
            }
        ]
    },
    {
        'type': 'Gold',
        'list':[
            {
                'name': 'django',
                'url': 'https://www.djangoproject.com/fundraising/'
            },
            {
                'name': 'django danmark',
                'url': 'https://django-denmark.org/'
            },
            {
                'name': 'NEXMO',
                'url': 'https://developer.nexmo.com/'
            },
            {
                'name': 'Django Events Foundation',
                'url': 'https://www.defna.org/'
            }
        ]
    },
    {
        'type': 'Bronze',
        'list': [
            {
                'name': 'Go Fund Me',
                'url': 'https://www.gofundme.com/f/pycon-africa-financial-assistance'
            },
            {
                'name': 'Python Academy',
                'url': 'https://www.python-academy.com/'
            },
            {
                'name': 'Real Python',
                'url': 'https://realpython.com/'
            },
            {
                'name': 'Aktech Labs',
                'url': 'https://aktechlabs.com/'
            },
            {
                'name': 'SikiLabs',
                'url': 'https://sikilabs.com/'
            },
            {
                'name': 'Torchbox',
                'url': 'https://www.torchbox.com/'
            },
            {
                'name': 'Read the docs',
                'url': 'https://readthedocs.org/'
            },
            {
                'name': 'Wildfish',
                'url': 'https://wildfish.com/'
            },
            {
                'name': 'Caktus Group',
                'url': 'https://caktusgroup.com/'
            },
            {
                'name': 'Weekly Python Exercise',
                'url': 'http://weeklypythonexercise.com/'
            }
        ]
    },
    {
        'type': 'Special',
        'list': [
            {
                'name': 'ICT4D.at',
                'url': 'https://ict4d.at/'
            }
        ]
    }
]


def get_sponsors():
    """
    This function returns the sponsors
    """
    return SPONSORS

def print_sponsors():
    """
    This function print the sponsors
    """
    print("Here are the sponsors list of PyCON Africa 2019")
    print('-----------------------------------------------\n')
    
    for cat in SPONSORS:
        print(Back.YELLOW + Fore.BLACK + '{} Sponsors'.format(cat['type']) + Back.RESET + Fore.RESET + "\n")
        
        for spon in cat['list']:
            print('    ' + Back.WHITE + Fore.BLUE + ' {} '.format(spon['name']) + Back.RESET + Fore.RESET)
            print('    Url: {}\n'.format(spon['url']))
            
        print('\n')
        
        
if __name__ == "__main__":
    print_sponsors()