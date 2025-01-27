## Purpose

Date: 4/23/2024

Group: Tech Wizards

Members: Sofia Castro, Kenneth Riles, Narek Asaturyan, Peter Abdelsayed

This document introduces details about the modules for the user-friendly and secure E-commerce game launcher program. These modules serve as building blocks that establish the state-of-the-art image that our product captures, as portrayed by the graphical user interfaces, and a complex database system that ensures a safely accessible virtual environment for many users nationwide. With the congregation of these modules, we were able to implement an efficient login/registration system, a navigable store with a transaction system, a personal library for owning games, and a settings page for each player to gain the best gaming experience.

## References 
Tkinter - Python package for building GUIs 

Tkkbootstrap - Styles Tkinter widgets and additional functionalities for GUI development

Gspread - Package for interacting with Google Cloud API

Openpyxl - Package for manipulating, managing, and displaying excel spreadsheets

Smtplib - Package for sending email to newly created user

PIL - Manages image formatting and manipulation

## Overview
1. This program implements a readable and easy to use login/registration management system. This structure utilizes data from the program’s main database to store and retrieve data on account information.
2. The next stage after a user creates a new account is the verification process. In this scenario, the program automatically sends an email to the registered accounts input email address inbox via the SMTP protocol. The user is promptly required to open the email and click on the link to verify their account before logging into the game launcher.
3. Once the user logs in, they can autonomously navigate the online game launcher store to search for, view and add games to their personal cart. After the user adds all the games they want into their cart, they can click on the “cart” widget to checkout.
4. Users have access to their own personal library of purchased games/demos, settings adjustment, and eventually their own profile page, including an “add friends” feature.

## Operation Procedure

1. To get run our software, install the "main.exe" file.
2. Then, access the directory in your system containing “main.exe” file and execute it.
3. Once the program is launched, you will be asked to log in.
4. If you have an account, log in with your credentials.
5. If not, create a new account and you will receive an email for account verification.
6. Once you are signed in, you are free to navigate the store and purchase games to add into your library.

## Examples of use

### 1. Filter games displayed on the store page
Store page has the ability to sort games shown by user preference. Currently we can change the items displayed based on the category and price range. We also have a search bar that shows games based on key characters entered into the search bar.

![Screenshot (95)](https://github.com/user-attachments/assets/3b7262b9-e339-4681-b1bc-b743cc12c038)

Figure 1.1: Category: “RPG”, Price Range $0-$100

![Screenshot (96)](https://github.com/user-attachments/assets/7b797306-2978-4f93-b79a-1536274f91ed)

Figure 1.2: Category: “Simulation”, Price Range $0-$10

![Screenshot (97)](https://github.com/user-attachments/assets/199953b5-733f-4e67-a302-793e8766b24f)

Figure 1.3: The keyword “er” is inputted in the search bar and the user’s keyboard button is entered.

### 2. Choose to purchase for myself or as a gift.
The user can determine if they want to purchase the game for themself or as a gift. If they purchase the game for themself it is immediately added to the user’s library. However, if the item is purchased as a gift the user obtains a code that can be activated by any user with an account, to be added to their library. 

![Screenshot (98)](https://github.com/user-attachments/assets/c04c133e-ea04-43ba-b4b8-d7ef0fdf3836)

Figure 2.1: The first game is chosen to be purchased “For myself” and the game beneath is chosen “As gifts”.

![Screenshot (99)](https://github.com/user-attachments/assets/e0a21fa6-5e5d-4df4-be5f-4c35d7ad4929)

Figure 2.2: Once the games are confirmed payment and billing entries are shown.

![Screenshot (100)](https://github.com/user-attachments/assets/25383b12-bf1f-49a7-9cc6-80ed4e9290ef)

Figure 2.3: Order is confirmed and a gift code is given if purchased as a gift and added to the library if purchased for this account.

![Screenshot (101)](https://github.com/user-attachments/assets/7a066e37-e7a2-43a3-a8fd-e515bcebe736)

Figure 2.4: The game is added to the library.

![Screenshot (102)](https://github.com/user-attachments/assets/72f7c171-9ed6-4dec-99f5-7b55a125e73a)

Figure 2.5: When the “Activate” button, from the store page, is pressed a window opens with an entry ready to receive a gift code. If a proper gift code is entered then the game is added to the library.
### 3. Update profile page
The user can change their personal description and update their profile picture. 

![Screenshot (103)](https://github.com/user-attachments/assets/b1964a38-7d4d-41d1-9f9a-dd2aa762acff)

Figure 3.1: When the “Upload Image” button is pressed an option to find the directory containing an image is given. 

![Screenshot (104)](https://github.com/user-attachments/assets/bc775d47-dc0d-4d45-9a62-77bcf32d297c)

Figure 3.2: About Me description is changed according to the last saved entry.


### 4. Filter games in library
The user’s library has a dynamic search bar that changes as keywords are entered. Games can also be sorted to favorite by right clicking on the selected game.

![Screenshot (105)](https://github.com/user-attachments/assets/d4c7eb36-55fe-4991-bd31-3a338f73197d)

Figure 4.1: Games are sorted by favorite.

![Screenshot (106)](https://github.com/user-attachments/assets/7b010187-1065-474f-8ee8-e0ba52c01e6c)

Figure 4.2: Games displayed changes dynamically as keywords are entered. Example given uses the keyword's “om”.
