import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
import csv
import re

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Make sure to have the 'program.py' file in the correct location
from program import create_connection, save_data_table, cod_postal_api, data_csv_file, open_valid_file_csv

### DATABASE ###
# testes para a conexão da BD
class ConnectionDatabase(unittest.TestCase):
    @patch('mysql.connector.connect')  # Mock the database connection
    def test_successful_connection(self, mock_connect):
        """Test for a successful connection to the database."""
        # Create a mock connection object
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        # Call the create_connection function
        connection = create_connection('localhost', 'root', '', 'concelho_distritos')

        # Assert that mysql.connector.connect was called with the right arguments
        mock_connect.assert_called_once_with(
            host='localhost',
            user='root',
            password='',
            database='concelho_distritos'
        )
        
        # Assert that the returned connection is the mock connection
        self.assertEqual(connection, mock_connection)

    @patch('mysql.connector.connect')
    def test_error_connection_database(self, mock_connect):
        """Test for a failed connection to the database."""
        # Simulate connection failure by raising an error
        mock_connect.side_effect = mysql.connector.Error("Connection failed")

        # Call the create_connection function with incorrect credentials
        connection = create_connection('localhost', 'root', '', 'concelho_distritos')

        # Assert that mysql.connector.connect was called with the wrong password
        mock_connect.assert_called_once_with(
            host='localhost',
            user='root',
            password='testes_erro',
            database='concelho_distritos'
        )

        # Assert that the function returns None when connection fails
        self.assertIsNone(connection)   

# testes de insercao na BD (tabela distrito_conc_post)


