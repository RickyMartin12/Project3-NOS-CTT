# program.py

import requests
import pandas as pd
import mysql.connector
import csv
import os
from mysql.connector import Error
import requests

api_num = "f6ef0f7e3f4f4d3fa64d56c67e639a15"



def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        # print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return connection

def insert_concelho_distrito(connection, codigo_postal, concelho, distrito):
    insert_query = """
    INSERT INTO distrito_conc_post (codigo_postal, concelhos, distritos) 
    VALUES (%s, %s, %s);
    """
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query, (codigo_postal, concelho, distrito))
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def save_file_csv(file_name, codigo_postal, concelho, distrito):
    csv_data = []
    file_exists = os.path.isfile(file_name)
    csv_data.append([codigo_postal, concelho, distrito])

    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['cp7', 'concelho', 'distrito'])  # Write headers

        writer.writerows(csv_data)

def save_data_table(host_name, user_name, user_password, db_name, codigo_postal, concelho, distrito):
    connection = create_connection(host_name, user_name, user_password, db_name)
    insert_concelho_distrito(connection, codigo_postal, concelho, distrito)

def cod_postal_api(api, cp4, cp3):
    url = f"https://www.cttcodigopostal.pt/api/v1/{api}/{cp4}-{cp3}"

    # Send a GET request to the API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response (if the API returns JSON)
        data = response.json()
    elif response.status_code == 400:
        data = response.text
    else:
        # Handle unsuccessful responses
        data = "Error: Unable to fetch data."
    
    return data, response.status_code
    

def codigo_postal_selected (cp4, cp3):
    url = f"https://www.cttcodigopostal.pt/api/v1/{api_num}/{cp4}-{cp3}"

    # Send a GET request to the API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response (if the API returns JSON)
        data = response.json()

        if not data:  # Pythonic way
            codigo_postal = f"{cp4}-{cp3}"
            save_file_csv('codigos_postais.csv', codigo_postal, "", "")
            save_data_table("localhost", "root", "", "concelho_distritos", codigo_postal, "", "")
        else:
            # Accessing the first dictionary in the list
            first_entry = data[0]  # Get the first dictionary

            # Extracting codigo-postal, distrito, and concelho from the first entry
            codigo_postal = first_entry.get('codigo-postal')
            distrito = first_entry.get('distrito')
            concelho = first_entry.get('concelho')

            save_data_table("localhost", "root", "", "concelho_distritos", codigo_postal, concelho, distrito)

            save_file_csv('codigos_postais.csv', codigo_postal, concelho, distrito)

            
        
    elif response.status_code == 400:
        print(f"{response.text}")
        
    else:
        # Handle unsuccessful responses
        print(f"Error: Unable to fetch data.")


# opcao 2
def insert_new_codigo_postal():
    print("\n")
    codigo_postal_4 = input("Por favor introduza os 4 primeiros numeros do código postal: ")
    codigo_postal_3 = input("Por favor introduza os 3 ultimos numeros do código postal: ")

    # Call the function with user inputs
    codigo_postal_selected(codigo_postal_4, codigo_postal_3)



# opcao 1
def list_csv_file():
    file_name = 'codigos_postais.csv'
    if os.path.exists(file_name):
        print("\n--- List of Postal Codes ---")
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                print(row)
    else:
        print("CSV file does not exist. Please insert some data first.")



