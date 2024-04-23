from schmema import schemas as s, schemasArguments as sa
import psycopg2


def exec_query(query):
    try:
        establishConnection = psycopg2.connect(dbname="postgres",user="postgres",password="password",host="localhost")
        cursor = establishConnection.cursor()
        cursor.execute(query)
        first_word = query.split()[0].upper()
        if first_word in ["DELETE", "INSERT", "UPDATE"]:
            establishConnection.commit()
            establishConnection.close()
            print("Successful operation")
        else:
            values = cursor.fetchall()
            establishConnection.close()
            for value in values:
                print(f"{value}\n")
            print("Successful operation")
    except psycopg2.DatabaseError as e:
        print(f"ALERT ERROR ALERT : {e}")

def welcome_interface(isTransaction = False):
    print(
        """
        Welcome to the Database CLI Interface!
        Please select an option:
        1. Insert Data
        2. Delete Data
        3. Update Data
        4. Search Data
        5. Aggregate Functions
        6. Sorting
        7. Joins
        8. Grouping
        9. Subqueries
        10. Transactions
        11. Error Handling
        12. Exit
        """
    )
    userResponse = int(input("Enter your choice (1-12): "))
    while userResponse not in range(1,13):
        userResponse = int(input("Your choice must be between (1-12): "))
    if userResponse == 1:
        if isTransaction:
            return insert_data(True)
        else:
            insert_data()
    elif userResponse == 2:
        if isTransaction:
            return delete_data(True)
        else:
            delete_data()
    elif userResponse == 3:
        if isTransaction:
            return update_data(True)
        else:
            update_data()
    elif userResponse == 4:
        if isTransaction:
            return search_data(True)
        else:
            search_data()
    elif userResponse == 5:
        if isTransaction:
            return aggregate_data(True)
        else:
            aggregate_data()
    elif userResponse == 6:
        if isTransaction:
            return sorting(True)
        else:
            sorting()
    elif userResponse == 7:
        if isTransaction:
            return joins(True)
        else:
            joins()
    elif userResponse == 8:
        if isTransaction:
            return grouping(True)
        else:
            grouping()
    elif userResponse == 9:
        if isTransaction:
            return subqueries(True)
        else:
            subqueries()
    elif userResponse == 10:
        if isTransaction:
            print("Transaction already under way, select another operation")
            welcome_interface(False)
        else:
            transactions()
    elif userResponse == 11:
        error_handling()
    elif userResponse == 12:
        print("Thank you for using the Database CLI Interface")
def insert_data(isSubquery = False):
    #tableName,values
    values = []
    print("Please select the table that you would like to insert into: ")
    for index, key in enumerate(sa.keys()):
        print(f"{index+1}. {key[0:len(key)-1]}")
    choice = int(input("Please input the number of your choice: ")) - 1
    while choice not in range(len(list(sa.keys()))):
        choice = int(input("Please input a valid choice: ")) - 1
    for param in sa[list(sa.keys())[choice]]:
        value = input(f"Please enter a value for {param}: ")
        values.append(value)
    try:
        if not isSubquery:
            insert_data_executor(list(sa.keys())[choice],values)
            return
        else:
            valuesToString = "".join([f"\'{i}\'," for i in values[0:len(values)-1]] + [f"\'{values[-1]}\'"])
            return f"INSERT INTO {s[list(sa.keys())[choice]]} VALUES ({valuesToString})"
    except:
        print("Issue inserting data")
def delete_data(isSubquery = False):
    print("Please select the table that you would like to delete from: ")
    for index, key in enumerate(sa.keys()):
        print(f"{index+1}. {key[0:len(key)-1]}")
    choice = int(input("Please input the number of your choice: ")) -1
    while choice not in range(len(list(sa.keys()))):
        choice = int(input("Please input a valid choice: ")) - 1
    condition = input(f"What condition would you like to apply given schema {s[list(s.keys())[choice]]}: ")
    if not isSubquery:
        delete_data_executor(list(sa.keys())[choice],condition)
        return
    else:
        return f"DELETE FROM {list(sa.keys())[choice]} WHERE {condition}"

