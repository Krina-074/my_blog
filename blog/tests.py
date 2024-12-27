from django.test import TestCase
from django.core.cache import cache
from .models import Post, Comment

class PostModelTest(TestCase):

    def setUp(self):
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.'
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post content.')
        self.assertIsNotNone(self.post.created_at)

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')


class CommentModelTest(TestCase):

    def setUp(self):
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            content='This is a test comment.'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'This is a test comment.')
        self.assertEqual(self.comment.post, self.post)
        self.assertIsNotNone(self.comment.created_at)

    def test_comment_str(self):
        self.assertEqual(str(self.comment), f'Comment on {self.post.title}')


class PostSignalTest(TestCase):

    def setUp(self):
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.'
        )

    def test_cache_cleared_on_post_save(self):
        cache.set('recent_posts', 'some_value')
        self.assertEqual(cache.get('recent_posts'), 'some_value')

        # Save the post again to trigger the post_save signal
        self.post.title = 'Updated Test Post'
        self.post.save()

        # Check if the cache has been cleared
        self.assertIsNone(cache.get('recent_posts'))

    def test_cache_cleared_on_post_delete(self):
        cache.set('recent_posts', 'some_value')
        self.assertEqual(cache.get('recent_posts'), 'some_value')

        # Delete the post to trigger the post_delete signal
        self.post.delete()

        # Check if the cache has been cleared
        self.assertIsNone(cache.get('recent_posts'))