from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.animal import Animal
from models.vet import Vet
import repositories.animal_repository as animal_repository
import repositories.vet_repository as vet_repository

animals_blueprint = Blueprint("animals", __name__)

@animals_blueprint.route("/animals")
def animals():
    animals = animal_repository.select_all()
    vets    = vet_repository.select_all()
    return render_template("animals/index.html", animals = animals, vets = vets)

@animals_blueprint.route("/animals/new", methods=['GET'])
def new_animal():
    vets = vet_repository.select_all()
    return render_template("animals/new.html", vets = vets)

# The POST part below is the data retrieved from the GET above
@animals_blueprint.route("/animals",  methods=['POST'])
def create_animal():
    name            = request.form['animal_name']
    date_of_birth   = request.form['date_of_birth']
    animal_type     = request.form['animal_type']
    notes           = request.form['notes']
    owner           = request.form['owner']
    vet             = vet_repository.select_by_name(request.form['vet_name'])
    animal          = Animal(name, date_of_birth, animal_type, notes, owner, vet)
    animal_repository.save(animal)
    return redirect('/animals')

@animals_blueprint.route("/animals/<id>", methods=['GET'])
def show_animal(id):
    animal = animal_repository.select(id)
    return render_template('animals/show.html', animal = animal)

# EDIT
# GET '/animals/<id>/edit'
@animals_blueprint.route("/animals/edit/<id>", methods=['GET'])
def edit_animal(id):
    animal = animal_repository.select(id)
    vets = vet_repository.select_all()
    return render_template('animals/edit.html', animal = animal, vets = vets)

# UPDATE
# PUT '/animals/<id>'
# @animals_blueprint.route("/animals/edit/<id>", methods=['POST'])
@animals_blueprint.route("/animals/<id>", methods=['POST'])
def update_animal(id):
    name            = request.form['animal_name']
    date_of_birth   = request.form['date_of_birth']
    animal_type     = request.form['animal_type']
    notes           = request.form['notes']
    owner           = request.form['owner']
    vet             = vet_repository.select_by_name(request.form['vet_name'])
    animal          = Animal(name, date_of_birth, animal_type, notes, owner, vet)
    animal_repository.update(animal)
    return redirect('/animals')

# DELETE
# DELETE '/animals/<id>'
@animals_blueprint.route("/animals/delete/<id>", methods=['POST'])
def delete_animal(id):
    animal_repository.delete(id)
    return redirect('/animals')    
