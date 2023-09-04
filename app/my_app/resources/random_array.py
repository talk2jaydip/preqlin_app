import traceback
from flask_restful import Resource
from flask import request, render_template, make_response, jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
import numpy as np

class RandomArray(Resource):
    """
    A resource for generating random arrays and processing input sentences.

    Attributes:
        None

    Methods:
        post(): Handles POST requests for generating random arrays.
    """
    @classmethod
    @jwt_required()
    def post(cls):
        """
        Handle POST requests for generating random arrays and processing input sentences.

        Args:
            None

        Returns:
            tuple: A tuple containing the response data and HTTP status code.
        """
        try:
            # Get the current user's identity from the JWT
            current_user = get_jwt_identity()

            # Get the input sentence from the request
            sentence = request.json.get('sentence')

            # Perform some processing on the input (you can replace this with your logic)
            word_count = len(sentence.split())

            # Generate a random 500-dimensional array of floats
            random_array = np.random.rand(500).tolist()

            # Create a response dictionary
            response_data = {
                'user': current_user,
                'input_sentence': sentence,
                'word_count': word_count,
                'random_array': random_array
            }

            return response_data, 200

        except Exception as e:
            return {"error": str(e)}, 500
