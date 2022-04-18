users = dict()
users['Liza'] = [0]
users['Nikita'] = [0]
print(users)
users.get('Nikita').append(2131)
users.get('Liza').append(2132)
print(users.values())
