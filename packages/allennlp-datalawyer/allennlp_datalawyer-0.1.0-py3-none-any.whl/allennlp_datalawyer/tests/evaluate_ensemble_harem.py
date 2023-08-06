# coding: utf-8

from allennlp_datalawyer.models import CrfTaggerEnsemble
from allennlp_datalawyer.predictors import SentenceTaggerPredictor
from allennlp.common import Params
from allennlp.data import DatasetReader
from allennlp.common.util import lazy_groups_of
from typing import List, Iterator
from allennlp.data import Instance
import logging, os, fire

log = logging.getLogger('allennlp')


config_path = 'ner_elmo_harem_ensemble.jsonnet'
document_path = '/home/pedro/repositorios/entidades/dataset/harem/harem_test_selective_iberlef.txt'
cuda_device = -1
predictions_file = 'predictions_iberlef_on_harem'
scores_file = 'scores_iberlef_on_harem'
batch_size = 64


def get_instance_data(document_path) -> Iterator[Instance]:
    yield from predictor._dataset_reader.read(document_path)


def predict_instances(batch_data: List[Instance]) -> Iterator[str]:
    yield predictor.predict_batch_instance(batch_data)


params = Params.from_file(config_path)
model = CrfTaggerEnsemble.from_params(vocab=None, params=params)
for submodel in model.submodels:
    if cuda_device >= 0:
        submodel.cuda(cuda_device)
    else:
        submodel.cpu()
dataset_reader = DatasetReader.from_params(params.pop('dataset_reader'))
predictor = SentenceTaggerPredictor(model, dataset_reader)

count = 0

predictions_file = predictions_file + '.txt'
scores_file = scores_file + '.txt'

with open(predictions_file, mode='w', encoding='utf8') as out_file:
    for batch in lazy_groups_of(get_instance_data(document_path), batch_size):
        for _, results in zip(batch, predict_instances(batch)):
            for idx, result in enumerate(results):
                count += 1
                real_sentence = batch[idx]
                real_tags = real_sentence.fields['tags'].labels
                words = result['words']
                predicted_labels = result['tags']
                for word_idx, (word, tag) in enumerate(zip(words, predicted_labels)):
                    out_file.write(' '.join([word, real_tags[word_idx], tag]) + '\n')
                out_file.write('\n')
                if count % 200 == 0:
                    log.info('Predicted %d sentences' % count)
            out_file.write('\n')
out_file.close()
log.info('Finished predicting %d sentences' % count)
os.system("./%s -l < %s > %s" % ('conlleval.perl', predictions_file, scores_file))
print(open(scores_file, mode='r', encoding='utf8').read())
