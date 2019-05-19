from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta

from home.models import Project
from home.models import Profile

class ProjectTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create_user(username="Testermans", password="123456789")
        Project.objects.create(owner=testuser, title="First Project", abstract="Abstract", description="description", created=datetime.now()-timedelta(days=10), anonymity=False, visible=True)
        Project.objects.create(owner=testuser, title="Project 2", abstract="Abstract", description="description", created=datetime.now()-timedelta(days=6), anonymity=False, visible=True)
        Project.objects.create(owner=testuser, title="Project 3", abstract="Abstract", description="description", created=datetime.now()-timedelta(days=3), anonymity=False, visible=True)
        Project.objects.create(owner=testuser, title="Most recent project", abstract="Abstract", description="description", created=datetime.now(), anonymity=False, visible=True)

    def test_ordering_first_created_project_last_in_query(self):
        ''' When the projects are querried, the oldest project must be last in the query'''
        self.assertEqual(Project.objects.all().last().title, "First Project", "The oldest project was not at the end of the resultset generated by Project.objects.all()")

    def test_ordering_last_created_project_first_in_query(self):
        ''' When the projects are querried, the latest newly created project must be first'''
        self.assertEqual(Project.objects.all().first().title, "Most recent project", "The most recently created project was not first in the resultset of the Project.objects.all() querry. ORDERING CAN BE WRONG IN TESTS DUE TO CACHING I THINK, BUT NO PROBLEMS ARE FOUND IN PRODUCITION, just make sure it is ordered at ['-created']")

    def test_project_deleted_if_user_is_deleted(self):
        ''' If the user gets deleted, all the projects he made should also be deleted'''
        self.assertEqual(Project.objects.all().count(), 4, "More projects are added in the testcase or something else happened")
        User.objects.get(username="Testermans").delete()
        self.assertEqual(Project.objects.all().count(), 0, "All projects created by the testuser should have been deleted")

    def test_project_string_should_be_project_name(self):
        ''' ConnectID uses the __str__ method of projects to display the project title '''
        project = Project.objects.all().first()
        self.assertEqual(str(project), project.title, "If the project is converted to a string, it must be it's title as this is used in various UI components")

class ProfileBasicTestCase(TestCase):
    ''' To test user/profiles without actually creating the profile'''

    def setUp(self):
        User.objects.create_user(username="Testermans", password="123456789")

    def test_profile_created_when_user_created(self):
        ''' An empty profile should be made for every user. Use the _base_manager to get the profiles because the default one is overwritten'''
        user = User.objects.get(username="Testermans")
        self.assertTrue(Profile._base_manager.get(user=user))

    def test_profile_deleted_when_user_deleted(self):
        ''' The profile should be delted when the user gets deleted. Use the _base_manager to get the profiles because de default one is overwritten'''
        self.assertEqual(User.objects.all().count(), 1, "This test needs to be adjusted because it depends on only one user to be created in the SetUp function")
        User.objects.get(username="Testermans").delete()
        self.assertEqual(Profile._base_manager.all().count(), 0, "If the user is deleted, it's profile should also be deleted")

    def test_profile_not_returned_if_headline_and_bio_are_empty(self):
        ''' Users that are pure superusers (for the Django Admin) have profiles with empty headlines and bio's (this is required at sign in for regular users). They should not be treated as regular users.'''
        self.assertEqual(Profile.objects.all().count(), 0, "If the headline and bio are empty, it is supposed that the user is strictly a superuser with no real account on the platform and thus should not be displayed among other users in the platform.")

class ProfileAdvancedTestCase(TestCase):
    ''' To test user/profiles with full profiles'''

    def setUp(self):
        testuser = User.objects.create_user(username="Testermans", password="123456789")
        profile = testuser.profile
        profile.headline = "This is the headline"
        profile.whyImHere = "This is why I'm here"
        profile.bio = "This is my full bio"
        profile.linkedin = "https://linkedin.com"
        profile.save()

    def test_profile_favorites(self):
        ''' Generate comma seperated string of favorite projects, only used in the Admin'''
        otheruser = User.objects.create_user(username="Otheruser", password="123456789")
        project1 = Project.objects.create(owner=otheruser, title="Project 1", abstract="Abstract", description="description", created=datetime.now() - timedelta(days=10), anonymity=False, visible=True)
        project2 = Project.objects.create(owner=otheruser, title="Project 2", abstract="Abstract", description="description", created=datetime.now() - timedelta(days=6), anonymity=False, visible=True)
        profile = Profile.objects.get(user__username="Testermans")
        profile.favorites.add(project1, project2)
        self.assertEqual(profile.get_favorites(), "Project 2,Project 1", "Get_favorites() should return a string with all favorites seperated by a comma. ORDERING CAN BE WRONG IN TESTS DUE TO CACHING I THINK, BUT NO PROBLEMS ARE FOUND IN PRODUCITION, just make sure it is ordered at ['-created'] ")
