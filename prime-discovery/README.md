To Find-new-prime-numbers
--––––––––––––––––––––––––––––





✅ STEP 1 — Open Termux

If you don’t have it installed:

Install Termux from F-Droid (NOT Play Store — Play Store version is broken).

Link: https://f-droid.org/en/packages/com.termux/



---

✅ STEP 2 — Update Termux packages

Open Termux and run:

pkg update && pkg upgrade -y

Make sure everything is up to date.


---

✅ STEP 3 — Install Python

pkg install python -y

This gives you Python 3 on the phone.


---

✅ STEP 4 — (Optional but recommended) Install SymPy

This gives you full deterministic prime checking.

pip install sympy

If this fails, don't worry — the script still works without SymPy.


---

✅ STEP 5 — Create the Python script

Create the file:

nano next_prime.py

Nano will open.

Now paste the improved script I gave you earlier.
=============================================

see code in repo for java script

=============================================

✅ STEP 6 — Save the file in nano

Inside nano:

1. Press CTRL + O


2. Press Enter


3. Press CTRL + X



Your file is saved.


---

✅ STEP 7 — Make the script executable (optional)

chmod +x next_prime.py


---

✅ STEP 8 — Run the script

Interactive mode

Just type:

python next_prime.py

Then paste your huge number (100+ digits) and press Enter.


---

Or pipe a number into it:

echo 100000000000000000000000000000000000000000000000000 | python next_prime.py


---

Or pass a number as an argument:

python next_prime.py 99999999999999999999999999999999999999999999999999999


---

📌 What you will see

The script will output:

The smallest prime larger than the number you gave it

Works with:

50-digit numbers

100-digit numbers

200-digit numbers

Even 500-digit numbers (may take longer)

