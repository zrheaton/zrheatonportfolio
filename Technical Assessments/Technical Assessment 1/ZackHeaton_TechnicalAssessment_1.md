# Question 1

 Write a Ruby or Bash script that will print usernames of all users on a Linux system
   together with their home directories. Here's some example output:

   ```
   gitlab:/home/gitlab
   nobody:/nonexistent
   .
   .
   ```
   
   Each line is a concatenation of a username, the colon
   character (`:`), and the home directory path for that username. Your script
   should output such a line for each user on the system.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Response Question 1 

# First Draft 
#!/bin/bash

output_file="/home/zrheaton/usercheck.txt"

while IFS=: read -r username _ _ _ _ homedir _; do
  echo "${username}:${homedir}"
done < /etc/passwd > "$output_file"
echo "Output stored in $output_file"

# Second draft - - See CITATION A - I got it in my mind to google how this would work with ldap rather than manual management so I have a second draft. 

#!/bin/bash

output_file="/home/zrheaton/usercheck.txt"

if command -v getent &> /dev/null; then
  getent passwd | while IFS=: read -r username _ _ _ _ homedir _; do
    echo "${username}:${homedir}"
  done > "$output_file"
else
  while IFS=: read -r username _ _ _ _ homedir _; do
    echo "${username}:${homedir}"
  done < /etc/passwd > "$output_file"
fi

echo "Output stored in $output_file"

# See Citation A. The output file was not called for in question 1 but it made question 2 easier to do because it was already done. 
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Question 2 

   Next, write a second script that:

   * Takes the full output of your first script and converts it to an MD5 hash.
   * On its first run stores the MD5 checksum into the `/var/log/current_users` file.
   * On subsequent runs, if the MD5 checksum changes, the script should add a line in
     the `/var/log/user_changes` file with the message,
     `DATE TIME changes occurred`, replacing `DATE` and `TIME` with appropriate
     values, and replaces the old MD5 checksum in `/var/log/current_users`
     file with the new MD5 checksum.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Response Question 2

# Revised Script 1 

#!/bin/bash

# Variables 
output_file="/home/zrheaton/usercheck.txt"
current_md5_file="/var/log/current_user_hash"

if command -v getent &> /dev/null; then
  getent passwd | while IFS=: read -r username _ _ _ _ homedir _; do
    echo "${username}:${homedir}"
  done > "$output_file"
else
  while IFS=: read -r username _ _ _ _ homedir _; do
    echo "${username}:${homedir}"
  done < /etc/passwd > "$output_file"
fi

current_md5=$(md5sum "$output_file" | awk '{print $1}')
echo "$current_md5" > "$current_md5_file"
echo "MD5 checksum generated and stored in $current_md5_file"
echo "Output stored in $output_file"



# Script 2

#!/bin/bash

# Variables 
output_file="/home/zrheaton/usercheck.txt"
current_md5_file="/var/log/current_user_hash"
previous_output_file="/home/zrheaton/usercheck_previous.txt"  # Store the previous version of the output file
user_changes_log="/var/log/user_changes.log"


current_md5=$(md5sum "$output_file" | awk '{print $1}')
if [ ! -f "$current_md5_file" ]; then
  echo "No previous checksum found. Please run the generation script first."
  exit 1
fi

previous_md5=$(cat "$current_md5_file")

if [ "$current_md5" != "$previous_md5" ]; then
  timestamp=$(date "+%Y-%m-%d %H:%M:%S")
  echo "$timestamp changes occurred" >> "$user_changes_log"
  echo "Changes detected:" >> "$user_changes_log"
  diff_output=$(diff "$previous_output_file" "$output_file")
  
  # This part is cited in CITATION B at the bottom. I needed help to get this part right so I could see what changed in the log. 
  if [[ -n "$diff_output" ]]; then
    echo "$diff_output" | while read -r line; do
      # Use regex to detect deleted or added users
      if [[ $line =~ ^\<.* ]]; then
        echo "User deleted: ${line#< }" >> "$user_changes_log"
      elif [[ $line =~ ^\>.* ]]; then
        echo "User added: ${line#> }" >> "$user_changes_log"
      fi
    done
  fi
  
  echo "$current_md5" > "$current_md5_file"
  cp "$output_file" "$previous_output_file"
else
  echo "No changes detected."
fi

