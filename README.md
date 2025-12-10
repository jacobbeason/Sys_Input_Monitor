# Description 
This program asks the user for consent to begin logging, logs keystrokes using pynput and saves them to a txt file called keylog.txt, then, using SMTP, sends the file to an email address specified by the user on a desired time interval.
This program was created for solely educational purposes to gain a deeper understanding of how keylogging could be used by attackers to harvest sensitve data from vunerable systems and how SMTP can be automated.


# Requirements 
pynput

# Installation
1. Clone the repository:
  https://github.com/sprsrr/Sys_Input_Monitor.git
2. Create Virtual Environment :
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install pynput:
  pip install pynput


