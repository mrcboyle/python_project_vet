from db.run_sql import run_sql
from models.animal import Animal
from models.owner import Owner
from models.vet import Vet
import repositories.animal_repository as animal_repository
import repositories.vet_repository as vet_repository

# CREATE

def save(animal):
    sql = "INSERT INTO animals (name, dob, animal_type, notes, owner, vet_id) VALUES (?, ?, ?, ?, ?, ?) RETURNING *"
    values = [animal.name, animal.dob, animal.animal_type, animal.notes, animal.owner, animal.vet.id]
    print(values)
    results = run_sql(sql, values)
    id = results[0]['id']
    # what does this part do????????    
    animal.id = id
    return animal

# READ

def select_all():
    animals = [] # create an empty list
    sql = "SELECT * FROM animals"
    results = run_sql(sql) # returns rows in sql format

    for row in results:
        # convert to python format below
        # We have to tell Animals what the vet data is (thanks Nadia!)
        vet = vet_repository.select(row['vet_id'])
        # Then below, we pass in the variable vet (above) into the array. This allow the html to see the Vet name and id.
        animal = Animal(row['name'], row['dob'], row['animal_type'], row['notes'], row['owner'], vet, row['id'])
        animals.append(animal)
    return animals

def select(id):
    animal = None
    sql = "SELECT * FROM animals WHERE id = ?"
    values = [id]
    result = run_sql(sql, values)[0]
    # Again, we have to tell Animals what the vet data is  
    vet = vet_repository.select(result['vet_id'])
    if result is not None:
        # And pass the variable in below again, instead of the normal result. 
        animal = Animal(result['name'], result['dob'], result['animal_type'], result['notes'], result['owner'], vet, result['id'])
    return animal

# UPDATE

def update(animal):
    sql = "UPDATE animals SET (name, dob, animal_type, notes, owner, vet_id) = ( ?, ?, ?, ?, ?, ?) WHERE id = ?"

    values = [animal.name, animal.dob, animal.animal_type, animal.notes, animal.owner, animal.vet.id, animal.id]    
    run_sql(sql, values)

# DELETE

def delete_all():
    sql = "DELETE FROM animals"
    run_sql(sql)

def delete(id):
    sql = "DELETE FROM animals WHERE id = ?"
    values = [id]
    # if values = id (above) why don't we just return id in the run_sql below?
    run_sql(sql, values)