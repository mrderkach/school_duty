from django.test import TestCase
from django.utils import timezone
from posts.models import Post
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import unittest
from django.test.client import RequestFactory
from posts.views import *

class makeRequest:
    def __init__(self, a, b, c):
        self.method = a
        self.POST = b
        self.user = c

class PostMethodTests(TestCase):

    def setUp(self):
        User.objects.create(username='tester')

    def test_free_global(self):
        """
        free() should return amount of free places
        at the current post
        """
        capacity = 5
        busy = 2
        cur_post = Post(position='1', human_amount = capacity)
        cur_post.save()
        for i in range(busy):
            cur_post.userchoice_set.create(user=User.objects.get(username='tester'), date = timezone.now())
        self.assertEqual(cur_post.free(), capacity - busy)
        
    def test_free_negative(self):
        """
        free() should also return a negative number if there's
        too much pupils
        """
        capacity = 2
        busy = 5
        cur_post = Post(position='1', human_amount = capacity)
        cur_post.save()
        for i in range(busy):
            cur_post.userchoice_set.create(user=User.objects.get(username='tester'), date = timezone.now())
        self.assertLess(cur_post.free(), 0)   
        
class PostViewTests(TestCase):
    
    def test_details_correct_id(self):
        '''
        Context should return the correct id of the post
        '''
        test_post = Post.objects.create(position=1, human_amount=1)
        response = self.client.get(reverse('posts:details', args=(test_post.id,)))
        self.assertEqual(response.context['post'], str(test_post.id))
        
    def test_home_base_view(self):
        test_post = Post.objects.create(position=1, human_amount=1)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)     
        self.assertQuerysetEqual(response.context['posts'], list(map(lambda x: '<Post: {}>'.format(x), Post.objects.all())))
        
    def test_home_app(self):
        user = User.objects.create(username='tester', password='secret')
        test_post0 = Post.objects.create(position='410', human_amount=1)
        test_post = Post.objects.create(position='412', human_amount=1)
        usr_chc = test_post0.userchoice_set.create(user=user, date=timezone.now())
        request = makeRequest('POST', {'choice': test_post.position}, user )
        response = home(request)
        self.assertEqual(list(Post.objects.get(position='410').userchoice_set.all()), [])
        self.assertEqual(list(Post.objects.get(position='412').userchoice_set.all()), [usr_chc])