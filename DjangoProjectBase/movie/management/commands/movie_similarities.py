import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Compare two movies and optionally a prompt using OpenAI embeddings"

    def handle(self, *args, **kwargs):
        # ✅ Load OpenAI API key
        load_dotenv('../openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        # ✅ Get the first two movies from our database
        movies = Movie.objects.all()[:2]
        if len(movies) < 2:
            self.stderr.write("Need at least 2 movies in database")
            return
            
        movie1 = movies[0]  # First movie: La captura
        movie2 = movies[1]  # Second movie: Castillo medieval

        self.stdout.write(f"Comparing movies: '{movie1.title}' and '{movie2.title}'")

        def get_embedding(text):
            response = client.embeddings.create(
                input=[text],
                model="text-embedding-3-small"
            )
            return np.array(response.data[0].embedding, dtype=np.float32)

        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        # ✅ Generate embeddings of both movies
        self.stdout.write(f"Generating embedding for '{movie1.title}'...")
        emb1 = get_embedding(movie1.description)
        
        self.stdout.write(f"Generating embedding for '{movie2.title}'...")
        emb2 = get_embedding(movie2.description)

        # ✅ Compute similarity between movies
        similarity = cosine_similarity(emb1, emb2)
        self.stdout.write(f"Similitud entre '{movie1.title}' y '{movie2.title}': {similarity:.4f}")

        # ✅ Optional: Compare against a prompt
        prompt = "película infantil de animación llena de aventuras"
        self.stdout.write(f"Generating embedding for prompt: '{prompt}'...")
        prompt_emb = get_embedding(prompt)

        sim_prompt_movie1 = cosine_similarity(prompt_emb, emb1)
        sim_prompt_movie2 = cosine_similarity(prompt_emb, emb2)

        self.stdout.write(f"Similitud prompt vs '{movie1.title}': {sim_prompt_movie1:.4f}")
        self.stdout.write(f"Similitud prompt vs '{movie2.title}': {sim_prompt_movie2:.4f}")
        
        # ✅ Show which movie is more similar to the prompt
        if sim_prompt_movie1 > sim_prompt_movie2:
            self.stdout.write(self.style.SUCCESS(f"La película más similar al prompt es: '{movie1.title}'"))
        else:
            self.stdout.write(self.style.SUCCESS(f"La película más similar al prompt es: '{movie2.title}'"))