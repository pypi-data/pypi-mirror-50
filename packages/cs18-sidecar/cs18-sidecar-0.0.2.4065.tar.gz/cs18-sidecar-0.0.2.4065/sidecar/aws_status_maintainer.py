from logging import Logger
from typing import List
from sidecar.aws_session import AwsSession
from sidecar.const import Const
from sidecar.utils import Utils
from sidecar.status_maintainer import StatusMaintainer
from sidecar.sandbox_error import SandboxError


class AWSStatusMaintainer(StatusMaintainer):
    table_data = {}

    def __init__(self, awssessionservice: AwsSession, sandbox_id: str, logger: Logger, default_region: str,
                 table_name: str):
        super().__init__(logger)
        self.default_region = default_region
        self.dynamo_resource = awssessionservice.get_dynamo_resource(default_region=self.default_region)
        self.sandboxid = sandbox_id
        self._logger = logger
        self.table_name = table_name

        self.refresh_db()

    def _item_exist_in_db(self):
        table = self.dynamo_resource.Table(self.table_name)
        response = table.get_item(
            Key={
                Const.SANDBOX_ID_TAG: self.sandboxid
            }
        )
        return True if "Item" in response else False

    def _set_table_data(self, table, sandbox_id):
        response = table.get_item(
            Key={
                Const.SANDBOX_ID_TAG: sandbox_id
            }
        )

        if "Item" in response:
            self.table_data = response["Item"]
            self._logger.info("dynamo table response for sandbox {id} is {data}".format(id=sandbox_id, data=response))
            return "Item"

        return None

    def refresh_db(self):
        table = self.dynamo_resource.Table(self.table_name)
        try:
            Utils.wait_for(func=lambda: self._set_table_data(table, self.sandboxid) is not None,
                           interval_sec=1,
                           max_retries=5,
                           error='No sandbox data available')
        except Exception:
            self._logger.exception("Failed to get sandbox data from dynamodb after 5 times")
            return

    def update_qualiy_status(self, status: str):
        if not self._item_exist_in_db():
            return

        table = self.dynamo_resource.Table(self.table_name)
        response = table.update_item(
            Key={Const.SANDBOX_ID_TAG: self.sandboxid},
            UpdateExpression="set #f = :r",
            ExpressionAttributeValues={':r': status},
            ExpressionAttributeNames={"#f": Const.QUALIY_STATUS},
            ReturnValues="UPDATED_NEW"
        )

        if self.response_failed(response):
            raise Exception(f"Failed to update QualiY status '{status}' in sandbox '{self.sandboxid}'\n"
                            f"Response: {response}")

    def update_service_in_dynamo(self):
        if not self._item_exist_in_db():
            return

        table = self.dynamo_resource.Table(self.table_name)
        return table.update_item(
            Key={
                Const.SANDBOX_ID_TAG: self.sandboxid
            },
            UpdateExpression="set services = :r",
            ExpressionAttributeValues={
                ':r': self.table_data["services"]
            },
            ReturnValues="UPDATED_NEW"
        )

    def get_deployment_outputs(self, entity_name: str) -> {}:
        if entity_name in self.table_data["services"]:
            return self.table_data["services"][entity_name].get("outputs", {})

        for logical_id, logical_details in self.table_data["apps"].items():
            for instance_id, instance_json in logical_details['instances'].items():
                for app_name, app_details in instance_json['apps'].items():
                    if app_name == entity_name:
                        return app_details.get('outputs', {})
        raise Exception(f"could not find service/application with name '{entity_name}'")

    def get_service_deployment_outputs(self, service_name: str) -> {}:
        service = self.table_data["services"].get(service_name)
        if service:
            return service.get("outputs", {})
        raise Exception(f"could not find service with name '{service_name}'")

    def get_app_deployment_outputs(self, app_name: str) -> {}:
        app_details = self._get_first_application(app_name)
        if app_details:
            return app_details.get('outputs', {})
        raise Exception(f"could not find application with name '{app_name}'")

    def _get_first_application(self, app_name: str):
        for logical_id, logical_details in self.table_data["apps"].items():
            for instance_id, instance_json in logical_details['instances'].items():
                for name, app_details in instance_json['apps'].items():
                    if name == app_name:
                        return app_details
        return None

    def update_service_outputs(self, service_name: str, outputs: {}):
        if not self._item_exist_in_db():
            return

        self.table_data["services"][service_name]["outputs"] = outputs
        response = self.update_service_in_dynamo()
        if self.response_failed(response):
            self._logger.error(
                "error while updating service '{SERVICE}' outputs in sandbox '{SANDBOX}'. {RESPONSE}".format(
                    SERVICE=service_name,
                    SANDBOX=self.sandboxid,
                    RESPONSE=response))

    def update_app_instance_outputs(self, instance_logical_id, instance_id, app_name, outputs: {}):
        if not self._item_exist_in_db():
            return

        try:
            self.add_instance_to_data_table_if_not_exists(instance_id, instance_logical_id)
        except Exception as ex:  # log details for debugging, related to bug #1689
            self._logger.exception('fail to update instance outputs. instance_logical_id: {}, table_data: {}, exc={}'
                                   .format(instance_logical_id, self.table_data, str(ex)))
            raise ex

        app_details = self.table_data["apps"][instance_logical_id]["instances"][instance_id]["apps"] \
            .setdefault(app_name, {})

        app_details["outputs"] = outputs

        response = self.update_apps_in_dynamo()

        if self.response_failed(response):
            self._logger.error(
                "error while updating app instance outputs(sandbox_id: {sandbox_id}. app_name: "
                "{app}. instance_id: {instance_id})\n"
                "Response: {data}"
                    .format(sandbox_id=self.sandboxid, app=app_name, instance_id=instance_id, data=response))

    def update_service_status(self, name: str, status: str):
        if not self._item_exist_in_db():
            return

        self.table_data["services"][name]["status"] = status
        response = self.update_service_in_dynamo()
        if self.response_failed(response):
            self._logger.error(
                "error while updating service '{SERVICE}' status in sandbox '{SANDBOX}'. {RESPONSE}".format(
                    SERVICE=name,
                    SANDBOX=self.sandboxid,
                    RESPONSE=response))

    def update_app_instance_status(self, instance_logical_id, instance_id, app_name, status_tag, status):
        if not self._item_exist_in_db():
            return

        try:
            self.add_instance_to_data_table_if_not_exists(instance_id, instance_logical_id)
        except Exception as ex:  # log details for debugging, related to bug #1689
            self._logger.exception('fail to update instance status. instance_logical_id: {}, table_data: {}, exc={}'
                                   .format(instance_logical_id, self.table_data, str(ex)))
            raise ex

        app_details = self.table_data["apps"][instance_logical_id]["instances"][instance_id]["apps"]\
            .setdefault(app_name, {})

        app_details[status_tag] = status

        response = self.update_apps_in_dynamo()

        if self.response_failed(response):
            self._logger.error(
                "Error update_app_instance_status(sandbox_id: {sandbox_id}. app_name: {app}. instance_id: {instance_id})\n"
                "Response: {data}"
                    .format(sandbox_id=self.sandboxid, app=app_name, instance_id=instance_id, data=response))

    def update_apps_in_dynamo(self):
        if not self._item_exist_in_db():
            return

        table = self.dynamo_resource.Table(self.table_name)
        response = table.update_item(
            Key={
                Const.SANDBOX_ID_TAG: self.sandboxid
            },
            UpdateExpression="set " + "apps" + " = :r",
            ExpressionAttributeValues={
                ':r': self.table_data["apps"]
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def add_instance_to_data_table_if_not_exists(self, instance_id, instance_logical_id):
        if instance_id not in self.table_data["apps"][instance_logical_id]["instances"]:
            self.table_data["apps"][instance_logical_id]["instances"][instance_id] = \
                {
                    "apps": {}
                }

    def update_lazy_load_artifacts_waiting(self, value: bool):
        if not self._item_exist_in_db():
            return

        table = self.dynamo_resource.Table(self.table_name)

        response = table.update_item(
            Key={
                Const.SANDBOX_ID_TAG: self.sandboxid
            },
            UpdateExpression="set #f = :r",
            ExpressionAttributeValues={
                ':r': value
            },
            ExpressionAttributeNames={
                "#f": Const.LAZY_LOAD_ARTIFACTS_WAITING
            },
            ReturnValues="UPDATED_NEW"
        )

        if self.response_failed(response):
            self._logger.error("Error update_lazy_load_artifacts_waiting(sandbox_id: {sandbox_id} value: {value})\n"
                               "Response: {data}"
                               .format(sandbox_id=self.sandboxid, value=value, data=response))

    def update_sandbox_errors(self, errors: List[SandboxError]):
        if not self._item_exist_in_db():
            return

        table = self.dynamo_resource.Table(self.table_name)

        errors_to_db = [{"message": error.message, "code": error.code, "time": error.time} for error in errors]

        response = table.update_item(
            Key={
                Const.SANDBOX_ID_TAG: self.sandboxid
            },
            UpdateExpression="set #f = :r",
            ExpressionAttributeValues={
                ':r': errors_to_db
            },
            ExpressionAttributeNames={
                "#f": Const.SANDBOX_ERRORS
            },
            ReturnValues="UPDATED_NEW"
        )

        if self.response_failed(response):
            self._logger.error("Error update_sandbox_errors(sandbox_id: {sandbox_id} errors: {errors})\n"
                               "Response: {data}"
                               .format(sandbox_id=self.sandboxid, errors=errors_to_db, data=response))


    def update_sandbox_end_status(self, sandbox_deployment_end_status: str):
        if not self._item_exist_in_db():
            return

        table = self.dynamo_resource.Table(self.table_name)

        response = table.update_item(
            Key={
                Const.SANDBOX_ID_TAG: self.sandboxid
            },
            UpdateExpression="set #f = :r, #newend = :r",
            ExpressionAttributeValues={
                ':r': sandbox_deployment_end_status
            },
            ExpressionAttributeNames={
                "#f": Const.SANDBOX_DEPLOYMENT_END_STATUS,
                "#newend": Const.SANDBOX_DEPLOYMENT_END_STATUS_v2
            },
            ReturnValues="UPDATED_NEW"
        )

        if self.response_failed(response):
            self._logger.error("Error update_sandbox_end_status(sandbox_id: {sandbox_id} status: {status})\n"
                               "Response: {data}"
                               .format(sandbox_id=self.sandboxid, status=sandbox_deployment_end_status, data=response))

    def update_sandbox_start_status(self, sandbox_start_time):
        if not self._item_exist_in_db():
            return

        table = self.dynamo_resource.Table(self.table_name)

        response = table.update_item(
            Key={
                Const.SANDBOX_ID_TAG: self.sandboxid
            },
            UpdateExpression="set #f = :r, #newstart = :r",
            ExpressionAttributeValues={
                ':r': str(sandbox_start_time)
            },
            ExpressionAttributeNames={
                "#f": Const.SANDBOX_START_TIME,
                "#newstart": Const.SANDBOX_START_TIME_v2
            },
            ReturnValues="UPDATED_NEW"
        )

        if self.response_failed(response):
            self._logger.error("Error update_sandbox_start_status(sandbox_id: {sandbox_id} status: {status})\n"
                               "Response: {data}"
                               .format(sandbox_id=self.sandboxid, status=sandbox_start_time, data=response))

    def get_all_app_names_for_instance(self, logical_id: str):
        return self.table_data["spec"]["expected_apps"][logical_id]["apps"]

    @staticmethod
    def response_failed(response: dict) -> bool:
        return not response.get("ResponseMetadata") and \
               not response.get("ResponseMetadata").get("HTTPStatusCode") == 200

    def get_ingress_routes(self) -> List['IngressRouteRequest']:
        items = []
        for ingress_route in self.table_data.get('ingress_routes', []):
            items.append(IngressRouteRequest(
                listener_port=int(ingress_route['listener_port']),
                path=ingress_route['path'],
                host=ingress_route['host'],
                app_name=ingress_route['app_name'],
                app_port=int(ingress_route['app_port']),
                color=ingress_route['color']))
        return items

    def get_sandbox_errors(self) -> List[SandboxError]:
        self.refresh_db()
        errors = []
        for error in self.table_data.get(Const.SANDBOX_ERRORS, []):
            errors.append(SandboxError(message=str(error["message"]),
                                       code=str(error["code"]),
                                       time=str(error["time"])))
        return errors

    def get_terminating_flag(self) -> bool:
        table = self.dynamo_resource.Table(self.table_name)

        response = table.get_item(
            Key={Const.SANDBOX_ID_TAG: self.sandboxid},
            ConsistentRead=True,
            ProjectionExpression='terminating'
        )

        if "Item" in response:
            doc = response["Item"]
            if 'terminating' in doc:
                return doc['terminating']

        return False


class IngressRouteRequest:
    def __init__(self, listener_port: int, path: str, host: str, app_port: int, app_name: str, color: str):
        self.listener_port = listener_port
        self.path = path
        self.host = host
        self.app_port = app_port
        self.app_name = app_name
        self.color = color
