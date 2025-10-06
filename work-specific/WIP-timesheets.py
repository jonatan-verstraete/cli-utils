import subprocess, os


cmd_prs='''git log --since="8am" --pretty=format:"%s" | grep -Eo '(BUG|FT|US)[-/]?[0-9]+' | sort | uniq'''
# subprocess.run()


if __name__:
    all_tickets=[]
    base_path = os.path.expanduser("~/Documents/Github")

    # gets all repo names
    repos = [name for name in os.listdir(base_path) if 'bricsys' in name]
    for repo in repos:
        # enter the repo  
       os.chdir(f"{base_path}/{repo}")
       # get the history of all FT/US/BUG prefixed tickets and push these to the master-array
       output = subprocess.run(
            cmd_prs, 
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).stdout.decode('ascii').split("\n")
       
       ticketNumbers =[name for name in output if len(name)]
       if ticketNumbers:
            all_tickets.extend(ticketNumbers)
           
    print(all_tickets)

    # paths = os.path.expanduser(f"~/Documents/Github")