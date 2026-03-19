import os
import django
import requests
from django.core.files.base import ContentFile
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from blog_app.models import Post, Category
from django.contrib.auth.models import User

def populate():
    # Use the first available superuser as author
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

    blogs = [
        {
            'title': 'Agentic AI: The Next Frontier of Multimodal Models',
            'content': 'Agentic AI refers to AI systems designed to take autonomous action to achieve specific goals. Unlike basic chatbots, these agents can reason, plan, and use tools to handle complex tasks across various domains. With the evolution of multimodal models that understand text, image, and video, Agentic AI is set to become a cornerstone of daily life by 2025.',
            'category': 'Technology',
            'image_url': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'Why Minimalism is the Ultimate Strategy for Mental Health',
            'content': 'In an era of digital noise and physical clutter, minimalism offers a path to mental clarity. By intentionally choosing less, individuals can focus on what truly matters, reducing stress and anxiety. Minimalism is not just about owning fewer things; it is a mental health strategy that prioritizes quality over quantity in all aspects of life.',
            'category': 'Lifestyle',
            'image_url': 'https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'The Rise of 6G: Connecting the Unconnected',
            'content': 'While 5G is still being rolled out, researchers are already laying the foundation for 6G. Expected to launch around 2030, 6G will provide speeds 100 times faster than 5G and near-zero latency. This technology will enable revolutionary applications like holographic communication and global seamless connectivity, finally bridging the digital divide.',
            'category': 'Science',
            'image_url': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=800'
        }
    ]

    for blog in blogs:
        category, _ = Category.objects.get_or_create(name=blog['category'])
        if not Post.objects.filter(title=blog['title']).exists():
            post = Post(
                title=blog['title'],
                content=blog['content'],
                author=user,
                category=category,
                date_posted=timezone.now()
            )
            
            # Download image
            try:
                response = requests.get(blog['image_url'])
                if response.status_code == 200:
                    file_name = f"{blog['title'].lower().strip().replace(' ', '_')[:20]}.jpg"
                    post.image.save(file_name, ContentFile(response.content), save=False)
            except Exception as e:
                print(f"Failed to download image for {blog['title']}: {e}")
            
            post.save()
            print(f"Created post: {blog['title']}")
        else:
            print(f"Post already exists: {blog['title']}")

if __name__ == '__main__':
    populate()
