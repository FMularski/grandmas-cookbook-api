# Grandma's Cookbook API
![GitHub repo size](https://img.shields.io/github/repo-size/FMularski/thebitbybit-recruitment)
![GitHub last commit](https://img.shields.io/github/last-commit/FMularski/thebitbybit-recruitment?color=yellow)
![GitHub top language](https://img.shields.io/github/languages/top/FMularski/thebitbybit-recruitment?color=purple)

## 🍳 Created with
* Django 4.2
* Django Rest Framework 3.14.0
* drf-yasg 1.21.5
* Postrges
* Nginx
* Docker

## 🍳 About
Grandma's Cookbook is an API project allowing to browse and manage food recipes. The project itself consists of three docker containers being: the web application, a relational database and a reverse proxy server for serving the static content. The app was created as a recruitment task.

## 🍳 Core features
* User authentication (JWT)
* Getting list of all existing recipes
* Getting a particular recipe by its id
* Creating new recipes (superusers only)
* Updating existing recipes (superusers or objects' creators only)
* Deleting recipes
* Browsing recipes added to users' cookbooks
* Browsing objects with django admin panel

## 🍳 Launching and usage

* Download the project to your local machine
```bash
git clone https://github.com/FMularski/thebitbybit-recruitment.git
```
* Start the project with docker
```bash
docker compose up
```
During the booting up the database is migrated and sample data is populated, such as users and cooking recipes.
* Open the app in your browser at
```bash
http://localhost:80
```
* Have fun with the project by interacting with the provided open API or use any other client of your choice. You can also go to the admin panel to inspect existing objects.
```bash
http://localhost/admin
```
SU credentials:
email: admin@mail.com
password: admin

## 🍳 Testing
The code can be tested by executing in the web app container:
```bash
pytest
```
or (if you want some extra coverage info):
```bash
pytest --cov=cookbooks/tests/
```