echo "Script complete. Check the log in /var/log/user_changes.log for details."

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Question 3

   Finally, write a crontab entry that runs these scripts hourly.

   Provide both scripts and the crontab entry for the answer to be
   complete.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Response Question 3 

Crontab Entries 
0 * * * * /bin/bash /home/zrheaton/user_check_script.sh
0 * * * * /bin/bash /home/zrheaton/user_changes_logger.sh


# Script 1 - user_check_script.sh

#!/bin/bash

output_file="/home/zrheaton/usercheck.txt"

if command -v getent &> /dev/null; then
  getent passwd | while IFS=: read -r username _ _ _ _ homedir _; do
    echo "${username}:${homedir}"
  done > "$output_file"
else
  while IFS=: read -r username _ _ _ _ homedir _; do
    echo "${username}:${homedir}"
  done < /etc/passwd > "$output_file"
fi

echo "Output stored in $output_file"


# Script 2 - user_changes_logger.sh

#!/bin/bash

# Variables 
output_file="/home/zrheaton/usercheck.txt"
current_md5_file="/var/log/current_user_hash"
previous_output_file="/home/zrheaton/usercheck_previous.txt"  # Store the previous version of the output file
user_changes_log="/var/log/user_changes.log"


current_md5=$(md5sum "$output_file" | awk '{print $1}')
if [ ! -f "$current_md5_file" ]; then
  echo "No previous checksum found. Please run the generation script first."
  exit 1
fi

previous_md5=$(cat "$current_md5_file")

if [ "$current_md5" != "$previous_md5" ]; then
  timestamp=$(date "+%Y-%m-%d %H:%M:%S")
  echo "$timestamp changes occurred" >> "$user_changes_log"
  echo "Changes detected:" >> "$user_changes_log"
  diff_output=$(diff "$previous_output_file" "$output_file")
  
  # This part is cited in CITATION B at the bottom. I needed help to get this part right so I could see what changed in the log. 
  if [[ -n "$diff_output" ]]; then
    echo "$diff_output" | while read -r line; do
      # Use regex to detect deleted or added users
      if [[ $line =~ ^\<.* ]]; then
        echo "User deleted: ${line#< }" >> "$user_changes_log"
      elif [[ $line =~ ^\>.* ]]; then
        echo "User added: ${line#> }" >> "$user_changes_log"
      fi
    done
  fi
  
  echo "$current_md5" > "$current_md5_file"
  cp "$output_file" "$previous_output_file"
else
  echo "No changes detected."
fi

echo "Script complete. Check the log in /var/log/user_changes.log for details."


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 4

A user is complaining that it's taking a long time to load a page on our
   web application. In your own words, write down and discuss the possible
   cause(s) of the slowness. Also describe how you would begin to troubleshoot
   this issue?

   Keep the following information about the environment in mind:

   * The web application is written in a modern MVC web framework.
   * Application data is stored in a relational database.
   * All components (web application, web server, database) are running on a single
     Linux box with 8GB RAM, 2 CPU cores, and SSD storage with ample free space.
   * You have root access to this Linux box.

   We are interested in learning about your experience with modern web
   applications, and your ability to reason about system design and
   architectural trade-offs. There is no right or wrong answer to this
   question. Feel free to write as much or as little as you feel is necessary.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Response Question 4

The first step is to triage this issue based on set criteria to ensure we are handling this situation in a way that helps the customer. This includes finding out: 
- How long has this been happening/when did it start? 
- What is the position of the resource (is this a critical web application) 
- What is the expected speed 
- Set confidence with customer that they're in good hands and set expectations on a path forward (this means calming if it is an on-fire issue). 

The second step is to start into the technical investigation. 
- Something like a web application loading "slow" is sort of vague and subjective. I would prefer to do a live evidence/fact finding call of an hour.
 (I try to prevent fatigue by keeping it to an hour and no more...unless I have good reasonand customer buy-in). 
- As part of this fact finding I am looking for scope. A non comprehensive list to give you an idea of where my mind goes would be:  Is it one user, many users, one machine, multiple machines/access points, specific time of day or a pattern, when did it start and how was it noticed? Rule out network speeds and general connection. define acceptable speed vs current speed. Is it slow all the time or upon a certain trigger? What are system resources? In this question I'd spot that "8GB RAM, 2 CPU cores, and SSD storage with ample free space" is a oddly limited amount for a web application, web server, and database. 

