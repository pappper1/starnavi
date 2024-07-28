# from faker import Faker
import json
#
# fake = Faker()
#
# # Генерация данных для модели User
# users = [{
#     "email": fake.email(),
#     "hashed_password": fake.password(),
#     "is_ai_answer_comments": fake.boolean(),
#     "comments_ai_answer_delay": fake.random_int(min=1, max=10),
# } for i in range(1, 101)]
#
# # Генерация данных для модели Post
# posts = [{
#     "title": fake.sentence(),
#     "content":fake.text(),
#     "photo_uid": fake.uuid4(),
#     "author_id": fake.random_int(min=1, max=100),
#     "is_blocked": fake.boolean(),
# } for i in range(1, 101)]
#
#
#
# # Сохранение сгенерированных данных в файлы
# with open('app/tests/mock_users.json', 'w', encoding='utf-8') as f:
#     json.dump(users, f, ensure_ascii=False, indent=4)
#
# with open('app/tests/mock_posts.json', 'w', encoding='utf-8') as f:
#     json.dump(posts, f, ensure_ascii=False, indent=4)
with open ('app/tests/mock_users.json', 'r') as f:
    posts = json.load(f)
    for post in posts:
        del post["id"]

    with open('app/tests/mock_users.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)
