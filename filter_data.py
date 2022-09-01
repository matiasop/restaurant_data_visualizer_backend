from get_data import get_category
from collections import defaultdict


def add_sales_per_category(data):
    sales_per_category = defaultdict(int)
    for order in data:
        for product in order["products"]:
            category = product["category"]
            price = product["price"]
            sales_per_category[category] += price

    return dict(sales_per_category)


def add_sales_per_payment_type(data):
    sales_per_payment_type = defaultdict(int)
    for order in data:
        for payment in order["payments"]:
            type = payment["type"]
            amount = payment["amount"]
            sales_per_payment_type[type] += amount

    return dict(sales_per_payment_type)


def total_sales_per_group(group, data, aggregator):
    sales_per_group = {}
    groups = get_category(group, data)
    for g in groups:
        group_data = list(filter(lambda x: x[group] == g, data))
        if aggregator == "category":
            sales = add_sales_per_category(group_data)
        elif aggregator == "payment_type":
            sales = add_sales_per_payment_type(group_data)
        sales_per_group[g] = sales

    if group == "weekday":
        weekdays = ["Lunes", "Martes", "Miércoles",
                    "Jueves", "Viernes", "Sábado", "Domingo"]
        return {key: sales_per_group[key] for key in weekdays}
    return {key: sales_per_group[key] for key in sorted(sales_per_group)}


def transform_sales_format(sales):
    labels = list(sales.keys())
    sub_labels = list(sales[labels[0]].keys())

    result = defaultdict(list)
    for sub_label in sub_labels:
        for label in labels:
            result[sub_label].append(sales[label][sub_label])

    return {"labels": labels, "datasets": dict(result)}


def get_sales_per_category(data, period, category):
    sales = total_sales_per_group(period, data, "category")
    result = {}
    for key in sales:
        result[key] = sales[key][category]
    formatted_sales = transform_sales_format(sales)
    return formatted_sales


def get_total_sales(group, data, aggregator):
    sales = total_sales_per_group(group, data, aggregator)
    formatted_sales = transform_sales_format(sales)
    return formatted_sales


def get_sales(group, data):
    sales = total_sales_per_group(group, data, "category")
    total = {g: sum(sales[g].values()) for g in sales}
    return {"labels": list(total.keys()), "datasets": list(total.values())}
