from django.db import models

#                                       User model
class user(models.Model):
    Name = models.CharField(max_length = 100)
    Email = models.EmailField()
    Phone = models.IntegerField()
    State = models.CharField(max_length = 100)
    City = models.CharField(max_length = 100)
    Password = models.CharField(max_length = 100)

#                                       Model for Storing Query
class feed(models.Model):
    Query_box = models.TextField()
    Email = models.EmailField()
    Raise = models.IntegerField()

#                                       Model for Storing Comments
class feed_answer(models.Model):
    Query_Id = models.IntegerField()
    Comment = models.CharField(max_length = 200)

#                                       Model for storing Trade_feed
class Trade_feed(models.Model):
    Email = models.EmailField()
    Trade = models.TextField()

#                                      Model for storing Raise issues
class raise_issue(models.Model):
    Raise_Id = models.IntegerField()
    Email = models.EmailField()

#                                     Models for storing Feedbacks
class feedback(models.Model):
    Feedback = models.TextField()
    Email = models.EmailField()
