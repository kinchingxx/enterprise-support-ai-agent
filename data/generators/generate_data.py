import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


random.seed(42)

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_customers(count: int = 100) -> pd.DataFrame:
    industries = [
        "Healthcare",
        "Retail",
        "Finance",
        "Education",
        "Construction",
        "Hospitality",
        "Technology",
    ]

    regions = ["QLD", "NSW", "VIC", "SA", "WA"]
    company_sizes = ["Small", "Medium", "Large"]
    support_plans = ["Standard", "Premium", "Enterprise"]

    customers = []

    for i in range(1, count + 1):
        customers.append(
            {
                "customer_id": f"C{i:04d}",
                "company_name": f"Company {i:03d}",
                "industry": random.choice(industries),
                "region": random.choice(regions),
                "company_size": random.choice(company_sizes),
                "support_plan": random.choice(support_plans),
            }
        )

    return pd.DataFrame(customers)


def generate_products() -> pd.DataFrame:
    products = [
        ("P001", "CloudDesk", "Productivity", "4.2"),
        ("P002", "SecureGate", "Security", "3.8"),
        ("P003", "DataFlow", "Data Platform", "5.1"),
        ("P004", "InsightHub", "Analytics", "2.9"),
        ("P005", "ConnectAPI", "Integration", "3.4"),
        ("P006", "IdentityCore", "Identity", "4.7"),
        ("P007", "MobileWork", "Mobile", "2.5"),
        ("P008", "BackupVault", "Storage", "6.0"),
        ("P009", "ServiceDesk", "Support", "4.1"),
        ("P010", "AutomationHub", "Automation", "3.2"),
    ]

    return pd.DataFrame(
        products,
        columns=[
            "product_id",
            "product_name",
            "product_category",
            "release_version",
        ],
    )


def generate_tickets(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    count: int = 1000,
) -> pd.DataFrame:

    categories = [
        "Login",
        "Performance",
        "Integration",
        "Billing",
        "Data",
        "Security",
        "Configuration",
    ]

    priorities = ["Low", "Medium", "High", "Critical"]
    statuses = ["Open", "In Progress", "Resolved", "Closed"]

    descriptions = {
        "Login": "User unable to authenticate successfully.",
        "Performance": "Application performance is slower than expected.",
        "Integration": "External system integration is failing.",
        "Billing": "Customer reported an unexpected billing issue.",
        "Data": "Customer reported inconsistent data.",
        "Security": "Potential security-related issue requires investigation.",
        "Configuration": "Application configuration is not working as expected.",
    }

    start_date = datetime.now() - timedelta(days=180)

    tickets = []

    for i in range(1, count + 1):
        category = random.choice(categories)
        created_at = start_date + timedelta(
            minutes=random.randint(0, 180 * 24 * 60)
        )

        tickets.append(
            {
                "ticket_id": f"T{i:05d}",
                "customer_id": random.choice(
                    customers["customer_id"].tolist()
                ),
                "product_id": random.choice(
                    products["product_id"].tolist()
                ),
                "category": category,
                "priority": random.choices(
                    priorities,
                    weights=[25, 40, 25, 10],
                    k=1,
                )[0],
                "description": descriptions[category],
                "created_at": created_at.isoformat(),
                "status": random.choice(statuses),
            }
        )

    return pd.DataFrame(tickets)


def main():
    customers = generate_customers()
    products = generate_products()
    tickets = generate_tickets(customers, products)

    customers.to_csv(OUTPUT_DIR / "customers.csv", index=False)
    products.to_csv(OUTPUT_DIR / "products.csv", index=False)
    tickets.to_csv(OUTPUT_DIR / "tickets.csv", index=False)

    print("Synthetic enterprise data generated successfully.")
    print(f"Customers: {len(customers)}")
    print(f"Products: {len(products)}")
    print(f"Tickets: {len(tickets)}")


if __name__ == "__main__":
    main()