- Some of the tools I'd use for this would be htop (system resources), ifconfig/netstat -ano/grep/ping/traceroute/speedtest if installed/netcat (networking), df-h (harddrive. Is something spooling?), ll -a (permissions on files). 

Pretending it is not resource limitation for the sake of expressing where I'd go with this: 

The third step would be understanding the architecture of the web application itself. Knowing it was written in an MVC framework I looked up (CITATION C) what that entails. 
- Many of the symptoms above would guide me towards which of the following to look into but here is a general overlay. 

- I now know that MVC splits into model, controller, and view. There is fetching of data four different ways between the controller and view and model. There could be connection/networking issues there.
I would be looking at how these communicate with the network tools above. If there is something off I might try to pull a wireshark. Even though it's all on one machine it would have to loopback to itself. On the deepest levels we could possibly see what observability tools are available like Datadog or Dynatrace. Jaeger has a free plan you could possibly use. 


- The MVC shows that it is the model that will pull from the database is what pulls from the database so we could look into that. Is it a query optimization thing, is the database online and functional, or something getting in the way of the database not communicating, is it user permissions? Something that gets in the way of the database taking a long time to load something. 

We could use a profiler like the one included with SQL or Oracle or Solarwinds. This would highlight slow queries. 

- When it comes to a web application running slow the best metaphor is that the data has a path like a garden hose and either there is a kink or water is spooliong somewhere (like a permission taking a long time to process or a query taking extra time).   


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Question 5

The Git commit graph below shows the output of `git log --all --decorate --oneline --graph`. What sequence of Git commands would result in this commit graph when starting from an empty directory?

