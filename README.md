# mongo_load_record

Problem statement: create a class to implement insert , update and delete in Mongo using python .


Imports:
pymongo: a module to allow python interact with mysql database.
logging module: to log all activities: errors and processes to help with debugging.
In production print is prohibited, so logging. comes into the picture to see processes you would usually print on screen.
Exception handling: try and catch to ensure the code continues to run even though a section raises an error.
decouple.config: To load login and password from a .env file.


Workflow:
1. Creating a database class with the following properties:
  a. insert method: populate database table with records fetched from file.
  b. update method: update record in the document(update_one)
  c. delete method: delete record from document(delete_one)
  
2. Create 2 functions:
  a. read_file: To read date from a file and return result as a tuple( head, body).
    constraints:
    i. since mysql insert takes a tuple or list of tuples, it is important to use readlines()
    to get the output as a list: where each line is an element(str) of the list.
    ii. The elements(str) where converted to list using the split method for easy extraction , since 
    each value corresponded to a column value.
    iii. The header was extracted using pop method of a list which returns the removed item that was later stored as the head variable.
    iv. coverted the remaining list to list of tuples to match Mysql data insert format.
   b.convert_dtype: To convert string type values to float and int as the values of the data were numerical
   c. list_of_dict: To convert header into keys and body into values.
   creating a list of dictionaries from the records. Data reuirement for MongoDb insertion
    constraints:
      i. To access each element 2 for loops were created, one to access each tuple in the list
      and the second one to access each element in the tuple.
      ii. After that, each element was type casted to meet the requirement of the data.
      
   Procedural code:
   Initiating the class and calling each class methods.
   calling read_file and convert_dtypes functions.
   inserting, updating and deleting class methods.
   
