# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import logging
import os
from time import time

from annoy import AnnoyIndex

from doc_explanation.search.doc_search.sentence import ChunkedSentence

from .basic import BasicEmbeddingsIndex

log = logging.getLogger(__name__)

CACHE_FOLDER = os.path.join(os.getcwd(), ".cache")


class VectorSearch:
    """Basic implementation of a knowledge base."""

    def __init__(self, list_sentence: list[ChunkedSentence], embedding_model: str, embedding_size: int = 384):
        self.list_sentence: list[ChunkedSentence] = list_sentence
        self.index = None
        self.embedding_size = embedding_size
        self.embedding_model = embedding_model
        self.build()

    def build(self):
        """Builds the knowledge base index."""
        t0 = time()
        all_text_items = []
        for chunked_sentence in self.list_sentence:
            text = chunked_sentence.text
            all_text_items.append(text)

        # We compute the md5
        md5_hash = hashlib.md5("".join(all_text_items).encode("utf-8")).hexdigest()
        cache_file = os.path.join(CACHE_FOLDER, f"{md5_hash}.ann")

        # If we have already computed this before, we use it
        if os.path.exists(cache_file):
            # TODO: this should not be hardcoded. Currently set for all-MiniLM-L6-v2.
            ann_index = AnnoyIndex(self.embedding_size, "angular")
            ann_index.load(cache_file)

            self.index = BasicEmbeddingsIndex(embedding_model=self.embedding_model, index=ann_index)
            self.index.add_items(self.list_sentence)
        else:
            self.index = BasicEmbeddingsIndex(self.embedding_model)
            self.index.add_items(self.list_sentence)
            self.index.build()

            # We also save the file for future use
            os.makedirs(CACHE_FOLDER, exist_ok=True)
            self.index.embeddings_index.save(cache_file)

        log.info(f"Building the Knowledge Base index took {time() - t0} seconds.")

    def search_relevant_chunks(self, text, max_results: int = 3) -> list[ChunkedSentence]:
        """Search the index for the most relevant chunks."""
        if self.index is None:
            return []

        results = self.index.search(text, max_results=max_results)

        # Return the result directly
        return results
