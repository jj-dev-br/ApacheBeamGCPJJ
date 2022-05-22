##ApacheBeamGCProject

#DataFlow #Pub/Sub #CloudStorage #GoogleCloudPlatform #ApacheBeam #GoogleBigQuery

#What does it do
    This is an experimental Apache Beam repository.
    Run data_generator.py to create data in GCP Pub/Sub. Afterwards, run Streaming.py to create a template on Cloud Storage, and use it on Data FLow to stream the data generated to your Pub/Sub subscription, fusing the data.
    You can also run batch_gcp.py to create the batch template directly on Cloud Storage, which you can use to create a Data Flow pipeline that loads data in Google Big Query.

#What do you Need
    You need a Google Cloud Platform free account and install the packages on requirements.txt.


