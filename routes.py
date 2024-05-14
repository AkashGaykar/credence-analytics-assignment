from flask import Flask, request, jsonify, Blueprint
from db import movies_collection
from bson.objectid import ObjectId
from statusCode import *
from flask import current_app


# Sample data
sample_data = [
    {
        "name": "Harry Potter and the Order of the Phoenix",
        "img": "https://bit.ly/2IcnSwz",
        "summary": "Harry Potter and Dumbledore's warning about the return of Lord Voldemort is not heeded by the wizard authorities who, in turn, look to undermine Dumbledore's authority at Hogwarts and discredit Harry."
    },
    {
        "name": "The Lord of the Rings: The Fellowship of the Ring",
        "img": "https://bit.ly/2tC1Lcg",
        "summary": "A young hobbit, Frodo, who has found the One Ring that belongs to the Dark Lord Sauron, begins his journey with eight companions to Mount Doom, the only place where it can be destroyed."
    },
    {
        "name": "Avengers: Endgame",
        "img": "https://bit.ly/2Pzczlb",
        "summary": "Adrift in space with no food or water, Tony Stark sends a message to Pepper Potts as his oxygen supply starts to dwindle. Meanwhile, the remaining Avengers -- Thor, Black Widow, Captain America, and Bruce Banner -- must figure out a way to bring back their vanquished allies for an epic showdown with Thanos -- the evil demigod who decimated the planet and the universe."
    }
]

movie_blue_print = Blueprint('movie', __name__)
"""general function for creating response
"""
def create_response(reponse, status_code):
    reponse['status'] = status_code.phrase
    current_app.logger.debug(reponse)
    return (
        jsonify(reponse),
        status_code
    )
# Routes for API
"""
Getting list of all movies in database
"""
@movie_blue_print.route('/movie', methods=['GET'])
def get_movies():
    try:
        movies = list(movies_collection.find({}))
        for movie in movies:
            movie['id'] = str(movie.pop('_id'))
        current_app.logger.debug(movies)
        return create_response({'movies' : movies}, statusCode_200)
    except Exception as ex:
        current_app.logger.error(ex)
        return create_response({'error': 'exception occurred'}, Error_500)

""""
To create a new movie
"""
@movie_blue_print.route('/movie', methods=['POST'])
def add_movie():
    try:
        new_movie = request.get_json()
        db_response = movies_collection.insert_one(new_movie)
        del new_movie['_id']
        return create_response({"message": "movie saved successfully", "details": {"id": str(db_response.inserted_id),}}, statusCode_201)
    except Exception as ex:
        current_app.logger.error(ex)
        return create_response({'error': 'exception occurred'}, Error_500)

"""
To fetch the single movie details with the help od ID
"""
@movie_blue_print.route('/movie/<id>', methods=['GET'])
def get_movie(id):
    try:
        movie = movies_collection.find_one({"_id": ObjectId(id)}, {'_id': 0})
        if movie:
            return create_response({'movie': movie}, statusCode_200)
        else:
            return create_response({'error': 'Movie not found'}, Error_404)
    except Exception as ex:
        current_app.logger.error(ex)
        return create_response({'error': 'exception occurred'}, Error_500)
        
""""
Update movie details with the help of ID
"""
@movie_blue_print.route('/movie/<id>', methods=['PUT'])
def update_movie(id):
    try:
        updated_movie = request.get_json()
        result = movies_collection.update_one({'_id': ObjectId(id)}, {'$set': updated_movie})
        if result.modified_count == 1:
            return create_response({'message':'Movie Updated'}, statusCode_200)
        else:
            return create_response({'message':'No Change in movie details'}, statusCode_200)
        
    except Exception as ex:
        current_app.logger.error(ex)
        return create_response({'error': 'exception occurred'}, Error_404)


""""
Update movie name with the help of ID
"""
@movie_blue_print.route('/movie/<id>', methods=['PATCH'])
def update_movie_name(id):
    try:
        updated_movie_details = request.get_json()
        movie_name = updated_movie_details.get('name')
        movie = movies_collection.find_one({"_id": ObjectId(id)}, {'_id': 0})
        if movie is not None:
            movie['name'] = movie_name
            result = movies_collection.update_one({'_id': ObjectId(id)}, {'$set': movie})
            if result.modified_count == 1:
                return create_response({'message':'Movie Name Updated'}, statusCode_200)
            else:
                return create_response({'message':'No Change in movie name'}, statusCode_200)
        else:
            return create_response({'error': 'Movie not found'}, Error_404)
    except Exception as ex:
        current_app.logger.error(ex)
        return create_response({'error': 'exception occurred'},Error_500)
    
""""
To delete particular movie
"""
@movie_blue_print.route('/movie/<id>', methods=['DELETE'])
def delete_movie(id):
    try:
        result = movies_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return create_response({'message': 'Movie deleted'}, statusCode_200)
        else:
            return create_response({'error': 'Movie not found'}, Error_404)
    except Exception as ex:
        current_app.logger.error(ex)
        return create_response({'error': 'exception occurred'}, Error_500)
