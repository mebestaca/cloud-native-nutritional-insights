from azure.storage.blob import BlobServiceClient

# Connect to the local Azurite storage emulator
connection_string = "UseDevelopmentStorage=true"

blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)

# Create a Blob container called "datasets"
container_name = "datasets"
container_client = blob_service_client.get_container_client(container_name)

try:
    container_client.create_container()
    print(f"Container '{container_name}' created.")
except Exception:
    print(f"Container '{container_name}' already exists.")

# Upload All_Diets.csv
blob_client = container_client.get_blob_client("All_Diets.csv")

with open("All_Diets.csv", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print("All_Diets.csv uploaded successfully to Azurite...")