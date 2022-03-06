# RSA_Lab
I experimented with some known RSA attacks on textbook RSA. The code is for learning purposes
and should not be used for real applications.

## How to run:

### Install the requirements
- You can install it by using `pip install -r requirements.txt`

- You also need to install Sage for Sage shell, otherwise you cannot run the Hastad Broadcast
Attack (**Hastad.py** and **test_Hastad.py**) which utilizes some Sage functionality. The Python code of Hastad will not work 
and give errors if you use the normal Python interpreter. 

- Use Python 3



### To run the Hastad test:
Open up a Sage shell and use `python -m unittest test_Hastad`

### To run the other tests:
You can simply use an IDE (I used intellij with Python plugin), and run the unit tests in the
**tests** folder