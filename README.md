### Movie Video Understanding API

This Django REST API provides functionalities that allow users to interact with movies such as retrieving specific scenes, answering movie-related questions, and engaging in dialogue with movie characters. For the demo, you can interact with a five minute clip compilation of the movie, <The Wizard of OZ>. (Using `generate_synopses.py` we generated synopses for each scene, and using `synopses_vectordb.py` we stored text embeddings of synopses in a vector database. You don't have to run these again.)

#### Key Features

1. **Video Search-driven Short-Form Contents**
   - Allows users to query specific scenes from movies.

2. **Video Question Answering Chatbot**
   - Answers user queries about movie plots or character motivations by retrieving relevant movie scenes and processing their content.

3. **Avatar Dialogue Chatbot**
   - Enables users to interact directly with a movie character avatar by asking questions that the character answers based on their dialogue and actions in the movie.

#### REST API Endpoints

1. **Short-Form Video Content Generation**
   - **Endpoint**: `/movieapi/short_form`
   - **Method**: POST
   - **Description**: Receives a textual query about a movie scene and returns the video timestemp of the scene corresponding to the query.

2. **Video Question Answering**
   - **Endpoint**: `/movieapi/video_qa`
   - **Method**: POST
   - **Description**: Processes a user's question about a movie and returns a textual response based on the content of relevant movie scenes.

3. **Avatar Dialogue Interaction**
   - **Endpoint**: `/movieapi/avatar_chat`
   - **Method**: POST
   - **Description**: Allows users to interact with a chatbot that embodies a movie character, answering questions in the character's style and perspective.

#### Example CURL Commands

- **Short-Form Video Content Generation**
  ```
  curl -X POST -H "Content-Type: application/json" -d '{"query": "Scene where the Witch melts."}' http://localhost:8000/movieapi/short_form
  # Expected Output: {"timestamp": {"start":"02:39","end":"03:12"}, "synopsis": "The Wicked Witch melts ..."}
  ```

- **Video Question Answering**
  ```
  curl -X POST -H "Content-Type: application/json" -d '{"query":"How did the witch die?"}' http://localhost:8000/movieapi/video_qa
  # Expected Output: {"answer": "The witch was melted by water thrown by Dorothy."}
  ```

- **Avatar Dialogue Interaction**
  ```
  curl -X POST -H "Content-Type: application/json" -d '{"query": "How did melting feel like?", "character": "Witch"}' http://localhost:8000/movieapi/avatar_chat
  # Expected Output: {"answer": "It was agonizing and sudden, a dreadful way to go."}
  ```

#### Unit Tests

Unit tests based on the package `unittest` are located at `movie_ai/movieapi/tests.py`
We ran the unit tests and obtained a coverage report by running these commands (You don't have to run these again):

```
cd movie_ai
coverage run --branch --source='.' manage.py test movieapi
coverage report
```

Coverage report contents are a follows:

```
Name                              Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------------
manage.py                            12      2      2      1    79%
movie_ai/__init__.py                  0      0      0      0   100%
movie_ai/asgi.py                      4      4      0      0     0%
movie_ai/settings.py                 20      0      0      0   100%
movie_ai/urls.py                      3      0      0      0   100%
movie_ai/wsgi.py                      4      4      0      0     0%
movieapi/__init__.py                  0      0      0      0   100%
movieapi/admin.py                     1      0      0      0   100%
movieapi/apps.py                      4      0      0      0   100%
movieapi/migrations/__init__.py       0      0      0      0   100%
movieapi/models.py                    1      0      0      0   100%
movieapi/mongo_utils.py               5      0      0      0   100%
movieapi/tests.py                    25      0      0      0   100%
movieapi/urls.py                      3      0      0      0   100%
movieapi/views.py                    68      4     14      5    89%
-------------------------------------------------------------------
TOTAL                               150     14     16      6    88%
```