class InsertValuesTableOnDatabase(unittest.TestCase):
    @patch('mysql.connector.connect')  # Mock the database connection
    def test_insert_table_dat_success(self, mock_connect):
        """Test successful insertion of data into the table"""
        # Create a mock cursor object
        mock_cursor = MagicMock()
        
        # Mock the connection to return the mock cursor
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        host_name = 'localhost'
        user_name = 'root'
        user_password = ''
        db_name = 'concelho_distritos'
        codigo_postal = '2520-193'
        concelho = 'Peniche'
        distrito = 'Leiria'
        
        # Call the save_data_table function
        save_data_table(host_name, user_name, user_password, db_name, codigo_postal, concelho, distrito)
        
        # Define the expected SQL query without backticks and semicolon
        expected_sql = "INSERT INTO distrito_conc_post (codigo_postal, concelhos, distritos) VALUES (%s, %s, %s)"
        
        # Normalize both expected and actual SQL strings
        expected_sql_normalized = ' '.join(expected_sql.split()).rstrip(';')  # Normalize expected SQL
        actual_sql_normalized = ' '.join(mock_cursor.execute.call_args[0][0].strip().split()).rstrip(';')  # Normalize actual SQL
        
        # Assert that the connection's cursor method was called
        mock_connect.assert_called_once_with(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        
        # Assert that the actual SQL matches the expected SQL
        self.assertEqual(expected_sql_normalized, actual_sql_normalized, 
                         f"Expected SQL: '{expected_sql_normalized}', but got: '{actual_sql_normalized}'")

        # Check if the correct values were passed to the execute method
        mock_cursor.execute.assert_called_once()
        called_sql, called_params = mock_cursor.execute.call_args[0]
        
        # Check if the SQL statement contains the expected command
        self.assertIn("INSERT INTO distrito_conc_post", called_sql, "The SQL command is incorrect.")
        
        # Assert that the values passed to the execute method are correct
        self.assertEqual(called_params, (codigo_postal, concelho, distrito), 
                         f"Expected parameters: {(codigo_postal, concelho, distrito)}, but got: {called_params}")
        
        # Assert that the connection's commit method was called to save the changes
        mock_connection.commit.assert_called_once()

    @patch('mysql.connector.connect')  # Mock the database connection
    def test_insert_table_dat_failure(self, mock_connect):
        """Test successful insertion of data into the table"""
        # Create a mock cursor object
        mock_cursor = MagicMock()
        
        # Mock the connection to return the mock cursor
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        host_name = 'localhost'
        user_name = 'root'
        user_password = ''
        db_name = 'concelho_distritos'
        codigo_postal = 12
        concelho = 'Peniche'
        distrito = 'Leiria'

        # Call the save_data_table function and expect it to raise a TypeError or other exception
        with self.assertRaises(TypeError):
            save_data_table(host_name, user_name, user_password, db_name, codigo_postal, concelho, distrito)

        # Assert that the connection's cursor method was called
        mock_connect.assert_called_once_with(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )

        # Check that execute was never called due to the exception
        mock_cursor.execute.assert_not_called()

        # Check that commit was also never called
        mock_connection.commit.assert_not_called()


### APIS ###

class ApiValuesDistritoConcelho(unittest.TestCase):
    @patch('requests.get')
    def test_api_values_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"codigo_postal": "2520-193", "concelho": "Peniche", "distrito": "Leiria"}

        # Call the cod_postal_api function
        data, status_code = cod_postal_api('f6ef0f7e3f4f4d3fa64d56c67e639a15', '2520', '193')
        

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {"codigo_postal": "2520-193", "concelho": "Peniche", "distrito": "Leiria"})

    @patch('requests.get')
    def test_api_values_api_invalid(self, mock_get):
        api_key = 'f6ef0f7e3f4f4d3fa64d56c67e639a1'
        mock_response = mock_get.return_value
        mock_response.status_code = 400
        mock_response.text = f"API key '{api_key}' invalida!"

        # Call the cod_postal_api function
        data, status_code = cod_postal_api(api_key, '2520', '193')
        

        # Assertions
        self.assertEqual(status_code, 400)
        self.assertEqual(data, f"API key '{api_key}' invalida!")

    @patch('requests.get')
    def test_api_values_cod_postal_invalid(self, mock_get):
        api_key = 'f6ef0f7e3f4f4d3fa64d56c67e639a15'
        mock_response = mock_get.return_value
        mock_response.status_code = 400
        mock_response.text = "Codigo postal com formato invalido. Formato deve ser '1234-123'."

        # Call the cod_postal_api function
        data, status_code = cod_postal_api(api_key, '2520', '19')
        

        # Assertions
        self.assertEqual(status_code, 400)
        self.assertEqual(data, "Codigo postal com formato invalido. Formato deve ser '1234-123'.")


    @patch('requests.get')
    def test_api_values_server_error(self, mock_get):
        """Test API response for a generic error."""
        # Mock the response object for an error
        mock_response = mock_get.return_value
        mock_response.status_code = 500  # Simulating a server error

        # Call the cod_postal_api function
        data, status_code = cod_postal_api('your_api_num', '2520', '193')

        # Assertions
        self.assertEqual(status_code, 500)
        self.assertEqual(data, "Error: Unable to fetch data.")
    


### CSV ###


class VerifyFileIsCSV(unittest.TestCase):
    def teste_valid_csv_file(self):
        with self.assertRaises(ValueError) as context:
            open_valid_file_csv('codigos_postais.txt')
        self.assertEqual(str(context.exception), "O ficheiro deve ter a extensão .csv")

class VerifyFileIsExists(unittest.TestCase):
    def teste_valid_file_exists(self):
        content = open_valid_file_csv('../codigos_postais.csv')
        # Check if the first row (header) is as expected
        self.assertEqual(content[0], ['cp7', 'concelho', 'distrito'])  # Check header
        actual_data = content[1:]  # Get all data rows except the header
        
        # Here, you might want to check only if '7800-780' is in the actual data
        self.assertIn(['7800-780', '', ''], actual_data)

class VerifyFileIsNotExists(unittest.TestCase):
    def teste_valid_file_not_exists(self):
        with self.assertRaises(FileNotFoundError) as context:
            open_valid_file_csv('non_existing_file.csv')
        self.assertEqual(str(context.exception), "O ficheiro 'non_existing_file.csv' não existe.")

