from pymongo import MongoClient

# Підключення до MongoDB у Docker
client = MongoClient("mongodb://admin:secret@localhost:27017")

# База та колекція
db = client["goit_hw_mongo"]
collection = db["cats"]

# Очищаємо колекцію, щоб не дублювати дані
collection.delete_many({})

# CREATE — додавання котів
cats_data = [
    {"name": "Барсік", "age": 3, "features": ["чорний", "грайливий", "дружній"]},
    {"name": "Мурзик", "age": 5, "features": ["білий", "спокійний", "любить спати"]},
    {"name": "Пушок", "age": 2, "features": ["сірий", "енергійний", "любить рибу"]}
]
collection.insert_many(cats_data)
print("✅ Коти додані.")

# READ — всі коти
print("\n📋 Всі коти:")
for cat in collection.find():
    print(cat)

# READ — коти старші 3 років
print("\n📋 Коти старші 3 років:")
for cat in collection.find({"age": {"$gt": 3}}):
    print(cat)

# UPDATE — додаємо характеристику Барсіку
collection.update_one({"name": "Барсік"}, {"$push": {"features": "любить молоко"}})
print("\n✏️ Після оновлення Барсік:")
for cat in collection.find({"name": "Барсік"}):
    print(cat)

# DELETE — видаляємо Пушка
collection.delete_one({"name": "Пушок"})
print("\n🗑️ Після видалення Пушок:")
for cat in collection.find():
    print(cat)
