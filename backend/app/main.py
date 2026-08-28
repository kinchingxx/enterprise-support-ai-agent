from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException


app = FastAPI(
    title="Enterprise Support Source APIs",
    description="Simulated enterprise CRM, product and support systems.",
    version="1.0.0",
)


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def load_csv(filename: str) -> pd.DataFrame:
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise RuntimeError(
            f"{filename} not found. Run the synthetic data generator first."
        )

    return pd.read_csv(file_path)


@app.get("/")
def root():
    return {
        "service": "Enterprise Support Source APIs",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/customers")
def get_customers():
    customers = load_csv("customers.csv")

    return customers.to_dict(orient="records")


@app.get("/customers/{customer_id}")
def get_customer(customer_id: str):
    customers = load_csv("customers.csv")

    result = customers[
        customers["customer_id"] == customer_id
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return result.iloc[0].to_dict()


@app.get("/products")
def get_products():
    products = load_csv("products.csv")

    return products.to_dict(orient="records")


@app.get("/products/{product_id}")
def get_product(product_id: str):
    products = load_csv("products.csv")

    result = products[
        products["product_id"] == product_id
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return result.iloc[0].to_dict()


@app.get("/tickets")
def get_tickets(
    status: str | None = None,
    priority: str | None = None,
):
    tickets = load_csv("tickets.csv")

    if status:
        tickets = tickets[
            tickets["status"].str.lower() == status.lower()
        ]

    if priority:
        tickets = tickets[
            tickets["priority"].str.lower() == priority.lower()
        ]

    return tickets.to_dict(orient="records")


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    tickets = load_csv("tickets.csv")

    result = tickets[
        tickets["ticket_id"] == ticket_id
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return result.iloc[0].to_dict()