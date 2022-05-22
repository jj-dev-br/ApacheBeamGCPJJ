import apache_beam as beam
import os
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam import window

pipeline_options = {
  "project": "beam-tooltorial",
  "runner": "DataFlowRunner",
  "region": "southamerica-east1",
  "staging_location":"gs://beam-tooltorial/temp",
  "temp_location":"gs://beam-tooltorial/temp",
  "template_location":"gs://beam-tooltorial/template/streaming_sliding",
  "save_main_session": True ,
  "streaming" : True }

pipeline_options = PipelineOptions.from_dictionary(pipeline_options)
p1 = beam.Pipeline(options=pipeline_options)

serviceAccount = r'/home/joaopedro/ProjetosPessoais/ApacheBeamGCPJJ/beam-tooltorial-27aa3d535e65.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= serviceAccount

subscription = 'projects/beam-tooltorial/subscriptions/MeusVoos-Sub'
saida = 'projects/beam-tooltorial/topics/saida'

class separar_linhas(beam.DoFn):
  def process(self,record):
    return [record.decode("utf-8").split(',')]

class filtro(beam.DoFn):
  def process(self,record):
    if int(record[8]) > 0:
      return [record]

pcollection_entrada = (
    p1  | 'Read from pubsub topic' >> beam.io.ReadFromPubSub(subscription=subscription)
)

Tempo_Atrasos = (
  pcollection_entrada
  | "Separar por Vírgulas Atraso" >> beam.ParDo(separar_linhas())
  | "Pegar voos com atraso" >> beam.ParDo(filtro())
  | "Criar par atraso" >> beam.Map(lambda record: (record[4],int(record[8])))
  | "Window" >> beam.WindowInto(window.SlidingWindows(10,5))
  | "Somar por key" >> beam.CombinePerKey(sum)
)

Qtd_Atrasos = (
  pcollection_entrada
  | "Separar por Vírgulas Qtd" >> beam.ParDo(separar_linhas())
  | "Pegar voos com Qtd" >> beam.ParDo(filtro())
  | "Criar par Qtd" >> beam.Map(lambda record: (record[4],int(record[8])))
  | "Window Atr" >> beam.WindowInto(window.SlidingWindows(10,5))
  | "Contar por key" >> beam.combiners.Count.PerKey()
)

tabela_atrasos = (
    {'Qtd_Atrasos':Qtd_Atrasos,'Tempo_Atrasos':Tempo_Atrasos}
    | "join Atrasos e Qtd" >> beam.CoGroupByKey()
    | 'Converting to byte String' >> beam.Map(lambda row: (''.join(str(row)).encode('utf-8')) )
    | "Escrever no Tópico" >> beam.io.WriteToPubSub(saida)
)

result = p1.run()
result.wait_until_finish()