def update_data(isSubquery = False):
    #User must use qoutes around strings in condition
    print("Please select the table that you would like to update from: ")
    for index, key in enumerate(sa.keys()):
        print(f"{index+1}. {key[0:len(key)-1]}")
    choice = int(input("Please input the number of your choice: ")) -1
    while choice not in range(len(list(sa.keys()))):
        choice = int(input("Please input a valid choice: ")) - 14
    print("For Column: ")
    chosen = list(sa.keys())[choice]
    for index, c in enumerate(sa[chosen]):
        print(f"{index+1}: {c}")
    columnNUM = int(input("Which column would you like to modify: ")) -1
    column = sa[chosen][columnNUM]
    newValue = input("Enter the new value you want to be assigned: ")
    condition = input(f"What condition would you like to apply given schema {s[list(s.keys())[choice]]}: ")
    if not isSubquery:
        update_data_executor(chosen,column,newValue,condition)
        return
    else:
        return f"UPDATE {chosen} SET {column} = \'{newValue}\' WHERE {condition}"

def search_data(isSubquery = False):
    #tableName,condition
    print("Please select the table that you would like to search from: ")
    for index, key in enumerate(sa.keys()):
        print(f"{index+1}. {key[0:len(key)-1]}")
    choice = int(input("Please input the number of your choice: ")) - 1
    while choice not in range(len(list(sa.keys()))):
        choice = int(input("Please input a valid choice: ")) - 1
    chosen = list(sa.keys())[choice]
    print("Which columns would you like to select: ")
    for index, c in enumerate(sa[chosen]):
        print(f"{index+1}: {c}")
    print(f"{len(sa[chosen])+1}: All Columns")
    cols = str(input("Please enter columns as a comma seperated list. ie 1,2,3: "))
    if len(cols) == 1 and cols == str(len(sa[chosen])+1):
        condition = input(f"What condition would you like to apply given schema {s[list(s.keys())[choice]]}: ")
        if not isSubquery:
            search_data_executor(chosen,condition,"*")
            return
        else:
            return f"SELECT * FROM {chosen} WHERE {condition}"
    else:
        condition = input(f"What condition would you like to apply given schema {s[list(s.keys())[choice]]}: ")
        inter = [sa[chosen][int(i)-1] for i in cols.split(",")]
        columns = ",".join(inter)
        if not isSubquery:
            search_data_executor(chosen,condition,columns)
            return
        else:
            return f"SELECT {columns} FROM {chosen} WHERE {condition}"

def aggregate_data(isSubquery = False):
    #tablesName,column,calculationType
    print("Please select the table that you would like to aggregate from: ")
    for index, key in enumerate(sa.keys()):
        print(f"{index+1}. {key[0:len(key)-1]}")
    choice = int(input("Please input the number of your choice: ")) -1
    while choice not in range(len(list(sa.keys()))):
        choice = int(input("Please input a valid choice: ")) -1
    print("For Column: ")
    chosen = list(sa.keys())[choice]
    for index, c in enumerate(sa[chosen]):
        print(f"{index+1}: {c}")
    columnNUM = int(input("Which column would you like to apply an aggregate on: ")) -1
    column = sa[chosen][columnNUM]
    possibleAggregations = ["SUM","AVG","COUNT","MIN","MAX"]
    print("Which type of aggregation would you like to use: ")
    for index, agg in enumerate(possibleAggregations):
        print(f"{index+1}.{agg}")
    aggy = possibleAggregations[int(input("Select a number: "))-1]
    if not isSubquery:
        aggregate_functions_executor(chosen,column,aggy)
        return
    else:
        return f"SELECT {aggy}({column}) FROM {chosen}"

def sorting(isSubquery = False):
    #tableName,column,sortBy
    print("Please select the table that you would like to sort from: ")
    for index, key in enumerate(sa.keys()):
        print(f"{index+1}. {key[0:len(key)-1]}")
    choice = int(input("Please input the number of your choice: ")) - 1
    while choice not in range(len(list(sa.keys()))):
        choice = int(input("Please input a valid choice: ")) - 1
    print("For Column: ")
    chosen = list(sa.keys())[choice]
    for index, c in enumerate(sa[chosen]):
        print(f"{index+1}: {c}")
    columnNUM = int(input("Which column would you like to apply sort on: ")) -1
    column = sa[chosen][columnNUM]
    possibleOrderings = ["ASC","DESC"]
    print("Which type of ordering would you like to use: ")
    for index, agg in enumerate(possibleOrderings):
        print(f"{index+1}.{agg}")
    sorty = possibleOrderings[int(input("Select a number: "))-1]
    if not isSubquery:
        sorting_executor(chosen,column,sorty)
        return
    else:
        return f"SELECT * FROM {chosen} ORDER BY {column} {sorty}"

