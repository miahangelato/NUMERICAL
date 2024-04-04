from django.shortcuts import render
from .forms import LinearEquationForm
import numpy as np
import re

def index(request):
    if request.method == 'POST':
        form = LinearEquationForm(request.POST)
        if form.is_valid():
            equations_str = form.cleaned_data['equations']
            equations = equations_str.strip().split('\n')

            coefficients = []
            constants = []
            for equation in equations:
                parts = equation.split("=")
                lhs = parts[0].strip()
                rhs = parts[1].strip()

                # Extracting coefficients from the left-hand side of the equation
                lhs_terms = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', lhs)  # Extract all numbers (floats and integers) from the equation
                coef = []
                for term in lhs_terms:
                    coef.append(float(term))

                # Extracting the constant from the right-hand side of the equation
                constant = float(rhs)

                coefficients.append(coef)
                constants.append(constant)

            coefficients_matrix = np.array(coefficients)
            constants_vector = np.array(constants)
            determinant = np.linalg.det(coefficients_matrix)
            

            # Check if the system of equations is solvable
            if determinant == 0:
                result = "The system of equations is either inconsistent or has infinitely many solutions."
            else:
                # Create matrices for variables 'x', 'y', and 'z' by replacing their coefficients with constants
                x_matrix = np.array(coefficients)
                x_matrix[:, 0] = constants_vector

                y_matrix = np.array(coefficients)
                y_matrix[:, 1] = constants_vector

                z_matrix = np.array(coefficients)
                z_matrix[:, 2] = constants_vector

                # Calculate the values of x, y, and z using Cramer's Rule
                solutions = np.linalg.solve(coefficients_matrix, constants_vector)
                result = f"The solution of the system of equations is x = {solutions[0]}, y = {solutions[1]}, z = {solutions[2]}"

            num_columns = coefficients_matrix.shape[1]  # Number of columns in the coefficients matrix

            # Print the calculated matrices for x, y, and z
            print("Matrix for x:")
            print(x_matrix)
            print("Matrix for y:")
            print(y_matrix)
            print("Matrix for z:")
            print(z_matrix)

            context = {
                'form': form,
                'result': result,
                'num_columns': num_columns,
                'coefficients_matrix': coefficients_matrix,
                'constants_vector': constants_vector,
                'x_matrix': x_matrix,  # Pass the x_matrix to the template
                'y_matrix': y_matrix,  # Pass the y_matrix to the template
                'z_matrix': z_matrix,  # Pass the z_matrix to the template
            }

            return render(request, 'cramer_rule/result.html', context)
    else:
        form = LinearEquationForm()
    return render(request, 'cramer_rule/index.html', {'form': form})
