# Final-Project - Hand write recognition #
==========================================
Operating Instructions:
======================
All the files needed to run the Python files in the project are fully present.
Here is a brief explanation of each file:
* dal.py - Data access layer.
* extended_model.py - Contains the logic of extended algorithm.
* shrinking_model.py - Contains the logic of shrinking algorithm.
* multiplication_model.py - Contains the logic of multiplication algorithm.
* matrix_manipulate.py - Contains two functions:
                                                1. Convert image to matrix.
                                                2. Lowering the irrelevant margin from the matrix
* unit_test.py - Basic test file for each model.
* LoadMNIST.py - A program to load the MNIST photo set according to the different models.
                 Currently the program loads images for all models.
* TestMNIST.py - A program to Test the MNIST photo set according to the different models.
                 Currently the program test images for selected model passing as CLI argument.
* LoadMNIST_0_1.py - A program to load just photos of 0 and 1 according to the different models.
                     Currently the program loads images for all models.
* TestMNIST_0_1.py - A program to Test just photos of 0 and 1 according to the different models.
                     Currently the program test images for selected model passing as CLI argument.
* program.py -  A small application that enables manual writing of the literature,
                study of the machine and examination of the machine.

Database:
=========
Use MYSQL.
Create user named "admin"
Add password "123456"
Create database called "hand_write_recognition".
Create the following tables for each model:
- CREATE TABLE shrinking_model (pattern VARCHAR(50), digit VARCHAR(1));
- CREATE TABLE extended_model (pattern VARCHAR(100), digit VARCHAR(1));
- CREATE TABLE multiplication_model (pattern VARCHAR(50), digit VARCHAR(1));

- CREATE TABLE one_zero_shrinking (pattern VARCHAR(50), digit VARCHAR(1));
- CREATE TABLE one_zero_extended (pattern VARCHAR(100), digit VARCHAR(1));
- CREATE TABLE one_zero_multiplication (pattern VARCHAR(50), digit VARCHAR(1));

For each table define index as following:
- ALTER TABLE <-- fill in model name --> ADD INDEX (pattern);

-- Your database is now ready!! --

MNIST Dataset:
==============
Put the MNIST Dataset in the following path:
C:\\Users\\<-- fill in user name -->\\PycharmProjects\\Final-Project\\samples\\train-images.idx3-ubyte