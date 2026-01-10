import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from blog_app.models import Post, Category
from django.contrib.auth.models import User
from django.utils import timezone

def populate():
    # Get or create admin user
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    categories_data = [
        ('world', 'The Future of Global Connectivity', 'Global connectivity is evolving rapidly. In this post, we explore how low-orbit satellites and 6G technology are set to bridge the digital divide between continents.', 'post_images/world.png'),
        ('school', 'Modernizing the Classroom', 'Education is no longer confined to four walls. Virtual reality and interactive AI tutors are transforming how students engage with complex subjects in modern schools.', 'post_images/school.png'),
        ('village', 'The Quiet Charm of Rural Life', 'Finding peace in a fast-paced world often leads us back to the village. Discover why slow living in rural areas is becoming the ultimate luxury for the modern soul.', 'post_images/village.png'),
        ('enviroment', 'Protecting Our Oceans', 'The deep blue holds the key to our planet\'s health. We discuss the latest innovations in marine conservation and how urban centers are reducing plastic runoff.', 'post_images/env.png'),
        ('child', 'The Magic of Childhood Play', 'Unstructured play is more than just fun; it is the laboratory of the developing brain. Learn about the psychological importance of let-loose play for children.', 'post_images/child.png'),
        ('social media', 'The Evolution of Digital Identity', 'Who are we online? Social media has moved beyond simple sharing into the realm of complex digital personas and the metaverse.', 'post_images/social.png'),
        ('Technology', 'AI: Beyond the Hype', 'Artificial Intelligence is permeating every industry. We look past the buzzwords to see the real-world impact of machine learning on everyday efficiency.', 'post_images/social.png'),
        ('Lifestyle', 'Embracing Minimalism', 'Less is more. Minimalism is not just an aesthetic; it is a mental health strategy. How decluttering your physical space can clear your mind.', 'post_images/village.png'),
        ('Travel', 'Hidden Gems of the Mediterranean', 'Escape the tourists and find the soul of the Med. From secret coves in Crete to the backstreets of Sicily, here is your ultimate travel guide.', 'post_images/world.png'),
        ('Food', 'The Art of Sourdough Bread', 'Baking the perfect loaf is a science and an art. We dive into the world of wild yeast starters and the patience required for the perfect crust.', 'post_images/village.png'),
        ('Health', 'Meditation for Mental Clarity', 'In the age of information overload, silence is golden. Why 10 minutes of daily mindfulness can drastically lower stress and improve focus.', 'post_images/env.png'),
        ('Science', 'Exploring the Quantum Realm', 'Quantum physics used to be theoretical fluff. Now, it is the foundation of the next computing revolution. A beginner\'s guide to qubits.', 'post_images/env.png'),
        ('Education', 'Lifelong Learning in the Digital Age', 'Learning doesn\'t end with a degree. The digital age has democratized knowledge, making it possible to master new skills at any stage of life.', 'post_images/school.png'),
        ('Business', 'Remote Work: The New Normal', 'The office is dead; long live the home office. We analyze data from the last three years to see how remote work is affecting corporate productivity.', 'post_images/social.png'),
        ('Entertainment', 'Trends in Virtual Reality Cinema', 'Cinema is becoming immersive. VR headsets are taking audiences from passive observers to active participants in the narrative.', 'post_images/social.png'),
        ('Sports', 'The Rise of Extreme Sports', 'Pushing human limits to the edge. Why adrenaline-fueled sports like mountain biking and free climbing are seeing record-breaking participation.', 'post_images/world.png'),
    ]

    for cat_name, title, content, img_path in categories_data:
        category = Category.objects.get(name=cat_name)
        # Check if post already exists to avoid duplicates
        if not Post.objects.filter(title=title).exists():
            Post.objects.create(
                title=title,
                content=content,
                author=user,
                category=category,
                image=img_path,
                date_posted=timezone.now()
            )
            print(f"Created post: {title}")
        else:
            print(f"Post already exists: {title}")

if __name__ == '__main__':
    populate()
