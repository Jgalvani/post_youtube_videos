import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from tqdm import tqdm
from datetime import timedelta
from lib.args import args

# Set up the YouTube API client
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret_file.json', 
    [
        'https://www.googleapis.com/auth/youtube.force-ssl',
        'https://www.googleapis.com/auth/youtube.upload'
    ]
)
credentials = flow.run_local_server(port=0)
youtube = build('youtube', 'v3', credentials=credentials)

def post_video(path, date):
    """ Upload the new video """
    
    # Define the parameters for the new video
    title = os.path.dirname(path).split('/')[-1]
    description = title + '\nSome description...'
    
    try:
        # Create the video resource
        video_resource = {
            'snippet': {
                'title': title,
                'description': description,
                'categoryId': '10',  # Set the category ID to the content of your video (10 = music)
            },
            
            # publish at a specific date
            'status': {
                'privacyStatus': 'private',
                'publishAt': date
            }
        }

        # Insert the video into the authenticated user's YouTube channel
        print('posting video...')
        insert_response = youtube.videos().insert(
            part='snippet,status',
            body=video_resource,
            media_body=MediaFileUpload(path)
        ).execute()

        id = insert_response["id"]
        
        print(f'The video was uploaded with ID: {id}')
        
    except HttpError as error:
        print(f'An error occurred: {error}')
    

if args.unique:
        if not os.path.isdir(args.inputs):
            print(f'{args.inputs} is not a directory')
            exit()
            
        post_video(args.inputs, args.date.isoformat())
        exit()
        
for index, directory in enumerate(tqdm(os.listdir(args.inputs), desc='directories', position=1)):
    
    path = os.path.join(args.inputs, directory)
    if not os.path.isdir(path):
        tqdm.write(f'{path} is not a directory')
        continue
    
    date = args.date + timedelta(day=index)
    
    post_video(path, date.isoformat())
    
    
