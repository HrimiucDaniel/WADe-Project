@echo off

start /B python "Dynamic Page Service\main.py"
start /B python "User\controller.py"
start /B python "Guided Tour Service\main.py"
cd "Dynamic Page Service"