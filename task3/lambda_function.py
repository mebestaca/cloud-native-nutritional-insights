from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
import os


def process_nutritional_data_from_azurite():

    print("===== SIMULATED SERVERLESS FUNCTION STARTED =====")

    # Connect to local Azurite Blob Storage
    connection_string = "UseDevelopmentStorage=true"

    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string
    )

    container_name = "datasets"
    blob_name = "All_Diets.csv"

    print(f"Connecting to Azurite container: {container_name}")
    print(f"Downloading blob: {blob_name}")

    # Access the CSV stored in Azurite
    container_client = blob_service_client.get_container_client(
        container_name
    )

    blob_client = container_client.get_blob_client(blob_name)

    # Download CSV directly from Blob Storage
    stream = blob_client.download_blob().readall()

    print("All_Diets.csv downloaded successfully from Azurite.")

    # Load downloaded bytes into Pandas
    df = pd.read_csv(io.BytesIO(stream))

    print(f"Dataset loaded successfully: {len(df)} recipes")

    # Calculate average macronutrients for each diet
    avg_macros = (
        df.groupby("Diet_type")[
            ["Protein(g)", "Carbs(g)", "Fat(g)"]
        ]
        .mean()
        .round(2)
    )

    print("\n===== AVERAGE MACRONUTRIENTS BY DIET TYPE =====")
    print(avg_macros)

    # Convert results into NoSQL-style records
    result = avg_macros.reset_index().to_dict(orient="records")

    # Create simulated NoSQL directory
    os.makedirs("simulated_nosql", exist_ok=True)

    # Store results as JSON
    with open("simulated_nosql/results.json", "w") as file:
        json.dump(result, file, indent=4)

    print("\nResults stored in simulated_nosql/results.json")
    print("===== SIMULATED SERVERLESS FUNCTION COMPLETE =====")

    return "Data processed and stored successfully."


if __name__ == "__main__":
    print(process_nutritional_data_from_azurite())