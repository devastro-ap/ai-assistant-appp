import streamlit as st
from sympy import symbols, Eq, solve, diff, integrate, sympify
from chempy import balance_stoichiometry
from chempy.util.parsing import formula_to_composition

st.title("Simple AI Assistant - Math, Physics, Chemistry")

topic = st.selectbox("Choose a subject", ["Math", "Physics", "Chemistry"])

if topic == "Math":
    st.subheader("Math Solver")
    expr = st.text_input("Enter expression or equation (e.g., x**2 - 4 = 0)")
    operation = st.selectbox("Operation", ["Solve equation", "Differentiate", "Integrate"])

    if expr:
        x = symbols('x')
        try:
            if operation == "Solve equation":
                lhs, rhs = expr.split('=')
                eq = Eq(sympify(lhs), sympify(rhs))
                sol = solve(eq, x)
                st.write("Solution:", sol)
            elif operation == "Differentiate":
                st.write("Derivative:", diff(sympify(expr), x))
            elif operation == "Integrate":
                st.write("Integral:", integrate(sympify(expr), x))
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Physics":
    st.subheader("Physics Calculator")
    motion_eq = st.text_input("Enter motion formula (e.g., v = u + a*t)")
    values = st.text_input("Enter known values as key=value, comma-separated (e.g., u=5,a=2,t=3)")

    if motion_eq and values:
        try:
            lhs, rhs = motion_eq.split('=')
            expr = Eq(sympify(lhs), sympify(rhs))
            vals = {symbols(k): float(v) for k,v in [item.split('=') for item in values.split(',')]}
            sol = solve(expr.subs(vals))
            st.write("Result:", sol)
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Chemistry":
    st.subheader("Chemistry Tools")
    chem_op = st.selectbox("Choose operation", ["Molar Mass", "Balance Equation"])

    if chem_op == "Molar Mass":
        formula = st.text_input("Enter chemical formula (e.g., H2O)")
        if formula:
            try:
                comp = formula_to_composition(formula)
                molar_mass = sum(v * m for (el, v), m in zip(comp.items(), [1.008, 15.999, 12.01, 14.01]))
                st.write("Approximate Molar Mass:", molar_mass, "g/mol")
            except Exception as e:
                st.error(f"Error: {e}")

    elif chem_op == "Balance Equation":
        reactants = st.text_input("Reactants (comma-separated, e.g., H2, O2)")
        products = st.text_input("Products (comma-separated, e.g., H2O)")

        if reactants and products:
            try:
                reac = [r.strip() for r in reactants.split(',')]
                prod = [p.strip() for p in products.split(',')]
                reac_coeffs, prod_coeffs = balance_stoichiometry(set(reac), set(prod))
                st.write("Balanced Equation:")
                st.write(' + '.join(f"{v} {k}" for k, v in reac_coeffs.items()) + " → " +
                         ' + '.join(f"{v} {k}" for k, v in prod_coeffs.items()))
            except Exception as e:
                st.error(f"Error: {e}")
