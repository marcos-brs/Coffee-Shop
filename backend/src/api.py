import json
import os

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from sqlalchemy import exc

from .auth.auth import AuthError, requires_auth
from .database.models import db_drop_and_create_all, setup_db, Drink

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# ROUTES
'''
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where
    drinks is the list of drinks or appropriate status code indicating reason 
    for failure
'''


@app.route('/drinks', methods=['GET'])
def list_drinks():
    drinks = Drink.query.all()
    formatted_drinks = [drink.short() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': formatted_drinks
    })


'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where 
    drinks is the list of drinks or appropriate status code indicating reason 
    for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def list_drinks_detail(f):
    drinks = Drink.query.all()
    formatted_drinks = [drink.long() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': formatted_drinks
    })


'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where 
    drink an array containing only the  newly created drink or appropriate 
    status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(f):
    try:
        data = dict(request.form or request.json or request.data)
        title = data.get('title')
        recipe = data.get('recipe')

        if type(recipe) != str:
            recipe = json.dumps(recipe)

        new_drink = Drink(title=title, recipe=recipe)
        new_drink.insert()
        return jsonify({
            'success': True,
            'drinks': new_drink.long()
        })
    except:
        abort(422)


'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where 
    drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(f, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        data = dict(request.form or request.json or request.data)
        title = data.get('title', None)
        recipe = data.get('recipe', None)

        if title == None and recipe == None:
            abort(400)

        if title != None:
            drink.title = title

        if recipe != None:
            if type(recipe) != str:
                recipe = json.dumps(recipe)
            drink.recipe = recipe

        drink.update()

        return jsonify({
            'success': True,
            'drinks': drink.long()
        })
    except:
        abort(422)


'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id 
    is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(f, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        drink.delete()

        return jsonify({
            'success': True,
            'delete': id
        })
    except:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable Entity"
    }), 422


'''
implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
    }), 422


'''
implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    Receive the raised authorization error and propagates it as response
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
