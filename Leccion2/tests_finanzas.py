import pytest
import csv
from finanzas import *
import os

def test_process_file_exception_InvalidNumberOfColumns_missing_col():
    # Test data: 11 columnas, falta el mes de Julio
    header = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
              'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    with open('missing_column.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    # Verification
    with pytest.raises(InvalidNumberOfColumns, match="Invalid number of columns. Expected 12 found 11."):
        Finanzas().process_file('missing_column.csv', separator=',')
    os.remove('missing_column.csv')


def test_process_file_exception_InvalidNumberOfColumns_extra_col():
    # Test data: 13 columnas
    header = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
              'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre', 'aeed']

    with open('extra_column.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    # Verification
    with pytest.raises(InvalidNumberOfColumns, match="Invalid number of columns. Expected 12 found 13."):
        Finanzas().process_file('extra_column.csv', separator=',')
    os.remove('extra_column.csv')

def test_process_file_exception_InvalidColumnNameOrOrder_name():
    # Columna "Mayo" mal escrita ("Maio")
    header = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Maio', 'Junio', 'Julio',
              'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    with open('bad_column_name.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    with pytest.raises(InvalidColumnNameOrOrder, match="Column name or column order is not correct.*"):
        Finanzas().process_file('bad_column_name.csv', separator=',')
    os.remove('bad_column_name.csv')

def test_process_file_exception_InvalidColumnNameOrOrder_order():
    # Semptiembre y Octubre están intercambiadas
    header = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
              'Agosto', 'Octubre', 'Septiembre', 'Noviembre', 'Diciembre']

    with open('bad_column_order.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    with pytest.raises(InvalidColumnNameOrOrder, match="Column name or column order is not correct.*"):
        Finanzas().process_file('bad_column_order.csv', separator=',')
    os.remove('bad_column_order.csv')

def test_process_file_exception_FileNotFoundError():
    assert Finanzas().process_file('incorrect_filename.csv', separator=',') is False

def test_process_file_handles_empty_column():
    # Columna "Enero" vacía
    header = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
              'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    row1 = ["", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    row2 = ["", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    with open('empty_column.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(row1)
        writer.writerow(row2)

    errors = []
    expected_income = sum(row1[1:]) + sum(row2[1:])
    fin = Finanzas().process_file('empty_column.csv', separator=',')

    if fin.is_data_loaded() is not True:
        errors.append("File not processed")
    if fin.get_year_incomes() != expected_income:
        print(fin.get_year_incomes())
        print(expected_income)
        errors.append("Wrong yearly income computed")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))
    os.remove('empty_column.csv')


def test_process_file_handles_different_data_types():
    header = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
              'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    row1 = [ "1.000,01", 1, "2", "3.1", 4.2, -5, "-6", "-7.9", "ups", 9, 10, 11]
    row2 = ["", "-1.9'", "0", "NaN", 10, 0.432321, "1,1", "-2,1", -1, 0, -10, 11]

    with open('data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(row1)
        writer.writerow(row2)

    expected_income = 1 + 2 + 3 + 4 + 9 + 10 + 11 + 10 + 11
    expected_expenses_mean= abs(-5 - 6 - 1 - 10)
    errors = []
    fin = Finanzas().process_file('data.csv', separator=',')

    if fin.is_data_loaded() is not True:
        errors.append("File not processed")
    if fin.get_year_incomes() != expected_income:
        errors.append("Wrong yearly income computed")
    if fin.get_year_expenses() != expected_expenses_mean:
        errors.append("Wrong yearly expenses mean computed")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))
    os.remove('data.csv')

def test_get_month_with_more_expenses():
    header = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
              'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    row1 = [0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11]
    row2 = [0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11]

    with open('data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(row1)
        writer.writerow(row2)

    expected_expenses = 22
    expected_month = "diciembre"

    fin = Finanzas().process_file('data.csv', separator=',')
    peak, month = fin.get_month_with_more_expenses()

    errors = []
    if peak != expected_expenses:
        errors.append("wrong expenses")
    if month != expected_month:
        errors.append("wrong month")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))
    os.remove('data.csv')

def test_get_month_with_more_savings():
    # Los datos de prueba incluyen tammbién el caso de dividir por cero
    header = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
              'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    row1 = [0, 2, 3, 10, 20, 0, 6, 7, 8, 14, 10, 11]
    row2 = [0, -1, -1, -5, -11, -5, -6, -7, -1, -1, -19, -11]

    with open('data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(row1)
        writer.writerow(row2)

    percent_savings = 100*(14-1)/14
    expected_month = "octubre"
    saved = 13

    fin = Finanzas().process_file('data.csv', separator=',')
    proportion, month, saves = fin.get_month_with_more_savings()

    errors = []
    if proportion != percent_savings:
        errors.append("wrong proportion of savings")
    if month != expected_month:
        errors.append("wrong month")
    if saved != saves:
        errors.append("wrong amount saved")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))
    os.remove('data.csv')

def test_get_year_expenses_mean_empty_columns():
    # Calculo media de gastos con columnas de menos
    header = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
              'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    row1 = ["", "", 2, 3, 4, 5, 6, 5, 1, 9, 0, -1]
    row2 = ["", "", -2, -3, -4, -5, -6, -7, -8, -9, -10, -11]

    with open('empty_column.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(row1)
        writer.writerow(row2)

    expected_expenses = abs(sum(row2[2:]) - 1)/10
    fin = Finanzas().process_file('empty_column.csv', separator=',')

    assert fin.get_year_expenses_mean() == expected_expenses

def test_get_year_expenses_mean():
    header = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
              'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    row1 = [1, -6, 2, 3, 4, 5, 6, 5, 1, 9, 0, -1]
    row2 = [-3, -2, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11]

    with open('empty_column.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(row1)
        writer.writerow(row2)

    expected_expenses = abs(sum(row2) - 7)/12
    fin = Finanzas().process_file('empty_column.csv', separator=',')

    assert fin.get_year_expenses_mean() == expected_expenses
    os.remove('empty_column.csv')

def test_get_year_expenses():
    header = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
              'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    row1 = [1, -6, 2, 3, 4, 5, 6, 5, 1, 9, 0, -1]
    row2 = [-3, -2, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11]

    with open('empty_column.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(row1)
        writer.writerow(row2)

    expected_expenses = abs(sum(row2) - 7)
    fin = Finanzas().process_file('empty_column.csv', separator=',')

    assert fin.get_year_expenses() == expected_expenses
    os.remove('empty_column.csv')

def test_get_year_incomes():
    header = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
              'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    row1 = [1, -6, 2, 3, 4, 5, 6, 5, 1, 9, 0, -1]
    row2 = [-3, -2, -2, -3, -4, -5, -6, -7, -8, -9, 10, -11]

    with open('data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(row1)
        writer.writerow(row2)

    expected_incomes = 1 + 2 + 3 + 4 + 5 + 6 + 5 + 1 + 9 + 10
    fin = Finanzas().process_file('data.csv', separator=',')

    assert fin.get_year_incomes() == expected_incomes
    os.remove('data.csv')
    
# Tested indirectly:
# private methodd __convert_2_numeric_type(), is_data_loaded()