def joins(isSubquery = False):
    #table1,table2,key1,key2
    print("Please select the first table that you would like to join: ")
    for index, key in enumerate(sa.keys()):
        print(f"{index+1}. {key[0:len(key)-1]}")
    choice = int(input("Please input the number of your choice: ")) - 1
    while choice not in range(len(list(sa.keys()))):
        choice = int(input("Please input a valid choice: ")) - 1
    print("Please select the second table that you would like to join: ")
    for index, key in enumerate(sa.keys()):
        print(f"{index+1}. {key[0:len(key)-1]}")
    choice2 = int(input("Please input the number of your choice: ")) - 1
    while choice2 not in range(len(list(sa.keys()))):
        choice2 = int(input("Please input a valid choice: ")) - 1
    print("Which Column would you like to use as a key in table 1: ")
    chosen = list(sa.keys())[choice]
    for index, c in enumerate(sa[chosen]):
        print(f"{index+1}: {c}")
    columnNUM = int(input("Enter Column: ")) -1
    column = sa[chosen][columnNUM]
    print("Which Column would you like to use as a key in table 2: ")
    chosen2 = list(sa.keys())[choice2]
    for index, c in enumerate(sa[chosen2]):
        print(f"{index+1}: {c}")
    columnNUM2 = int(input("Enter Column: ")) -1
    column2 = sa[chosen2][columnNUM2]
    if not isSubquery:
        joins_executor(chosen,chosen2,column,column2)
        return
    else:
        return f"SELECT * FROM {chosen} INNER JOIN {chosen2} ON {chosen}.{column} = {chosen2}.{column2}"

def grouping(isSubquery = False):
    #column1,tableName,column2
    print("Please select the table that you want to group from: ")
    for index, key in enumerate(sa.keys()):
        print(f"{index+1}. {key[0:len(key)-1]}")
    choice = int(input("Please input the number of your choice: ")) - 1
    while choice not in range(len(list(sa.keys()))):
        choice = int(input("Please input a valid choice: ")) - 1
    print("For Column: ")
    chosen = list(sa.keys())[choice]
    for index, c in enumerate(sa[chosen]):
        print(f"{index+1}: {c}")
    columnNUM = int(input("Which column would you like to group by: ")) -1
    column = sa[chosen][columnNUM]
    if not isSubquery:
        grouping_executor(column,chosen)
        return
    else:
        return f"SELECT {column}, COUNT(*) FROM {chosen} GROUP BY {column}"
def subqueries(isSubquery = False):
    print(
        """
        What would you like the outer query to be:
        Please select an option:
        1. Insert Data
        2. Delete Data
        3. Update Data
        4. Search Data
        5. Aggregate Functions
        6. Sorting
        7. Joins
        8. Grouping
        """
    )
    userResponse = int(input("Enter your choice (1-8): "))
    outer_query = ""
    while userResponse not in range(1,9):
        userResponse = int(input("Your choice must be between (1-8): "))
    if userResponse == 1:
        outer_query = insert_data(True)
    elif userResponse == 2:
        outer_query = delete_data(True)
    elif userResponse == 3:
        outer_query = update_data(True)
    elif userResponse == 4:
        outer_query = search_data(True)
    elif userResponse == 5:
        outer_query = aggregate_data(True)
    elif userResponse == 6:
        outer_query = sorting(True)
    elif userResponse == 7:
        outer_query = joins(True)
    elif userResponse == 8:
        outer_query = grouping(True)
    print(
            """
            What would you like the inner query to be 
            Please select an option:
            1. Insert Data
            2. Delete Data
            3. Update Data
            4. Search Data
            5. Aggregate Functions
            6. Sorting
            7. Joins
            8. Grouping
            9. Subquery
            """
        )
    userResponse = int(input("Enter your choice (1-9): "))
    inner_query = ""
    while userResponse not in range(1,10):
        userResponse = int(input("Your choice must be between (1-9): "))
    if userResponse == 1:
        inner_query = insert_data(True)
    elif userResponse == 2:
        inner_query = delete_data(True)
    elif userResponse == 3:
        inner_query = update_data(True)
    elif userResponse == 4:
        inner_query = search_data(True)
    elif userResponse == 5:
        inner_query = aggregate_data(True)
    elif userResponse == 6:
        inner_query = sorting(True)
    elif userResponse == 7:
        inner_query = joins(True)
    elif userResponse == 8:
        inner_query = grouping(True)
    elif userResponse == 9:
        inner_query = subqueries(True)
    if not isSubquery:
        subqueries_executor(outer_query,inner_query)
        return
    else:
        return f"{outer_query} ({inner_query})"

