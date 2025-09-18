import os
import random
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Show embedding for a random movie"

    def handle(self, *args, **kwargs):
        # ✅ Load OpenAI API key
        load_dotenv('../openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        # ✅ Get a random movie from the database
        movies = Movie.objects.all()
        if not movies:
            self.stderr.write("No movies found in database")
            return
            
        random_movie = random.choice(movies)
        
        self.stdout.write(f"Selected random movie: '{random_movie.title}'")
        self.stdout.write(f"Description: {random_movie.description}")
        self.stdout.write("=" * 60)

        def get_embedding(text):
            response = client.embeddings.create(
                input=[text],
                model="text-embedding-3-small"
            )
            return np.array(response.data[0].embedding, dtype=np.float32)

        # ✅ Generate embedding for the random movie
        self.stdout.write("Generating embedding...")
        embedding = get_embedding(random_movie.description)
        
        # ✅ Show embedding info
        self.stdout.write(f"Embedding dimension: {len(embedding)}")
        self.stdout.write(f"Embedding type: {type(embedding)}")
        self.stdout.write("=" * 60)
        
        # ✅ Show first 10 values of the embedding
        self.stdout.write("First 10 embedding values:")
        for i, value in enumerate(embedding[:10]):
            self.stdout.write(f"  [{i}]: {value:.6f}")
        
        self.stdout.write("=" * 60)
        
        # ✅ Show last 10 values of the embedding
        self.stdout.write("Last 10 embedding values:")
        for i, value in enumerate(embedding[-10:], start=len(embedding)-10):
            self.stdout.write(f"  [{i}]: {value:.6f}")
            
        self.stdout.write("=" * 60)
        self.stdout.write(f"Successfully generated {len(embedding)}-dimensional embedding for '{random_movie.title}'")