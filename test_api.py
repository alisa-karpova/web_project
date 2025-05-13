from requests import get, post, delete

"""get all snowboards"""
print(get('http://localhost:8000/api/snbs').json())

"""get only one of them"""
# bad request (wrong snb_id)
print(get('http://localhost:8000/api/snbs/999').json())

# bad request (wrong type)
print(get('http://localhost:8000/api/n1').json())

# correct request
print(get('http://localhost:8000/api/snbs/1').json())


"""add a snowboard"""
# empty request
print(post('http://localhost:8000/api/snbs', json={}).json())

# bad request (not enough keys)
print(post('http://localhost:8000/api/snbs', json={"owner_id": 2, "owner_level": "beginner"}).json())

# bad request (wrong owner_id)
print(post('http://localhost:8000/api/snbs', json={"owner_id": 32,
                                                   "owner_height": 167,
                                                   "owner_weight": 78,
                                                   "owner_style": "freeride",
                                                   "owner_level": "pro",
                                                   "high_tramps": False}).json())

# # bad request (read an output message)
print(post('http://localhost:8000/api/snbs', json={"owner_id": 2,
                                                   "owner_height": 167,
                                                   "owner_weight": 78,
                                                   "owner_style": "freeride",
                                                   "owner_level": "pro",
                                                   "high_tramps": True}).json())

# correct request
print(post('http://localhost:8000/api/snbs', json={"owner_id": 2,
                                                   "owner_height": 167,
                                                   "owner_weight": 78,
                                                   "owner_style": "carving",
                                                   "owner_level": "experienced",
                                                   "high_tramps": False}).json())

# check result
print(get('http://localhost:8000/api/snbs').json())


"""edit a snowboard"""
# empty request
print(post('http://localhost:8000/api/snbs/2', json={}).json())

# bad request (not enough keys)
print(post('http://localhost:8000/api/snbs/2', json={"owner_id": 2, "owner_level": "beginner"}).json())

# bad request (wrong snb_id)
print(post('http://localhost:8000/api/snbs/22', json={"owner_id": 2,
                                                      "owner_height": 167,
                                                      "owner_weight": 78,
                                                      "owner_style": "freeride",
                                                      "owner_level": "pro",
                                                      "high_tramps": True}).json())

# bad request (wrong type)
print(post('http://localhost:8000/api/snbs/n2', json={"owner_id": 2,
                                                      "owner_height": 167,
                                                      "owner_weight": 78,
                                                      "owner_style": "freeride",
                                                      "owner_level": "pro",
                                                      "high_tramps": True}).json())

# bad request (read an output message)
print(post('http://localhost:8000/api/snbs/2', json={"owner_id": 2,
                                                     "owner_height": 167,
                                                     "owner_weight": 78,
                                                     "owner_style": "freeride",
                                                     "owner_level": "pro",
                                                     "high_tramps": True}).json())

# correct request
print(post('http://localhost:8000/api/snbs/2', json={"owner_id": 2,
                                                     "owner_height": 167,
                                                     "owner_weight": 78,
                                                     "owner_style": "freeride",
                                                     "owner_level": "pro",
                                                     "high_tramps": False}).json())
# check result
print(get('http://localhost:8000/api/snbs/2').json())


"""delete a snowboard"""
# bad request (wrong id)
print(delete('http://localhost:8000/api/snbs/999').json())
# bad request (wrong type)
print(delete('http://localhost:8000/api/snbs/n2').json())
# correct request
print(delete('http://localhost:8000/api/snbs/2').json())