def transactions():
    try:
        establishConnection = psycopg2.connect(dbname="postgres",user="postgres",password="password",host="localhost")
        cursor = establishConnection.cursor()
        transactionKeepGoing = True
        cursor.execute("BEGIN;")
        print("Transaction now under way")
        savepoints = []
        while transactionKeepGoing:
            print("What would you like the next action to be: Enter N for next command, S for SavePoint, R# for Rollback to savepoint #, or C for commit: ")
            na = input("Enter the next action: ")
            if na == "N":
                cursor.execute(welcome_interface(True))
            elif na == "S":
                sp = str(len(savepoints)+1)
                savepoints.append(sp)
                print(f"SAVEPOINT \"{sp}\";")
                cursor.execute(f"SAVEPOINT \"{sp}\";")
                print(f"SAVEPOINT \"{sp}\" created")
            elif na.startswith("R"):
                index = na[1:]
                print(f"ROLLBACK TO SAVEPOINT \"{index}\";")
                cursor.execute(f"ROLLBACK TO SAVEPOINT \"{int(index)}\";")
                savepoints = savepoints[0:int(index)+1]
                print(f"ROLLBACK TO {index} Completed")
            else:
                transactionKeepGoing = False
        establishConnection.commit()
        cursor.close()
        establishConnection.close()
        print("Successfully committed, transaction terminated")
    except psycopg2.DatabaseError as e:
        print(f"ALERT ERROR ALERT : {e}")

def error_handling():
        print("Alert: There is a try except block around the query execution")
        print("Error Handling is already enabled. Please continue with an operation")
        welcome_interface()
def insert_data_executor(tableName,values):
    valuesToString = "".join([f"\'{i}\'," for i in values[0:len(values)-1]] + [f"\'{values[-1]}\'"])
    exec_query(f"INSERT INTO {s[tableName]} VALUES ({valuesToString})")
def delete_data_executor(tableName,condition):
    exec_query(f"DELETE FROM {tableName} WHERE {condition}")

def update_data_executor(tableName,columnToChange,newValue,condition):
    exec_query(f"UPDATE {tableName} SET {columnToChange} = \'{newValue}\' WHERE {condition}")

def search_data_executor(tableName,condition,cols):
    exec_query(f"SELECT {cols} FROM {tableName} WHERE {condition}")

def aggregate_functions_executor(tablesName,column,calculationType):
    exec_query(f"SELECT {calculationType}({column}) FROM {tablesName}")

def sorting_executor(tableName,column,sortBy):
    exec_query(f"SELECT * FROM {tableName} ORDER BY {column} {sortBy}")

def joins_executor(table1,table2,key1,key2):
    exec_query(f"SELECT * FROM {table1} INNER JOIN {table2} ON {table1}.{key1} = {table2}.{key2}")

def grouping_executor(column1,tableName):
    exec_query(f"SELECT {column1}, COUNT(*) FROM {tableName} GROUP BY {column1}")

def subqueries_executor(outerQuery,innerQuery):
    exec_query(f"{outerQuery} ({innerQuery})")

def run():
    keep_going = True
    welcome_interface()
    while keep_going:
        val = input("Would you like to do another operation (Y/N): ")
        if val == "N":
            keep_going = False
        else:
            welcome_interface()

if __name__ == "__main__":
    run()