def list_db_conc_dist(cod_postal, distrito, concelho):
    query = "SELECT * FROM `distrito_conc_post` WHERE 1"

    params = []

    connection = create_connection("localhost", "root", "", "concelho_distritos")
    cursor = connection.cursor()

    # Add conditions based on user input
    if cod_postal != "":
        query += " AND codigo_postal LIKE %s"
        params.append('%' + cod_postal + '%')

    if distrito != "":
        query += " AND distritos LIKE %s"
        params.append('%' + distrito + '%')

    if concelho != "":
        query += " AND concelhos LIKE %s"
        params.append('%' + concelho + '%')

    # Now execute the query once with all the parameters
    cursor.execute(query, tuple(params))

    # Fetching all matching rows
    results = cursor.fetchall()

    formatted_strings = []


    print("+----------------------------------------------------+")
    print("| ID | Codigo Postal    | Concelhos     | Distritos  |")
    print("+----------------------------------------------------+")
    # Displaying the results
    if results:
        for row in results:
                formatted_string = f"| {row[0]:<2} | {row[1]:<16} | {row[2]:<13} | {row[3]:<10} |"
                formatted_strings.append(formatted_string)
        for formatted in formatted_strings:
                print(formatted)
        print("+----------------------------------------------------+")

    else:
        print("No results found.")

# opcao 3
def list_database_concelho_distrito_codigo_postal():

    
    value = input("Pesquisa na BD o codigo postal (primeiros 4 do codigo postal) (Enter sem nada retorna os valores do cidgo postal guardados na BD): ")
    print()
    distrito = input("Introduza o Distrito: ")
    print()
    concelho = input("Introduza o Concelho: ")
    print()

    list_db_conc_dist(value, distrito, concelho)

    
def open_valid_file_csv(file_name):
    if not file_name.endswith('.csv'):
        raise ValueError("O ficheiro deve ter a extensão .csv")
    
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"O ficheiro '{file_name}' não existe.")
    
    try:
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            contents = [row for row in reader]  # Read the CSV contents into a list
        return contents
    except Exception as e:
        raise Exception(f"Erro ao abrir o ficheiro: {e}")

def data_csv_file(distrito, concelho, cod_postal):
    found = False  # Flag to check if any rows are found
    results = []
    try:
        # Open and read the CSV file
        with open('codigos_postais.csv', mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            print("+-----------------------------------------------+")
            print("| Codigo Postal    | Concelhos     | Distritos  |")
            print("+-----------------------------------------------+")
            
            # Search for the row with the specified postal code
            for row in csv_reader:
                condition = True
                
                # Dynamically accumulate conditions for each non-empty parameter
                if distrito:
                    condition = condition and (row['distrito'] == distrito)
                if concelho:
                    condition = condition and (row['concelho'] == concelho)
                if cod_postal:
                    condition = condition and (row['cp7'] == cod_postal)
                
                # If all conditions are satisfied, print the row and set found to True
                if condition:
                    results.append(row)
                    print(f"| {row['cp7']:<16} | {row['concelho']:<13} | {row['distrito']:<10} |")
                    print("+-----------------------------------------------+")
                    found = True

                    
            
            if not found:
                print(f"No postal codes found for district '{distrito}'.")
    except FileNotFoundError:
        print("Error: The file 'codigos_postais.csv' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return results  # Return the list of found results
    

# opcao 4
def list_codigo_postal_csv():
    # Specify the postal code to search for

    # CSV - Distrito CSV
    # CSV - Codigo Postal
    # CSV - Concelho
    # Ambas
    distrito = input("Introduza o Distrito: ")
    print()
    concelho = input("Introduza o Concelho: ")
    print()
    cod_postal = input("Introduza o Codigo Postal: ")
    print()

    data_csv_file(distrito, concelho, cod_postal)

    



if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Listar o Ficheiro CSV")
        print("2. Inserir novo Codigo Postal, Concelho e Distrito (inserir na BD e ficheiro CSV)")
        print("3. Listar a tabela Concelhos, Distritos, Codigo Postal através da Base de Dados")
        print("4. Listar a tabela Concelhos, Distritos, Codigo Postal através do ficheiro CSV")
        print("0. Exit")

        choice = input("Escolhe uma opção: ")

        if choice == '1':
            list_csv_file()
        elif choice == '2':
            insert_new_codigo_postal()
        elif choice == '3':
            list_database_concelho_distrito_codigo_postal()
        elif choice == '4':
            list_codigo_postal_csv()
        elif choice == '0':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")