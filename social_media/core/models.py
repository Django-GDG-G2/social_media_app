from django.db import models
from users.models import User
  

class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.TextField(max_length=150, blank=False)
    content = models.TextField()
    media = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"posted by {self.author.username} | {self.created_at}"




class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.author.username} commented on the post {self.post.id}"
    


class Like(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'post')  # A user can only like a post once.

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"