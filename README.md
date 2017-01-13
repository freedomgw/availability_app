# Availability App

This availability app was built under Python 2.7, MySQL and jQuery. Several features include creating two types of users: customers and babysitters. Babysitters are able to create availabilities. Customers are able to book availabilities from different babysitters.

## Getting Started
1. Install virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
pip install virtualenv
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate

2. Install Python packages
pip install -r requirements.txt

3. Install Homebrew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

4. Install MySQL
brew install mysql

5. Start MySQL Server
mysql.server start

6. Run Migrations
mysql -u root -p < migrations/migration_001.sql
mysql -u root -p < migrations/migration_002.sql

7. Run application
python main.py

8. Visit the webpage
http://localhost:8080/login
