# Movie Video Understanding Web App

Welcome to the Movie Video Understanding Web App! This web application leverages advanced AI-driven video understanding to provide users with rich interactions based on movie scenes. Whether you’re interested in exploring specific scenes, getting answers to movie-related questions, or chatting with movie characters, our app has you covered.

## Features

Our web application provides the following key features:

1. **Video Scene Search**: Search for specific scenes in movies and get timestamps.
2. **Video Question Answering**: Ask questions about movie plots and get detailed answers based on relevant scenes.
3. **Avatar Dialogue Chatbot**: Chat with avatars of movie characters, asking them questions based on their dialogue and actions in the movie.

## Using the Web App

### Video Scene Search

- **Description**: Allows users to search for specific movie scenes and get the timestamps for those scenes.

- **How to Use**:
  1. In the chat interface, type the command `/scene <query>`, replacing `<query>` with your search term.
  2. The app will return the scene timestamp and a brief synopsis.

  **Example**:
  ```bash
  /scene scene where the Witch melts
  ```
  **Output**:
  ```
  02:39 ~ 03:12 - In this iconic scene from "The Wizard of Oz," the wicked witch menacingly ignites the Scarecrow's arm with fire, causing panic among his friends—Dorothy, the Tin Man, and the Cowardly Lion. Reacting quickly, Dorothy grabs a bucket of water to douse the flames that have engulfed the Scarecrow. However, in her frantic attempt to save her friend, she also inadvertently splashes the Witch with water. This causes the Witch to melt away dramatically, screaming about her demise and cursing Dorothy for her accidental victory...
  ```

### Video Question Answering

- **Description**: Answers user questions about movie plots based on the content of relevant movie scenes.

- **How to Use**:
  1. In the chat interface, type the command `/qa <question>`, replacing `<question>` with your query.
  2. The app will provide an answer based on the movie scenes.

  **Example**:
  ```bash
  /qa How did the witch die?
  ```
  **Output**:
  ```
  The witch died when Dorothy, in an attempt to save the Scarecrow whose arm was on fire, threw a bucket of water on him, and some of the water accidentally splashed onto the Wicked Witch of the West. This caused the Witch to dramatically melt away, screaming about her demise and cursing Dorothy for her accidental victory.
  ```

### Avatar Dialogue Chatbot

- **Description**: Allows users to chat with avatars of movie characters, asking them questions based on their dialogue and actions.

- **How to Use**:
  1. In the chat interface, type the command `/chat <question> --avatar <character>`, replacing `<question>` with your query and `<character>` with the character’s name.
  2. The app will simulate the character's response based on their dialogue.

  **Example**:
  ```bash
  /chat What did melting feel like? --avatar Witch
  ```
  **Output**:
  ```
  Witch says - Ohhh -- you curious creature! Melting! Such a peculiar and indescribable sensation it was! Imagine, if you will, the very essence of one's being dissolving, like sugar into tea, but far, far more agonizing. It felt as if every wicked deed, every dark spell, every ounce of my power was being washed away in a torrent of righteous indignation...
  ```
