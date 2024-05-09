from flask import Flask, request, jsonify
from bson.objectid import ObjectId
from db import movies_collection

app = Flask(__name__)


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


# Routes for API
@app.route('/movie', methods=['GET'])
def get_movies():
    movies = list(movies_collection.find({}, {'_id': 0}))
    return jsonify(movies)

@app.route('/movie', methods=['POST'])
def add_movie():
    new_movie = request.get_json()
    db_response = movies_collection.insert_one(new_movie)
    del new_movie['_id']
    return jsonify({"message": "movie saved successfully", "details": {"id": str(db_response.inserted_id),}}), 201


@app.route('/movie/<id>', methods=['GET'])
def get_movie(id):
    movie = movies_collection.find_one({"_id": ObjectId(id)}, {'_id': 0})
    if movie:
        return jsonify(movie)
    else:
        return jsonify({'error': 'Movie not found'}), 404

@app.route('/movie/<id>', methods=['PUT'])
def update_movie(id):
    updated_movie = request.get_json()
    result = movies_collection.update_one({'_id': ObjectId(id)}, {'$set': updated_movie})
    if result.modified_count == 1:
        return jsonify({'message':'Movie Updated'})
    else:
        return jsonify({'error': 'Movie not found'}), 404

@app.route('/movie/<id>', methods=['DELETE'])
def delete_movie(id):
    result = movies_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Movie deleted'}), 200
    else:
        return jsonify({'error': 'Movie not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)