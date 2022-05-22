#pip install google-cloud-pubsub
#producer

import csv
import time
from google.cloud import pubsub_v1
import os

service_account_key = r'/home/joaopedro/ProjetosPessoais/ApacheBeamGCPJJ/beam-tooltorial-27aa3d535e65.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key

topico = 'projects/beam-tooltorial/topics/MeusVoos'
publisher = pubsub_v1.PublisherClient()

entrada = r'/home/joaopedro/ProjetosPessoais/ApacheBeamGCPJJ/voos_sample.csv'

with open(entrada, 'rb') as file:
    for row in file:
        print('Publishing in Topic')
        publisher.publish(topico,row)
        time.sleep(2)