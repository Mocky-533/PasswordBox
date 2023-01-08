# Password Box

A very simple password management box, where you can add, edit and search your passwords.

On first launch, a login password(key) is required. Every time after that, just simply input the particular password(key) to get access to the box.

## Functions

1. Add password
    - Offer a chance to update password when the one being added is duplicated.(site and account simultaneously)
2. Search password by either app/site name or account/email
    - Chosen password can be copied into clipboard. (v1.01)
3. Update stored password
4. Delete stored password
5. change login password(key)
    - add verification before changing login key. (v1.01)

## Usage

1. Install requirements

    `pip install -r requirements.txt`

2. Launch it

    `python interface.py`

## Notification

- Before launching, make sure the terminal running contains at least 30 lines and 110 cols, or the curses package might run into error due to the lack of space on the screen.

## To do

- [x] ~~A GUI (maybe)~~ Used cursor instead.
- [x] ~~Optimize searching functions~~ DONE.
- [x] ~~use cursers pad to display search result, so that the error of not enough room can be dodged.~~

## Ending

This repo was just a project to try database operation and python-curses functions.

And this might just be it. Probably I will no longer work on this mini project. Anyone is welcomed to do anything with it, have fun~
