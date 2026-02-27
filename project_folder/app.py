from flask import Flask, render_template, request, send_file
from faker import Faker
import pandas as pd
import random

app = Flask(__name__)
fake = Faker()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    num_rows = int(request.form["rows"])
    num_cols = int(request.form["columns"])

    data = []

    for _ in range(num_rows):
        row = {}

        for col_index in range(num_cols):
            column_name = f"field_{col_index+1}"

            # Randomly assign realistic values
            value_type = random.choice(["name", "number", "city", "email"])

            if value_type == "name":
                value = fake.name()
            elif value_type == "number":
                value = random.randint(18, 100)
            elif value_type == "city":
                value = fake.city()
            else:
                value = fake.email()

            row[column_name] = value

        data.append(row)

    df = pd.DataFrame(data)

    file_name = "synthetic_dataset.csv"
    df.to_csv(file_name, index=False)

    return send_file(file_name, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
