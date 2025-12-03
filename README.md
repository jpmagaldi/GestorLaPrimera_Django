# GestorLaPrimera_Django

Initial Project for Web-Based Management and Invoicing System this is an initial project aimed at unifying all the phases of the company's current management and invoicing software into a web-based platform.

The initial idea is to use the same database currently used by the company. For now, HTML is being used for the frontend, but it could be replaced with a more robust framework if the client or situation requires it.

Important: The Ui is in spanish.


## Features:

-  ### Invoice:
    - Can already connect to ARCA servers to request the latest issued invoice \
    (for security reasons, the .crt and .key files that go in the "cert" folder have been removed)
    - Clients and products can be searched directly from the web interface (via AJAX calls)
    - When products are selected, the system also calculates TAX and the total amount
    - Can change price and quantity (with correspondingly validators) for every selected product
    - Electronic invoices can be issued directly from the application, with CAE and CAE Vto.

- ### CRUD:
    - Can change everything from clients.
    - Can communicate with ARCA servers, for validate CUIT number
    - Can change everything from suppliers. (Work in progress)

- ### Interface:
    - Admin interface is completely functional.

- ### Reports:
    - Invoices can search by date, client or both with respective invoice details
    - Work in progress

- ### Errors handling (with respective menssage error):
    - Can't duplicate client CUIT
    - If CUIT is invalidate (error in ARCA servers), can't create client
    - If can't connect with ARCA servers, user can't generate invoice



### Instructions:
Follow these steps to set up and run the Django project locally:
- Clone the repository
```
git clone https://github.com/jpmagaldi/GestorLaPrimera_Django.git
cd GestorLaPrimera_Django
```
- Install dependencies
```
pip install -r requirements.txt
```
- Apply migrations
```
python manage.py migrate
```
When apply migrations, you have a initial data in database, and admin account (user:admin, pw:1234)

- Run the development server
```
python manage.py runserver
```
Then visit https://localhost:8000 in your browser.


### Images (Reminder: everything is still in progress):

![](https://i.imgur.com/uIpcFQj.png)

![](https://i.imgur.com/VmQH0fP.png)

![](https://i.imgur.com/dqw5JcV.png)

![](https://i.imgur.com/dFI08xA.png)

![](https://i.imgur.com/2F6BacL.png)

![](https://i.imgur.com/Khl51oY.png)

![](https://i.imgur.com/daQvsew.png)

![](https://i.imgur.com/6I4MZoA.png)

![](https://i.imgur.com/7bAfk7E.png)

## License
[MIT](https://choosealicense.com/licenses/mit/)
