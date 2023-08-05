# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import requests
from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from assertions import *
import pandas as pd
from ibm_ai_openscale.supporting_classes import Metric, Threshold, MeasurementRecord
import random


class TestAIOpenScaleClient(unittest.TestCase):
    log_loss_random = None
    brier_score_loss = None
    ai_client = None
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    scoring_url = None
    b_app_uid = None
    x_uid = None
    labels = None
    variables = None
    wml_client = None
    subscription = None
    binding_uid = None
    aios_model_uid = None
    scoring_result = None
    payload_scoring = None
    published_model_details = None
    monitor_uid = None
    source_uid = None
    correlation_monitor_uid = None
    measurement_details = None
    transaction_id = None
    data_df = pd.read_csv(
        "./datasets/German_credit_risk/credit_risk_training.csv",
        dtype={'LoanDuration': int, 'LoanAmount': int, 'InstallmentPercent': int, 'CurrentResidenceDuration': int,
               'Age': int, 'ExistingCreditsCount': int, 'Dependents': int})

    test_uid = str(uuid.uuid4())

    # Custom deployment configuration
    credentials = {
        "url": "http://169.63.194.147:31520",
        "username": "xxx",
        "password": "yyy",
        "request_headers": {"content-type": "application/json"}
    }

    image_path = os.path.join(os.getcwd(), 'datasets', 'images', 'labrador.jpg')

    def score(self, subscription_details):
        fields = ["CheckingStatus", "LoanDuration", "CreditHistory", "LoanPurpose", "LoanAmount", "ExistingSavings",
                  "EmploymentDuration", "InstallmentPercent", "Sex", "OthersOnLoan", "CurrentResidenceDuration",
                  "OwnsProperty", "Age", "InstallmentPlans", "Housing", "ExistingCreditsCount", "Job", "Dependents",
                  "Telephone", "ForeignWorker"]
        values = [
            ["no_checking", 13, "credits_paid_to_date", "car_new", 1343, "100_to_500", "1_to_4", 2, "female", "none", 3,
             "savings_insurance", 25, "none", "own", 2, "skilled", 1, "none", "yes"],
            ["no_checking", 24, "prior_payments_delayed", "furniture", 4567, "500_to_1000", "1_to_4", 4, "male", "none",
             4, "savings_insurance", 60, "none", "free", 2, "management_self-employed", 1, "none", "yes"],
            ["0_to_200", 26, "all_credits_paid_back", "car_new", 863, "less_100", "less_1", 2, "female", "co-applicant",
             2, "real_estate", 38, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["0_to_200", 14, "no_credits", "car_new", 2368, "less_100", "1_to_4", 3, "female", "none", 3, "real_estate",
             29, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["0_to_200", 4, "no_credits", "car_new", 250, "less_100", "unemployed", 2, "female", "none", 3,
             "real_estate", 23, "none", "rent", 1, "management_self-employed", 1, "none", "yes"],
            ["no_checking", 17, "credits_paid_to_date", "car_new", 832, "100_to_500", "1_to_4", 2, "male", "none", 2,
             "real_estate", 42, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["no_checking", 50, "outstanding_credit", "appliances", 5696, "unknown", "greater_7", 4, "female",
             "co-applicant", 4, "unknown", 54, "none", "free", 2, "skilled", 1, "yes", "yes"],
            ["0_to_200", 13, "prior_payments_delayed", "retraining", 1375, "100_to_500", "4_to_7", 3, "male", "none", 3,
             "real_estate", 70, "none", "own", 2, "management_self-employed", 1, "none", "yes"]
        ]

        payload = {"fields": fields, "values": values}
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer xxx'}
        scoring_url = subscription_details['entity']['deployments'][0]['scoring_endpoint']['url']

        response = requests.post(scoring_url, json=payload, headers=header)

        return payload, response.json(), 25

    @staticmethod
    def get_metrics_list(client, monitor_uid):
        monitor_details = client.data_mart.monitors.get_details(monitor_uid=monitor_uid)
        metrics_list = [metric['id'] for metric in monitor_details['entity']['metrics']]

        return metrics_list

    @staticmethod
    def get_formatted_metrics_pandas(metrics_pandas, metrics_uids):
        variables = pd.DataFrame()
        for uid in metrics_uids:
            values = metrics_pandas.loc[metrics_pandas['id'] == uid, 'value']
            print(uid, values)
            variables[uid] = values.to_list()

        return variables

    @staticmethod
    def calculate_corr_matrix(variables_df, bkpi_uids):
        corr_matrix = variables_df.corr()
        significance_threshold = 0.6
        measurements = []

        for uid in bkpi_uids:
            bkpi_corr = corr_matrix[[uid]]
            bkpi_corr = bkpi_corr.drop(uid)

            metrics = {
                "max_positive_coefficient": float(bkpi_corr.max(skipna=True).values[0]),
                "max_negative_coefficient": float(bkpi_corr.min(skipna=True).values[0]),
                "mean_abs_coefficient": float(bkpi_corr.mean(skipna=True).values[0]),
                "significant_coefficients": int(bkpi_corr[bkpi_corr.abs() > significance_threshold].count().values[0])
            }

            source = {
                "id": "correlation_matrix_",
                "type": "correlation_matrix",
                "data": {
                    "input_variables": {
                        "fields": variables_df.columns.to_list(),
                        "values": list(map(list, list(variables_df.to_numpy())))
                    },
                    "correlation_matrix": {
                        "fields": corr_matrix.columns.to_list(),
                        "values": list(map(list, list(corr_matrix.to_numpy())))
                    },
                }
            }

            print(metrics, source)

            measurements.append(MeasurementRecord(metrics=metrics, sources=source))

        return measurements

    @classmethod
    def setUpClass(cls):
        try:
            requests.get(url="{}/v1/deployments".format(cls.credentials['url']), timeout=10)
        except:
            raise unittest.SkipTest("Custom app is not available.")

        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()

        if "ICP" in get_env():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)

        prepare_env(cls.ai_client)

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_bind_custom(self):
        TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("My Custom deployment", CustomMachineLearningInstance(self.credentials))
        print("Binding uid: {}".format(self.binding_uid))
        self.assertIsNotNone(self.binding_uid)

    def test_03_get_binding_details(self):
        binding_details = self.ai_client.data_mart.bindings.get_details()
        print("Binding details: {}".format(binding_details))
        self.assertIsNotNone(binding_details)

    def test_04_get_deployments(self):
        print('Available deployments: {}'.format(self.ai_client.data_mart.bindings.get_asset_deployment_details()))
        self.ai_client.data_mart.bindings.list_assets()
        self.ai_client.data_mart.bindings.get_asset_details()

    def test_05_subscribe_custom(self):
        subscription = self.ai_client.data_mart.subscriptions.add(
            CustomMachineLearningAsset(
                source_uid='credit',
                label_column='Risk',
                prediction_column='prediction',
                probability_column='probability',
                feature_columns=['CheckingStatus', 'LoanDuration', 'CreditHistory', 'LoanPurpose', 'LoanAmount',
                                 'ExistingSavings', 'EmploymentDuration', 'InstallmentPercent', 'Sex', 'OthersOnLoan',
                                 'CurrentResidenceDuration', 'OwnsProperty', 'Age', 'InstallmentPlans', 'Housing',
                                 'ExistingCreditsCount', 'Job', 'Dependents', 'Telephone', 'ForeignWorker'],
                categorical_columns=['CheckingStatus', 'CreditHistory', 'LoanPurpose', 'ExistingSavings',
                                     'EmploymentDuration', 'Sex', 'OthersOnLoan', 'OwnsProperty', 'InstallmentPlans',
                                     'Housing', 'Job', 'Telephone', 'ForeignWorker'],
                binding_uid=self.binding_uid))

        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print('Subscription details: ', subscription.get_details())
        print("Subscription id: {}".format(self.subscription_uid))
        self.assertIsNotNone(self.subscription_uid)

    def test_06_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

    def test_07_register_correlation_monitor(self):
        monitor_name = 'BKPIs correlations'
        metrics = [
            Metric(name='max_positive_coefficient'),
            Metric(name='max_negative_coefficient'),
            Metric(name='mean_abs_coefficient'),
            Metric(name='significant_coefficients'),
        ]

        my_monitor = self.ai_client.data_mart.monitors.add(name=monitor_name, metrics=metrics)
        print('monitor definition details', my_monitor)

        TestAIOpenScaleClient.correlation_monitor_uid = self.ai_client.data_mart.monitors.get_uids(name=monitor_name)[0]
        print('monitor_uid', TestAIOpenScaleClient.correlation_monitor_uid)

        self.assertIsNotNone(my_monitor)
        self.assertIsNotNone(TestAIOpenScaleClient.correlation_monitor_uid)

    def test_08_get_corr_monitor_details(self):
        my_monitor = self.ai_client.data_mart.monitors.get_details(TestAIOpenScaleClient.correlation_monitor_uid)
        print("Monitor definition details: {}".format(my_monitor))

        self.assertTrue('BKPIs correlations' in str(my_monitor))

    def test_09_enable_corr_monitoring(self):
        thresholds = [Threshold(metric_uid='max_positive_coefficient', upper_limit=0.4)]
        TestAIOpenScaleClient.subscription.monitoring.enable(TestAIOpenScaleClient.correlation_monitor_uid, thresholds=thresholds)

        assert_custom_monitor_enablement(subscription_details=self.subscription.get_details(), monitor_uid=TestAIOpenScaleClient.correlation_monitor_uid)

    def test_10_define_and_enable_bkpi_monitor(self):
        monitor_name = 'Business KPIs'
        metrics = [
            Metric(name='revenue'),
            Metric(name='roi'),
        ]

        my_monitor = self.ai_client.data_mart.monitors.add(name=monitor_name, metrics=metrics)
        print('monitor definition details', my_monitor)

        TestAIOpenScaleClient.b_app_uid = self.ai_client.data_mart.monitors.get_uids(name=monitor_name)[0]
        print('monitor_uid', TestAIOpenScaleClient.b_app_uid)

        self.assertIsNotNone(my_monitor)
        self.assertIsNotNone(TestAIOpenScaleClient.b_app_uid)

        thresholds = [Threshold(metric_uid='revenue', lower_limit=5000)]
        TestAIOpenScaleClient.subscription.monitoring.enable(TestAIOpenScaleClient.b_app_uid, thresholds=thresholds)

        assert_custom_monitor_enablement(subscription_details=self.subscription.get_details(), monitor_uid=self.b_app_uid)

    def test_11_define_and_enable_custom_X_monitor(self):
        monitor_name = 'Custom X'
        metrics = [
            Metric(name='drift'),
            Metric(name='accuracy'),
        ]

        my_monitor = self.ai_client.data_mart.monitors.add(name=monitor_name, metrics=metrics)
        print('monitor definition details', my_monitor)

        TestAIOpenScaleClient.x_uid = self.ai_client.data_mart.monitors.get_uids(name=monitor_name)[0]
        print('monitor_uid', TestAIOpenScaleClient.x_uid)

        self.assertIsNotNone(my_monitor)
        self.assertIsNotNone(TestAIOpenScaleClient.x_uid)

        thresholds = [Threshold(metric_uid='accuracy', lower_limit=0.7)]
        TestAIOpenScaleClient.subscription.monitoring.enable(TestAIOpenScaleClient.x_uid, thresholds=thresholds)

        assert_custom_monitor_enablement(subscription_details=self.subscription.get_details(),
                                         monitor_uid=self.x_uid)

    def test_13_list_custom_monitors(self):
        self.ai_client.data_mart.monitors.list()

    def test_14_store_bkpis(self):
        def generate_kpis():
            metrics = {
                "revenue": random.randint(-5000, 30000),
                "roi": random.randint(-2000, 10000),
            }

            return metrics

        measurements = []

        for i in range(10):
            measurements.append(MeasurementRecord(metrics=generate_kpis()))

        TestAIOpenScaleClient.measurement_details = TestAIOpenScaleClient.subscription.monitoring.store_measurements(
            monitor_uid=self.b_app_uid, measurements=measurements)

        print('measurement details', TestAIOpenScaleClient.measurement_details)
        TestAIOpenScaleClient.subscription.monitoring.show_table(monitor_uid=TestAIOpenScaleClient.b_app_uid)

        bkpi_pd = TestAIOpenScaleClient.subscription.monitoring.get_table_content(monitor_uid=TestAIOpenScaleClient.b_app_uid)
        metrics_uids = self.get_metrics_list(self.ai_client, monitor_uid=TestAIOpenScaleClient.b_app_uid)

        TestAIOpenScaleClient.variables = self.get_formatted_metrics_pandas(bkpi_pd, metrics_uids)
        print(TestAIOpenScaleClient.variables.head())

    def test_15_store_X_metrics(self):
        def generate_x_metrics():
            metrics = {
                "drift": random.random(),
                "accuracy": random.random(),
            }
            return metrics

        measurements = []

        for i in range(10):
            measurements.append(MeasurementRecord(metrics=generate_x_metrics()))

        TestAIOpenScaleClient.measurement_details = TestAIOpenScaleClient.subscription.monitoring.store_measurements(
            monitor_uid=self.x_uid, measurements=measurements)

        print('measurement details', TestAIOpenScaleClient.measurement_details)
        TestAIOpenScaleClient.subscription.monitoring.show_table(monitor_uid=TestAIOpenScaleClient.x_uid)

        x_pd = TestAIOpenScaleClient.subscription.monitoring.get_table_content(monitor_uid=TestAIOpenScaleClient.x_uid)
        print(x_pd)
        metrics_uids = self.get_metrics_list(self.ai_client, monitor_uid=TestAIOpenScaleClient.x_uid)
        print(metrics_uids)

    # def test_16_get_measurement(self):
    #     measurement_uid = TestAIOpenScaleClient.measurement_details[0]['measurement_id']
    #     print('measuremnt_uid', measurement_uid)
    #
    #     measurement = TestAIOpenScaleClient.subscription.monitoring.get_measurements(monitor_uid=TestAIOpenScaleClient.correlation_monitor_uid, measurement_uid=measurement_uid)
    #     print('measurement', json.dumps(measurement, indent=2))

    def test_19_run_correlation_framework(self):
        token = self.ai_client._token
        datamart_id = self.aios_credentials['data_mart_id']
        subscription_id = TestAIOpenScaleClient.subscription_uid
        bkapp_id = "business_kpis"

        headers = {"Authorization": "Bearer {}".format(token)}

        payload = {
            "subscription_uid": "{}".format(subscription_id),
            "business_app_uid": "{}".format(bkapp_id)
        }

        endpoint_path = '{}/{}/v2/monitoring_services/correlations/monitor_instances/{}/runs/{}'.format(self.aios_credentials['url'], datamart_id, "mockedid", "mockedid")

        response = requests.put(url=endpoint_path, headers=headers, json=payload)
        print(response.status_code)
        print(response.text)

    def test_20_check_correlation_metrics(self):
        self.subscription.monitoring.show_table(monitor_uid=TestAIOpenScaleClient.correlation_monitor_uid)
        self.subscription.monitoring.print_table_schema()
        self.subscription.monitoring.describe_table(monitor_uid=TestAIOpenScaleClient.correlation_monitor_uid)

        metrics = self.subscription.monitoring.get_metrics(deployment_uid=self.deployment_uid,
                                                           monitor_uid=TestAIOpenScaleClient.correlation_monitor_uid, format='samples')
        print("Metrics:\n{}".format(metrics))

        metrics = self.subscription.monitoring.get_metrics(deployment_uid=self.deployment_uid,
                                                           monitor_uid=TestAIOpenScaleClient.correlation_monitor_uid, format='time_series')
        print("Metrics timeseries:\n{}".format(metrics))

        python_df = TestAIOpenScaleClient.subscription.monitoring.get_table_content(
            monitor_uid=TestAIOpenScaleClient.correlation_monitor_uid, format="python")
        print(python_df)

    # def test_29_disable_monitoring(self):
    #     TestAIOpenScaleClient.subscription.monitoring.disable(TestAIOpenScaleClient.correlation_monitor_uid)
    #
    # def test_30_check_issues(self):
    #     self.ai_client.data_mart.show_issues()
    #
    # def test_34_unsubscribe(self):
    #     self.ai_client.data_mart.subscriptions.delete(self.subscription.uid)
    #
    # def test_35_unbind(self):
    #     self.ai_client.data_mart.bindings.delete(self.binding_uid)
    #
    # @classmethod
    # def tearDownClass(cls):
    #     print("Deleting DataMart.")
    #     cls.ai_client.data_mart.delete()


if __name__ == '__main__':
    unittest.main()
