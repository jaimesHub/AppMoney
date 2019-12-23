import pymongo
import uuid

from bson.objectid import ObjectId

client = pymongo.MongoClient(
    "mongodb+srv://jaime:12345678A@clusterdemo-zcrgs.mongodb.net/test?retryWrites=true&w=majority")
db = client.project

# db.project.insert_one({
#     '_id': str(uuid.uuid4()),
#     'budget_day': 1540,
#     'expense_day': 1320,
#     'category_day': 'Category 2',
#     'date': 2
# })
# print(len(list(db.project.find({}))))

# print(db.project.find())


def len_db():
    return len(list(db.project.find({})))

def db_add_new_transaction(id_user, expense, category, note, date, wallet, type_trans):
    db.project.insert_one({
        '_id': str(uuid.uuid4()),
        'id_user': ObjectId(id_user),
        'expense': expense,
        'category': category,
        'note': note,
        'date': date,   # now = datetime.now(), now.strftime("%H:%M:%S, %DD/%MM/%YY")
        'wallet': wallet,
        'type': type_trans
    })

def update_id_user_into_db(id_user):
    db.project.insert({
        'id_user': ObjectId(id_user)
    })


def get_all_transactions():
    return db.project.find({})


def delete_item_from_db(_id):
    db.project.delete_one({'_id': _id})


def update_item_from_db(_id, expense, category, note, date, wallet, type_trans):
    for item in db.project.find({}):
        if item['_id'] == _id:
            db.project.update_one({
                'expense': expense,
                'category': category,
                'note': note,
                'date': date,
                'wallet': wallet,
                'type': type_trans
            })
        break
    return item

def create_new_user(username, email, password):
    db.user.insert_one({
        'username': username,
        'email': email,
        'password': password
    })

def delete_user(id):
    db.user.delete_one({'_id': ObjectId(id)})

def get_user_by_name(username):
    # print(id)
    return db.user.find_one({'username': username})