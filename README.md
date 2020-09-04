# Description

This program will accept a JSON file and run it through a custom JSON decoder that reverses and string fields and doubles any integer fields. 

# How to use this code

A Makefile is provided for convenience. To run the demo: 

`make run`

To cleanup the generated files:

`make cleanup`

To run tests:

`make test`

# Answers to follow-up questions

## Question 2. 

### Question

Describe how you would scale this if there were 10TBs of files, using any tool/framework available.

### Answer

Some questions I would ask include: 
1. Are the files a static dataset or is this some periodic rate of growth? 
2. What's the rate (e.g. 10TB/month or year)? 
3. Are there any processing requirements on newly generated files?

Assumptions:
 - a dynamic dataset of incoming generated JSON files growing at rate of 10TBs/year (or about 1TB/month)
 - average incoming file size is 1 MB
 - files should be processed as they are saved

We can have the files land in AWS S3 and be processed on-the-fly with a AWS Lambda function that is triggered upon the arrival of a new file. 
Given that the script is relatively simple, 1,000,000 executions (1 TB / 1 MB) of the function per month would result in very small infrastructure costs. 
After execution, the transformed data can be stored in S3 again for further manual or automated analysis. 
The cost would scale linearly with either an increasing rate of incoming files or decreasing average file size. 
A 10x movement in either of these dimensions would result in a potentially acceptable 10x increase in costs.
If there is a 10x increase in both dimensions (i.e. 10x increase in throughput to 10TB/month AND 10x decrease in average file size to 100KB), 
the costs would increase 2 orders of magnitude, in which case other solutions may become more desirable.

## Question 3.

### Question

What if, instead of saving to a file, we were to save TBs of these JSON objects to MongoDB. What would you do to make sure good software practices were followed?

### Answer

The architecture described above can be used for writing to MongoDB simply by pointing the output fo the Lambda function to a MongoDB cluster rather than S3. 
A cluster would allow for distrubuting the load of writing the new files across several nodes. 
We can size the cluster depending on the writes and other access patterns requirements.
To ensure good software practices and quality data products, I would use a test-driven approach in combination with some form of CI/CD in the steps prior to 
deployment of our Lambda function. 
In addition, I would extend the transform function to include provenance and other metadata to increase the auditability of the transformed data.
