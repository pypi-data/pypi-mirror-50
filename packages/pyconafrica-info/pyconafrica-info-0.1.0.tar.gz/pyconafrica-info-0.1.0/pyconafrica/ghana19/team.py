"""
This file contains organizing team description related code.
"""
from colorama import init, Style, Fore, Back
init()

TEAM = [
    {
        'name': 'Marlene Mhangami',
        'role': 'Chair of the organising committee.',
        'bio': \
"""Marlene is a Director of the Python Software Foundation, 
         and a co-founder of ZimboPy, a Zimbabwean non-profit that 
         empowers women to pursue careers in technology.
        
         She lives in Harare and has an active role in assisting the growth of Python 
         communities locally and across Africa."""
    },
    {
        'name': 'Aaron Yankey',
        'role': 'Chair of the Python Software Community in Ghana.',
        'bio': \
"""Best known for helping make Ghana a space-faring nation, Aaron has been contributing 
         his widow's mite to the tech community for over seven years. 
         He's a member of the Python Software Foundation Grants committee and 
         helps promote Python-related activities around the globe."""
    },
    {
        'name': 'Aisha Bello',
        'role': 'Aisha is a Cloud Systems Engineer at TechData.',
        'bio': \
"""She's a former board member of the Python Nigeria Community, a Python Software Foundation fellow,
         Django Software Foundation member and winner of the 2016 Malcolm Tredinnick Memorial award.
         Aisha is passionate about mentoring African women through PyLadies and DjangoGirls.
         She's on Twitter as @AishaXBello."""
    },
    {
        'name': 'Michael Young',
        'role': 'Treasurer.',
        'bio': \
"""Michael is a professional accountant with keen interest in Data Science and Financial Inclusion.
         He is a co-founder and Executive Board member of the Python Software Community in Ghana,
         and works with students and professionals as a career mentor, educator and a community builder."""
    },
    {
        'name': 'Abigail Mesrenyame Dogbe',
        'role': '',
        'bio': \
"""Abigail is the current Lead of PyLadies Ghana, a mentorship group with a focus on helping 
         more women become active participants and leaders in the Python open-source community.

         She has been involved in organising and coaching at several Django Girls events in Ghana and 
         hopes to empower more women in the field of technology through these initiatives."""
    },
    {
        'name': 'Noah Alorwu',
        'role': 'Talks committee lead.',
        'bio': \
"""Noah is a software developer, a member of ICT4D.at and UI designer. He's a co-founder and 
         executive board member of the Python Software Community in Ghana, 
         and a member of the Django Software Foundation. Noah has been involved in the organisation 
         of several events including Django Girls & PyCon Ghana. He's on Twitter: @plasmadray  """
    },
    {
        'name': 'Mannie Young',
        'role': 'Mannie is a computer scientist, graphic designer and software developer.',
        'bio': \
"""He's also a community builder, having kick-started the initiatives and user groups under 
         the Python Software Community in Ghana. He volunteers as a mentor for people hoping 
         to get into software development and organises events and workshops around the country. 
         He's on Twitter: @mawy_7."""
    },
    {
        'name': 'Daniele Procida',
        'role': 'Daniele works at Divio and currently lives in the Netherlands.',
        'bio': \
"""He is a core developer of the Django Project and has been an active volunteer organiser 
         in the Python community for several years. In recent years he has been involved in 
         the organisation of several editions of DjangoCon Europe, PyCon UK and PyCon Namibia."""
    }    
]

def get_team():
    """
    This function returns the team of organizers
    """
    return TEAM

def print_team():
    """
    This function prints the team of organizers
    """
    print("The organizers team of PyCON Africa 2019")
    print('----------------------------------------\n')
    
    for member in TEAM:
        print(Back.YELLOW + Fore.BLACK + member['name'] + Back.RESET + Fore.RESET)
        if member['role']:
            print('    '+ Back.WHITE + Fore.BLUE + ' {}'.format(member['role'])  + Back.RESET + Fore.RESET)
        print('    Bio: {}\n'.format(member['bio']))
        
    print("\n\nLet's clap for them \U0001F44F \U0001F44F \U0001F44F")
        
        
if __name__ == "__main__":
    print_team()