```
* 3ceaba9 (HEAD -> master) fourth commit
*   6b5b81f Merge
|\
| * 9f22672 (feature-branch) awesome feature
* | 572982b third commit
|/
* 87acf21 second commit
* 5662bb5 first commit
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Response Question 5

The commands that would would result in this graph when starting from an empty directory are: 

echo "data" > project.txt (this creates the file with changes on the local machine)
git project.txt (this stages the file so git knows it's ready to be uploaded)
git commit -m "whatever comment you want" (this is what actually makes the commit to the local respository or online one like github)

This process happens a few times. 

Another important series would be

git checkout -b "name of branch" (this allows you to create a new branch or an area/copy of the same code that you can modify in a non-live environment and push when confident). 

git merge feature-branch (this is how the changes in your copy/branch code go live into the repository that is shared). 

Specifically in this order I would think the commands looked something like this: 

git init
echo "first" > file.txt
git add file.txt
git commit -m "first commit"

echo "second" >> file.txt
git add file.txt
git commit -m "second commit"

echo "third" >> file.txt
git add file.txt
git commit -m "third commit"

git checkout -b feature-branch
echo "awesome feature" >> file.txt
git add file.txt
git commit -m "awesome feature"

git checkout master
echo "fourth" >> file.txt
git add file.txt
git commit -m "fourth commit"

git merge feature-branch


# CITATION D
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Question 6

XXXXXX has hired you to write a Git tutorial for beginners on this topic:

   **Using Git to implement a new feature/change without affecting the main branch**
   
   In your own words, write a tutorial/blog explaining things in a beginner-friendly way. 
   Make sure to address both the "why" and "how" for each Git command you use.  Assume 
   the audience are readers of a well known blog.

   (**Note**: This is just a scenario for you to demonstrate your written skills and ability to explain technical topics. We are not using these assessments for anything other than the recruitment process.)

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Response Question 6

Is your team collaborating as effectively as possible? GIT can take you to a new level! 

Git is a product that allows your team to move from siloed to robust collaboration with minimal change. Git is a code management system where a central "repository" (area that code is stored) is accessible, visible, and manageable with anyone based on their assigned permissions. 

At the center of of the project we start at the master branch. Imagine a whiteboard in the center of an office that holds all the code for a project. Perhaps envision this as a monitor displaying live code that is being used in your product. 

Connected to the master branch are a limitless number of other branches that can be named anything appropriate to the workflow. An engineer can create a new branch of "checkout" any branch including the master for work in their own area on their own time. The provided flexibility leads to better results given the opportunity to think. 

When an engineer has completed their work on any branch they can use the "commit" function which sends their code changes into the shared repository. This might be the master branch if the code is ready for a production environment but it might also be a testing environment separate from the master branch. 

Are you nervous about your application crashing due to coding mistakes? That's valid. Git offers a lot of advanced features to track, maintain accountability, and revert changes made in error. It can be computationally connected to standard operating procedures (SOPs) where a code change might require leadership or senior level approval. This allows safety rails while not impeding the work of individual contributors. 


 such as BLAME and Code Validation as advanced features to ensure that the "pushes" or "commits" follow a chain of authority. Master branch commits can be modelled on a standard operating procedure to ensure only the finest changes are pushed! If a mistake is made, it can be identified quickly and resolved. 

A general outline to accomplish the above can be done with the following commands: 

git checkout main: Switches to the main branch.
git pull origin main: Pulls any new changes from the remote repository (GitLab, GitHub, etc.) into your local branch, so you're working with the latest code.
git checkout -b new-feature: Creates and switches to a new branch called new-feature.
git add .: Stages all the changes in your working directory.
git commit -m "Added new feature": Commits the staged changes with a descriptive message.
git push origin new-feature: Pushes your new-feature branch to the remote repository.

More comprehensive documentation for the above process and others can be found at: https://docs.gitlab.com/ee/topics/git/index.html. 

If you are interested in the accountability advanced features you might start your search at: https://docs.gitlab.com/ee/user/project/repository/files/git_history.html OR https://docs.gitlab.com/ee/topics/git/undo.html

Find other great tutortials at: https://docs.gitlab.com/ee/topics/git/

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Question 7

What is a technical book/blog/course/etc. you experienced recently or in the past that you enjoyed?  

Please include:
 - A link or reference so we know what you are talking about.
 - A brief review of what you especially liked or didnt like about it.


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Response Question 7

I recently purchased Quickstart Guides for Python by Robert Oliver and SQL by Walter Shields. I've already had significant experience in both of these skills from the professional and they caught my eye on Instagram while scrolling. I purchased them really to check them out but as I started reading through them they are possibly the best resource I've ever worked with to understand. The authors do a fantastic job of assuming the reader knows nothing but organizing the content into logical sections for developed professionals. I think a side bonus is also the size of the books and the spiral style. They're the perfect size for learning and for a quick reference at my desk if I need it!

https://www.quickstartguides.com/collections/bundles/products/programming-quickstart-guides-bundle

Please include:
 - A link or reference so we know what you are talking about.
 - A brief review of what you especially liked or didnt like about it.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


CITATIONS

# CITATION A: 

Googled: find usernames ldap linux
Found: First link, https://superuser.com/questions/376838/how-to-get-linux-users-list-from-ldap


# CITATION B: 

Googled "regex to compare two strings bash"
Found: https://www.reddit.com/r/bash/comments/sai0nk/compare_two_strings/
New Google: "if [[ $line =~ ^\<.* ]]"
Found: https://stackoverflow.com/questions/21858164/bash-if-line-begins-with

Went to ChatGPT 4o. 

Prompt: I am writing a bash script where the goal is to identify changes in a particular file that I have a hash generated for. I've got most of it done as you can see but I just need help with the regex syntax and logic to detect when there is and is not a change. Take a look at what I have so far:

#!/bin/bash

# Variables 
output_file="/home/zrheaton/usercheck.txt"
current_md5_file="/var/log/current_user_hash"
previous_output_file="/home/zrheaton/usercheck_previous.txt"  # Store the previous version of the output file
user_changes_log="/var/log/user_changes.log"


current_md5=$(md5sum "$output_file" | awk '{print $1}')
if [ ! -f "$current_md5_file" ]; then
  echo "No previous checksum found. Please run the generation script first."
  exit 1
fi

previous_md5=$(cat "$current_md5_file")

if [ "$current_md5" != "$previous_md5" ]; then
  timestamp=$(date "+%Y-%m-%d %H:%M:%S")
  echo "$timestamp changes occurred" >> "$user_changes_log"
  echo "Changes detected:" >> "$user_changes_log"
  diff_output=$(diff "$previous_output_file" "$output_file")

------

Based on some googling I found a string that looks like this "if [[ $line =~ ^\<.* ]]"

I get the .* in regex but the rest I'm not sure of beyond line = ...why escape character? 

What would the logic look like for an if/else loop?


# CITATION C
https://www.geeksforgeeks.org/mvc-framework-introduction/

# CITATION D
https://docs.gitlab.com/ee/topics/git/commands.html