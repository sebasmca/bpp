import math
import re
import pandas as pd
from matplotlib import pyplot as ptl


class Finanzas():
    _data_processed = False
    _gastos = list()
    _ingresos = list()
    _months = ['enero', 'febrero', 'marzo', 'abril',
                      'mayo', 'junio', 'julio', 'agosto',
                      'septiembre', 'octubre', 'noviembre', 'diciembre']


    def __init__(self):
        self._gastos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._ingresos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        string_viejo = str("1,1'").replace(",\"", "a")


    def __convert_2_numeric_type(self, data):
        # El dato es numérico?
        try:
            assert type(data).__name__ == 'int' or type(data).__name__ == 'float'
            if math.isnan(data):
                return 0
            return int(data)

        except AssertionError:
        # Si no es numérico, intentamos transformarlo a int
        # En caso de que se haya escrito el decimal usando coma, intentamos remplazar por punto y convertir
            try:
                converted_data = int(str(data).replace(',', '.'))
                return converted_data

            except ValueError as e:
            # Caso en que no se ha podido convertir el valor a numérico por algún motivo
                return 0

        except ValueError as e:
            # Caso en que no se ha podido convertir el valor a numérico por algún motivo
            return 0

    '''''    except ValueError as e:
            # If value error during numeric check
            try:
                converted_data = int(str(data).replace(',', '.'))
                return converted_data

            except ValueError as e:
            # Caso en que no se ha podido convertir el valor a numérico por algún motivo
                return 0
            return 0'''''

    def process_file(self, file, separator):
        try:
            df = pd.read_csv(file, delimiter=separator)

            # Si la columna está vacía la desechamos y continuamos con la siguiente columna
            if df.shape[1] != 12:
                raise InvalidNumberOfColumns(f"Invalid number of columns. Expected 12 found {df.shape[1]}.")

            # Si el nombre de la columna no es correcto o no están en el orden indicado
            for i in range(0,12):
                if df.columns[i].lower() != self._months[i]:
                    raise InvalidColumnNameOrOrder('''Column name or column order is not correct.\n
                                                    Check the column order and if the months are correctly
                                                    localized in spanish (es_ES)''')

            col_index = 0
            for col in df:
                # Si la columna está vacía la desechamos y continuamos con la siguiente columna

                try:
                    if df[col].empty:
                        raise ColumnIsEmpty(f"Column {col} has no values. It will be not considered on the mean computation")
                except ColumnIsEmpty as e:
                    col_index += 1
                    df.drop(col)
                    continue

                row_count = 0
                for data in df[col]:
                    row_count += 1
                    dat = self.__convert_2_numeric_type(data)
                    if dat < int(0):
                        self._gastos[col_index] += dat
                    elif dat >= int(0):
                        self._ingresos[col_index] += dat
                    else:
                        print(f"Ignoring value {data} at row {row_count} for column {col}...")
                col_index += 1
            self._data_processed = True
            return self

        except FileNotFoundError:
            # el valor de  self._data_processed se mantiene a False
            return False


    def get_month_with_more_expenses(self):
        try:
            assert self._data_processed == True
            expenses_peak = abs(min(self._gastos))
            month = self._months[self._gastos.index(min(self._gastos))]
            return expenses_peak, month
        except AssertionError as e:
            print("No data has been loaded yet.")

    def get_month_with_more_savings(self):
        try:
            assert self._data_processed == True
            max_savings = 0
            saved_max = 0
            index_max = 13
            for i in range(0, 12):
                try:
                    savings = 100*((self._ingresos[i] + (self._gastos[i]))/self._ingresos[i])
                except ZeroDivisionError as e:
                    savings = 0
                if savings > max_savings:
                    max_savings = savings
                    index_max = i
                    saved_max = self._ingresos[i] + self._gastos[i]
            return max_savings, self._months[index_max], saved_max
        except AssertionError as e:
            print("No data has been loaded yet.")

    def get_year_expenses_mean(self):
        try:
            assert self._data_processed == True
            nelem=12
            sum=0
            for i in range(0, 12):
                sum += self._gastos[i]
                # Si la columna estaba vacía, la lista tiene un valor 0 por defecto, no la cuento en la media
                if self._gastos[i] == 0:
                    nelem -= 1
            return abs(sum/nelem)
        except AssertionError as e:
            print("No data has been loaded yet.")

    def get_year_expenses(self):
        try:
            assert self._data_processed == True
            return abs(sum(self._gastos))
        except AssertionError as e:
            print("No data has been loaded yet.")

    def get_year_incomes(self):
        try:
            assert self._data_processed == True
            return sum(self._ingresos)
        except AssertionError as e:
            print("No data has been loaded yet.")

    def plot_income_by_month(self):
        ptl.plot(self._ingresos)
        ptl.show()

    def is_data_loaded(self):
        return self._data_processed


class InvalidNumberOfColumns(Exception):
    pass


class InvalidColumnNameOrOrder(Exception):
    pass


class ColumnIsEmpty(Exception):
    pass
