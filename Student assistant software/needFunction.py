import pickle
import hashlib

def create_checksum(objects):
    sorted_objects = sorted(objects, key=lambda obj: obj.Id)
    # Serialize the list of objects to a bytes object
    serialized = pickle.dumps(sorted_objects)

    # Create a hash object
    hash_obj = hashlib.sha256()

    # Update the hash object with the serialized bytes object
    hash_obj.update(serialized)

    # Return the hexadecimal checksum
    return hash_obj.hexdigest()

def create_checksum_json(objects):
    sorted_objects = sorted(objects, key=lambda obj: obj["Course_id"])
    # Serialize the list of objects to a bytes object
    serialized = pickle.dumps(sorted_objects)
    # Create a hash object
    hash_obj = hashlib.sha256()
    # Update the hash object with the serialized bytes object
    hash_obj.update(serialized)
    # Return the hexadecimal checksum
    return hash_obj.hexdigest()