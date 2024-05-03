import base64
import requests
import json
from tqdm import tqdm


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

scene_data = []
with open('./data/scenes.json', 'r') as f:
    lines = f.readlines()
    for line in lines:
        scene_data.append(json.loads(line))

synopses_data = []
for data in tqdm(scene_data):

    scene_id = data["id"]
    movie_name = data["movie"]
    subtitles = data["subtitles"]

    base64_image = encode_image(f"./data/scenes/{scene_id}.jpg")

    prompt = f"""The following is a scene from the movie, {movie_name}

    Here are the subtitles:
    ```
    {subtitles}
    ```

    Please examine the scene and write a scene synopsis."""

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    payload = {
      "model": "gpt-4-turbo",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 512
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    synopsis = response.json()['choices'][0]['message']['content']
    synopses_data.append({'id':scene_id, 'synopsis': synopsis})

with open('./data/synopses.json', 'w') as f:
    for data in synopses_data:
        json.dump(data, f)
        f.write('\n')
