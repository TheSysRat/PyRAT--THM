# PyRAT--THM
Solution for ROOT access in challange TryHAckMe - PyRAT 

# Usage >>

```
git clone https://github.com/TheSysRat/PyRAT--THM
cd PyRAT--THM

python3 command_brute.py -l <IP> -p 8000 -e <command_dictionary>
NOTE: Good choose is common.txt

python3 password_brute.py -l <IP> -p 8000 -w <password_dictionary> -t <nr_of_threads>
NOTE: Good choose is rockyou.txt or 500-worst-passwords.txt 

```
