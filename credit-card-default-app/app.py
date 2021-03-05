from h2o_wave import Q, ui, app, main, data
from driverless_connect import DriverlessPredict
from mlops import get_prediction
import pandas as pd, os.path
import numpy as np
from views import *

@app('/')
async def serve(q: Q):
    q.page['meta'] = ui.meta_card(box='', theme='neon')
    if q.page['error_message']:
        del q.page['error_message']
    if q.args.predict:
        await update_dashboard(q)
    else:
        await show_homepage(q)


async def show_homepage(q: Q):
    if q.client.initialise is None:
        init(q)

        q.page['header'] = add_header_card(box='1 1 11 1')
        q.page['sidebar'] = add_sidebar_card(box='1 2 2 -1',
                                             customer_ids=q.user.customer_ids,
                                             customer_names=q.user.customer_names,
                                             customer_id=q.user.customer_id,
                                             endpoint=q.user.endpoint)
        q.page['content'] = add_text_card(box='3 2 9 -1', text="")

        q.client.initialise = True

    await q.page.save()


async def update_dashboard(q: Q):
    print("args: ", q.args)
    if q.args.customer_id is None:
        await q.page.save()
        return
    else:
        q.user.customer_id = q.args.customer_id
        q.user.endpoint = q.args.endpoint
        q.page['sidebar'] = add_sidebar_card(box='1 2 2 -1',
                                             customer_ids=q.user.customer_ids,
                                             customer_names=q.user.customer_names,
                                             customer_id=q.user.customer_id,
                                             endpoint=q.user.endpoint)

    customer = q.user.dataset[q.user.dataset['ID'] == int(q.args.customer_id)]
    customer_record = customer.iloc(0)[0].copy()
    if q.user.endpoint and q.user.endpoint != "":
        try:
            customer_record['Prediction'] = get_prediction(customer, q.args.endpoint).iloc[0]
        except:
            add_error_message(q, "error", "MLOps connection failed. Please check the correctness of the URL or whether the service is running.")

    q.page['content'] = add_text_card(box='3 2 9 1', text="")
    q.page['name'] = add_markdown(box='3 2 1 1', key="Customer Name:", value=customer_record['Name'])
    q.page['id'] = add_markdown(box='4 2 1 1', key="Customer ID:", value=str(customer_record['ID']))

    q.page['row11'] = add_gauge_card(box='3 3 1 3', key='Default Probability', value=customer_record['Prediction'])

    q.page['row12'] = add_stat_card(box='4 3 2 2', key='Income', value=str(customer_record['Income']))
    q.page['row22'] = add_interval_card(box='4 4 2 2', title="", value=str(customer_record['Income']))
    add_hist_to_page(q.page['row22'], q.user.dataset['Income'])

    q.page['row13'] = add_stat_card(box='6 3 2 2', key='Age', value=str(customer_record['Age']))
    q.page['row23'] = add_interval_card(box='6 4 2 2', title="", value=str(customer_record['Age']))
    add_hist_to_page(q.page['row23'], q.user.dataset['Age'])

    q.page['row14'] = add_stat_card(box='8 3 2 2', key='Credit Limit', value=str(customer_record['Credit Limit']))
    q.page['row24'] = add_interval_card(box='8 4 2 2', title="", value=str(customer_record['Credit Limit']))
    add_hist_to_page(q.page['row24'], q.user.dataset['Credit Limit'])

    q.page['row15'] = add_stat_card(box='10 3 2 2', key='Pay Delay September', value=customer_record['Pay Delay September'])
    q.page['row25'] = add_interval_card(box='10 4 2 2', title="", value=str(customer_record['Pay Delay September']))
    add_hist_to_page(q.page['row25'], q.user.dataset['Pay Delay September'])

    q.page['row31'] = add_area_card(box='3 6 4 4', title="Global Default Distribution", value=customer_record['Prediction'])
    add_hist_to_page(q.page['row31'], q.user.dataset['Prediction'])

    q.page['row32'] = add_chart(box='7 6 5 4', title="Global Feature Importance")
    q.page['row32'].data = [(x, y) for x, y in zip(q.user.fe["label"], q.user.fe['value'])][:10]

    q.page['row41'] = add_text_card(box='3 10 9 -1', text=q.user.about_text)

    await q.page.save()

def init(q):
    input_path = 'datasets/Credit Card - Test.csv'
    q.user.dataset = pd.read_csv(input_path).fillna(0)
    q.user.customer_ids = list(q.user.dataset['ID'])[:10]
    q.user.customer_names = list(q.user.dataset['Name'])[:10]

    if not os.path.isfile('datasets/Credit Card - Test_predictions.csv'):
        dp = DriverlessPredict(config={"username": "", "password": "", "experiment_key": "", "address": ""})
        predictions = dp.dai_predict(input_path=input_path)
    else:
        predictions = pd.read_csv("datasets/Credit Card - Test_predictions.csv")

    q.user.dataset['Prediction'] = predictions['Prediction']
    q.user.dataset = q.user.dataset.dropna()

    q.user.fe = pd.read_csv("datasets/Data - Original Shapley (Naive Shapley).csv").dropna()
    q.user.fe['value'] = q.user.fe['value']/q.user.fe['value'].max()
    q.user.about_text = 'The risk model for this dashboard is powered by Driverless AI.'

def add_hist_to_page(page, values):
    count, division = np.histogram(values)
    page.data = [(x, y) for x, y in zip(count.tolist(), division.tolist())]