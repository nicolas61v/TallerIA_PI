import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images from the media/movie/images/ folder"

    def handle(self, *args, **kwargs):
        # ✅ Directory where images are stored
        images_folder = 'media/movie/images/'
        
        # ✅ Verify the folder exists
        if not os.path.exists(images_folder):
            self.stderr.write(f"Images folder '{images_folder}' not found.")
            return

        updated_count = 0
        not_found_count = 0

        # ✅ Get all movies from database
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in database")

        # ✅ Process each movie
        for movie in movies:
            try:
                # ✅ Look for image file with format m_MOVIE_TITLE.png
                image_filename = f"m_{movie.title}.png"
                image_path_full = os.path.join(images_folder, image_filename)
                
                # ✅ Check if the image file exists
                if os.path.exists(image_path_full):
                    # ✅ Update the movie's image field with relative path
                    movie.image = os.path.join('movie/images', image_filename)
                    movie.save()
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
                else:
                    not_found_count += 1
                    self.stdout.write(self.style.WARNING(f"Image not found for: {movie.title} (looking for {image_filename})"))

            except Exception as e:
                self.stderr.write(f"Failed to update {movie.title}: {str(e)}")

        # ✅ Show final summary
        self.stdout.write(self.style.SUCCESS(f"Finished updating images."))
        self.stdout.write(self.style.SUCCESS(f"Images updated: {updated_count}"))
        self.stdout.write(self.style.WARNING(f"Images not found: {not_found_count}"))
        
        # ✅ List available images in folder for reference
        self.stdout.write("\nAvailable images in folder:")
        try:
            for filename in os.listdir(images_folder):
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    self.stdout.write(f"  - {filename}")
        except Exception as e:
            self.stderr.write(f"Could not list images folder: {str(e)}")