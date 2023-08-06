import os
import warnings
from typing import Any, Dict, Optional, Text

import editdistance
import rasa.utils.io
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.extractors import EntityExtractor
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.utils import write_json_to_file

__all__ = ['FuzzyEntitySynonymMapper']


class FuzzyEntitySynonymMapper(EntityExtractor):
    provides = ["entities"]

    defaults = {
        "fuzzy_matching": False,
        "fuzzy_threshold": 90
    }

    def __init__(
            self,
            component_config: Optional[Dict[Text, Text]] = None,
            synonyms: Optional[Dict[Text, Any]] = None,
            synonyms_by_entity: Optional[Dict[str, Dict[str, str]]] = None
    ) -> None:

        super(FuzzyEntitySynonymMapper, self).__init__(component_config)

        self.synonyms = synonyms if synonyms else {}
        self.synonyms_by_entity = synonyms_by_entity or {}

    def train(
            self, training_data: TrainingData, config: RasaNLUModelConfig,
            **kwargs: Any
    ) -> None:
        for key, value in list(training_data.entity_synonyms.items()):
            self.add_entities_if_synonyms(key, value)

        for example in training_data.entity_examples:
            for entity in example.get("entities", []):
                entity_val = example.text[entity["start"]: entity["end"]]
                self.add_entities_if_synonyms(entity_val,
                                              str(entity.get("value")))

        for item in training_data.lookup_tables:
            entity = item['name']
            elements = item['elements']

            if entity not in self.synonyms_by_entity:
                self.synonyms_by_entity[entity] = {}

            for element in elements:
                value = self.synonyms.get(element, value)
                if value:
                    self.synonyms_by_entity[entity][element] = value
                    self.synonyms_by_entity[entity][value] = value

    def process(self, message: Message, **kwargs: Any) -> None:

        updated_entities = message.get("entities", [])[:]
        self.replace_synonyms(updated_entities)
        self.remap_entities(updated_entities)
        message.set("entities", updated_entities, add_to_output=True)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[
        Dict[Text, Any]]:

        if self.synonyms:
            file_name = file_name + ".json"
            entity_synonyms_file = os.path.join(model_dir, file_name)
            write_json_to_file(
                entity_synonyms_file, {
                    'synonyms': self.synonyms,
                    'synonyms_by_entity': self.synonyms_by_entity
                }, separators=(",", ": ")
            )
            return {"file": file_name}
        else:
            return {"file": None}

    @classmethod
    def load(
            cls,
            meta: Dict[Text, Any],
            model_dir: Optional[Text] = None,
            model_metadata: Optional[Metadata] = None,
            cached_component: Optional["FuzzyEntitySynonymMapper"] = None,
            **kwargs: Any
    ) -> "FuzzyEntitySynonymMapper":

        file_name = meta.get("file")
        if not file_name:
            synonyms = None
            return cls(meta, synonyms)

        entity_synonyms_file = os.path.join(model_dir, file_name)
        if os.path.isfile(entity_synonyms_file):
            data = rasa.utils.io.read_json_file(entity_synonyms_file)
            synonyms = data['synonyms']
            synonyms_by_entity = data['synonyms_by_entity']
        else:
            synonyms = None
            synonyms_by_entity = None
            warnings.warn(
                "Failed to load synonyms file from '{}'".format(
                    entity_synonyms_file)
            )
        return cls(meta, synonyms, synonyms_by_entity)

    def remap_entities(self, entities):
        for entity in entities:
            value = entity['value']
            name = entity['entity']

            synonyms = self.synonyms_by_entity.get(name, {})
            if value not in synonyms:
                print('invalid mapping for entity %r with value %r' %
                      (name, value))
                for e in self.synonyms_by_entity:
                    if value in self.synonyms_by_entity[e]:
                        print('remapping value %r from entity %r to %r' %
                              (value, name, e))
                        entity['entity'] = e
                        entity['value'] = self.synonyms_by_entity[e][value]

    def replace_synonyms(self, entities):
        for entity in entities:
            # need to wrap in `str` to handle e.g. entity values of type int
            entity_value = str(entity["value"])
            if entity_value.lower() in self.synonyms:
                entity["value"] = self.synonyms[entity_value.lower()]
                self.add_processor_name(entity)
            else:
                self.fuzzy_match_entity(entity)

    def add_entities_if_synonyms(self, entity_a, entity_b):
        if entity_b is not None:
            original = str(entity_a)
            replacement = str(entity_b)

            if original != replacement:
                original = original.lower()
                if original in self.synonyms and self.synonyms[
                    original] != replacement:
                    warnings.warn(
                        "Found conflicting synonym definitions "
                        "for {}. Overwriting target {} with {}. "
                        "Check your training data and remove "
                        "conflicting synonym definitions to "
                        "prevent this from happening."
                        "".format(
                            repr(original),
                            repr(self.synonyms[original]),
                            repr(replacement),
                        )
                    )

                self.synonyms[original] = replacement

    def fuzzy_match_entity(self, entity):
        entity_value = str(entity["value"])

        fuzzy_match = None
        for w in self.synonyms.keys():
            value = self.get_fuzzy_match_value(w, entity_value, fuzzy_match)
            fuzzy_match = value if value else fuzzy_match

        if fuzzy_match:
            entity["value"] = self.synonyms[fuzzy_match[1]]
            self.add_processor_name(entity)

    def get_fuzzy_match_value(self, word, value, fuzzy):
        """
        Returns a tuple of similarity and value between 2 strings
        This converts the editdistance to a percentage
        Based on the equation used here:
        https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.ratio
        :param word:
        :param value:
        :return:
        """
        threshold = self.component_config["fuzzy_threshold"]
        distance = editdistance.eval(value, word)
        matches = max(len(word), len(value)) - distance
        similarity = 2 * matches / (len(word) + len(value)) * 100
        if similarity >= threshold:
            return max((similarity, word), fuzzy) \
                if fuzzy else (similarity, word)
        return None
