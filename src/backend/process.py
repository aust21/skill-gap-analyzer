# import redis, os, json
# from dotenv import load_dotenv

# load_dotenv()

# pool = redis.ConnectionPool(
#     decode_responses=True,
#     host=os.getenv("REDIS_HOST"),
#     port=15612,
#     password=os.getenv("REDIS_PASSWORD"),
#     username="default"
# )
# r = redis.Redis(connection_pool=pool)

# def load_to_redis(job_title: str):
#     job_title = job_title.title()
#     key = f"sk:{job_title}"
#     data = r.get(key)
#     # print("-"*50)
#     # print(job_title)
#     # print(data)
#     # print("-" * 50)

#     if data:
#         data = json.loads(data)
#         return data

#     new_data = {
#         "title":job_title,
#         "skills":[]
#     }

#     r.set(key, json.dumps(new_data))


# def load_to_postgres():
#     pass

# # load_to_redis("data engineer")