#!/usr/bin/python3
"""places_amenities views"""
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.amenity import Amenity
from os import getenv
from models import storage

db_storage = (getenv("HBNB_TYPE_STORAGE") == db)


@app_views.route('/places/<place_id>/amenities', 
                 methods=["GET"])
def get_place_amenities(place_id):
    """
    Get a list of all amenites associated with place
    (place_id)
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([a.to_dict() for a in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """
    Delete (amenity_id) associated with
    place identified by (place_id)
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    place_amenities = place.amenities
    place_amenity = list(filter(lambda a: a.id == amenity_id, place_amenities))
    if not place_amenity:
        abort(404)
    if db_storage:
        place.amenities.remove(place_amenity[0])
    else:
        place.amenity_ids.remove(place_amenity[0].id)
    place.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """
    Delete amenity (amenity_id) associated with
    place (place_id)
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    place_amenities = place.amenities
    place_amenity = list(filter(lambda a: a.id == amenity_id, place_amenities))
    if place_amenity:
        return jsonify(amenity.to_dict())
    if db_storage:
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)