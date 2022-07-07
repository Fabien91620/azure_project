from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.storage.blob.blockblobservice import BlockBlobService

from msrest.authentication import CognitiveServicesCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient

import os
import credentials


def get_computer_vision():
    computervision_client = ComputerVisionClient(credentials.COG_ENDPOINT,
                                                 CognitiveServicesCredentials(credentials.COG_KEY))

    return computervision_client


def get_connection_azure():
    account_name = 'stockageprojet'
    account_key = os.environ['ACCOUNT_KEY']  # en attendant, variable d'environnement
    block_blob_service = BlockBlobService(
        account_name=account_name,
        account_key=account_key
    )
    return block_blob_service


def add_image_in_azure(path, blob_name):
    pass
    # azure.create_blob_from_path(container_name=container_name, blob_name=blob_name, file_path=path)


def create_or_update_ressource_group(credential):
    resource_client = ResourceManagementClient(credential, credentials.SUBSCRIPTION_ID)
    rg_result = resource_client.resource_groups.create_or_update(credentials.SUBSCRIPTION_ID,
                                                                 {"location": credentials.LOCATION})
    print(f"Provisioned resource group {rg_result.name}")

    return rg_result


def create_storage_account(credential):
    storage_client = StorageManagementClient(credential, credentials.SUBSCRIPTION_ID)

    availability_result = storage_client.storage_accounts.check_name_availability(
        {"name": credentials.SA_NAME}
    )

    if not availability_result.name_available:
        print(f"Storage name {credentials.SA_NAME} is already in use. Try another name.")
        exit()

    poller = storage_client.storage_accounts.begin_create(credentials.RG_NAME, credentials.SA_NAME,
                                                          {
                                                              "location": credentials.LOCATION,
                                                              "kind": "Storage",
                                                              "sku": {"name": "Standard_LRS"}
                                                          })

    account_result = poller.result()
    print(f"Provisioned storage account {account_result.name}")

    return account_result


if __name__ == "__main__":
    pass
    # cmd = subprocess.run(["az group create", "--name", "gr-azure-project", "--location", "westeurope"], capture_output=True, text=True)
    # print(cmd.stdout)

    # cred = AzureCliCredential()
    #
    # ressource_group = create_or_update_ressource_group(cred)
    # storage_account = create_storage_account(cred)
    # print(ressource_group)
    # print(storage_account)

    # container_name = 'projetazure'

    # azure = get_connection_azure()
    # computer_vision = get_computer_vision()
