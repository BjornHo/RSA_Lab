# RSA_Lab
I experimented with some known RSA attacks. The code is for learning purposes
and should not be used for real applications.

### Implemented activities
- RSA
- Common Modulus Attack
- Hastad Broadcast Attack
- Franklin-Reiter Related Message Attack
- Experiments for Hastad and Franklin-Reiter attacks

## How to run:

### Install the requirements
- You can install it by using `pip install -r requirements.txt`

- You also need to install Sage for Sage shell, otherwise you cannot run the Hastad Broadcast
Attack or the Franklin-Reiter Related Message Attack which utilizes some Sage functionality. The Python code will not work 
and give errors if you use the normal Python interpreter. 

- Use Python 3

### To run the Hastad test:
- For simple form: open up a Sage shell, `cd tests` and use `python3 -m unittest test_Hastad_Simple.py`
- For generalized form: open up a Sage shell `cd tests` and use `python3 -m unittest test_Hastad.py`

### To run the Franklin-Reiter test:
Open up a Sage shell `cd tests` and use `python3 -m unittest test_Franklin_Reiter.py`

### To run the other tests:
You can simply use an IDE that supports Python (I used intellij with Python plugin), and run the unit tests in the
`tests` folder