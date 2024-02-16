import requests

# Define the URL of your Flask application
url = "http://localhost:5000/recommendations"

# Example user tags
user_tags = "Waterloo Sunset What's Going On Stairway to Heaven Bohemian Rhapsody Thriller TheKinks MarvinGaye LedZeppelin Queen MichaelJackson TheKinks MarvinGaye LedZeppelin Queen MichaelJackson TheKinks MarvinGaye LedZeppelin Queen MichaelJackson Lofi R&B Rock Rock Pop"

# Send a POST request with user_tags as the request body
response = requests.post(url, json={"user_tags": user_tags})

# Check if the request was successful
if response.status_code == 200:
    # Print the recommendations
    recommendations = response.json()["recommendations"]
    print("Top similar users:")
    for user_id in recommendations:
        print(user_id)
else:
    print("Failed to get recommendations. Status code:", response.status_code)
    
'''import requests

# Define the URL of your Flask API endpoint
url = "http://localhost:5000/recommendations"

# Example userId
user_id = "User_13"

# Send a POST request with the userId as the request body
response = requests.post(url, json={"userId": user_id})

# Check if the request was successful
if response.status_code == 200:
    # Print the recommendations
    recommendations = response.json()["recommendations"]
    print("Top similar users:")
    for user_id in recommendations:
        print(user_id)
else:
    print("Failed to get recommendations. Status code:", response.status_code)'''

