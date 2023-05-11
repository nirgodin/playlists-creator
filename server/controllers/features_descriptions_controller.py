from flask import Response, jsonify
from flask_restful import Resource

from server.logic.features_descriptions_manager import FeaturesDescriptionsManager


class FeaturesDescriptionsController(Resource):
    def __init__(self):
        super().__init__()
        self._features_descriptions_manager = FeaturesDescriptionsManager()

    def get(self) -> Response:
        features_descriptions = self._features_descriptions_manager.get_features_descriptions()
        res = {
            'featuresDescriptions': [features_descriptions]
        }

        return jsonify(res)