class VerifyerrorFileCSV(unittest.TestCase):
    def test_error_opening_file(self):
        """Test that an error is raised for an inaccessible file."""
        # Create a CSV file with restricted permissions
        restricted_file = 'restricted_file.csv'
        with open(restricted_file, 'w', newline='', encoding='utf-8') as f:
            f.write('Column1,Column2\nData1,Data2')
        
        # Remove write permissions
        os.chmod(restricted_file, 0o000)

        try:
            with self.assertRaises(Exception) as context:
                open_valid_file_csv(restricted_file)
            self.assertTrue("Erro ao abrir o ficheiro" in str(context.exception))
        finally:
            os.chmod(restricted_file, 0o666)
            os.remove(restricted_file)

class SearchFileCSVContents(unittest.TestCase):
    def test_search_values_csv_file(self):
        # Define the expected output based on known values in your CSV
        expected_result = [{'cp7': '7800-780', 'concelho': '', 'distrito': ''}]  # Update as necessary

        # Call the function with parameters
        result = data_csv_file(distrito='', concelho='', cod_postal='7800-780')
        

        # Check if the expected result is found
        self.assertEqual(result, expected_result)

    def test_search_values_csv_file_no_value(self):
        # Define the expected output when no values are searched
        # This should ideally be all rows in your CSV.
        expected_result = [
            {'cp7': '7800-780', 'concelho': '', 'distrito': ''},
            {'cp7': '7830-000', 'concelho': '', 'distrito': ''},
            # Include all relevant rows based on your CSV content
            # Ensure you include all rows that are present in your CSV file
        ]

        # Call the function without any filtering parameters
        result = data_csv_file(distrito='', concelho='', cod_postal='')

        for expected in expected_result:
            self.assertIn(expected, result)

class FileNotFoundCSV(unittest.TestCase):
    def test_file_not_found_csv(self):
        # Define a file name that does not exist
        non_existent_file = 'non_existent_file.csv'

        # Use assertRaises to check for FileNotFoundError
        with self.assertRaises(FileNotFoundError) as context:
            open_valid_file_csv(non_existent_file)
        
        # Optionally, you can check the exception message
        self.assertEqual(str(context.exception), f"O Ficheiro '{non_existent_file}' não existe")


def save_results_to_csv(results):
    """Save test results to a CSV file."""
    
    csv_file_path = os.path.join(os.path.dirname(__file__), 'test_results.csv')
    file_exists = os.path.isfile(csv_file_path)
    try:
        # Writing to CSV file in the specified format
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the headers
            if not file_exists:
                writer.writerow(['Test', 'Group', 'Status'])

            
            
            # Write the results, extracting class names and method names
            for test, status in results:
                met = test.split(' ')
                cls = met[1].split('.')[1]
                mtd = met[1].split('.')[2].replace(')', '')
                print(cls, mtd)

                writer.writerow([cls, mtd, status])
        print(f"CSV file created successfully at: {csv_file_path}")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

if __name__ == '__main__':
    suite = unittest.TestSuite()
    
    # Load all test cases from the current module
    tests = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
    suite.addTests(tests)
    
    # List to hold the results
    results = []

    # Create a custom test runner to capture the results
    class CustomTestResult(unittest.TextTestResult):
        def addSuccess(self, test):
            super().addSuccess(test)
            results.append((str(test), 'success'))

        def addFailure(self, test, err):
            super().addFailure(test, err)
            results.append((str(test), 'failure'))

        def addError(self, test, err):
            super().addError(test, err)
            results.append((str(test), 'error'))

    class CustomTextTestRunner(unittest.TextTestRunner):
        def _makeResult(self):
            return CustomTestResult(self.stream, self.descriptions, self.verbosity)

    # Run the test suite
    runner = CustomTextTestRunner(verbosity=2)
    runner.run(suite)

    # Save the results to a CSV file
    save_results_to_csv(results)
