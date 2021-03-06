# Copyright 2018 BLEMUNDSBURY AI LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cape_machine_reader.cape_machine_reader_model import CapeMachineReaderModelInterface
from cape_machine_reader.cape_machine_reader_core import MachineReader
import hashlib
import numpy as np
from pytest import fixture


class DummyMachineReaderModel(CapeMachineReaderModelInterface):
    """Random Scores for testing"""

    def tokenize(self, text):
        toks, spans, off = text.split(), [], 0
        for tok in toks:
            new_off = text.find(tok, off)
            spans.append((new_off, len(tok) + new_off))
            off = new_off
        return toks, spans

    def text2num(self, text):
        return int(hashlib.sha1(text.encode()).hexdigest(), 16) % 10 ** 8

    def doc2num(self, document_embedding):
        return int(np.sum(document_embedding) * 10 ** 6) % 10 ** 8

    def get_document_embedding(self, text):
        np.random.seed(self.text2num(text))
        document_tokens, _ = self.tokenize(text)
        return np.random.random((len(document_tokens), 240))

    def get_logits(self, question, document_embedding):
        question_tokens, _ = self.tokenize(question)
        n_words = document_embedding.shape[0]
        np.random.seed(self.text2num(question) + self.doc2num(document_embedding))
        start_logits = np.random.random(n_words)
        off = np.random.randint(1, 5)
        end_logits = np.concatenate([np.zeros(off) + np.min(start_logits), start_logits[off:]])
        return start_logits, end_logits


@fixture
def dummy_machine_reader_model():
    return DummyMachineReaderModel()


def test_machine_reader_objects_build(dummy_machine_reader_model):
    assert MachineReader(dummy_machine_reader_model)
