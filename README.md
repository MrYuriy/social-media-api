# Social Media API
## Description
RESTful API for a social media platform. The API allow users to create profiles, follow other users, create and retrieve posts, manage comments, and perform basic social media actions.

# Getting Started

To get started with the Social Media API, follow these steps:
(using PyCharm you can click on the green arrow without copying command)

1. Clone the repository:

    ```shell
    git clone https://github.com/phaishuk/social-media-api
    ```

2. Navigate to the project directory (don't forget to check the directory where you clone the project):

    ```shell
    cd social-media-api
    ```

3. Create a virtual environment:

    ```shell
   python -m venv venv
   ```

4. Activate the virtual environment:

   - For Windows:
   ```shell
   env\Scripts\activate
   ```
   - For MacOS, Unix, Linux:
   ```shell
   source env/bin/activate
   ```

5. Install the required dependencies:
```shell
pip install -r requirements.txt
```

6. Run server:
   Review the list of environment variables present in the .env.sample file.\
   These variables are placeholders for the actual values that need to be set in file .env

```shell
python manage.py runserver
```

7. Apply database migrations & and prepared data for testing:

```shell
python manage.py migrate
```

## Features

### User Registration and Authentication:

Users can register with their email and password to create an account.
Users can login with their credentials and receive a token for authentication.
Users can logout and invalidate their token.

### User Profile:

Users can create and update their profile, including profile picture, bio, and other details.
Users can retrieve their own profile and view profiles of other users.
Users can search for users by username or other criteria.

### Follow/Unfollow:
Users can follow and unfollow other users.
Users can view the list of users they are following and the list of users following them.
### Post Creation and Retrieval:
Users can create new posts with text content and optional media attachments (e.g., images).
Users can retrieve their own posts and posts of users they are following.
Users can retrieve posts by title and context.
### Comments:
Users can add comments to posts and view comments on posts.

## API Permissions:
Only authenticated users can perform actions such as creating posts/comments, and following/unfollowing users.
Users can update and delete their own posts and comments.
Users can update and delete their own profile.
## API Documentation:
The API is well-documented with clear instructions on how to use each endpoint.