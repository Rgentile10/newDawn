import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# create your automated tests here

# FORMAT TESTING, TO MAINTAIN MANAGABILITY

# HOW?
# As long as your tests are sensibly arranged, they won’t become unmanageable. Good rules-of-thumb include having:

# a separate TestClass for each model or view
# a separate test method for each set of conditions you want to test
# test method names that describe their function


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):

        # error message
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """

        time = timezone.now() + datetime.timedelta(days=30)
        # WE CREATE A QUESTION INSTANCE HERE
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

        # all three comphrehensive tests detects if the published date actually ISNT POSTED RECENTLY (this little snippet of code can be considereed covered (for now at least!))
        # And now we have three tests that confirm that Question.was_published_recently() returns sensible values for past, recent, and future questions.

    def create_question(question_text, days):
        """
        Create a question with the given `question_text` and published the
        given number of `days` offset to now (negative for questions published
        in the past, positive for questions that have yet to be published).
        """
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(
            question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(
            question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

# TODO:: IDEAS 4 MORE TESTS, including vary similar process for REsultsView

# We ought to add a similar get_queryset method to ResultsView and create a new test class for that view.
# It’ll be very similar to what we have just created; in fact there will be a lot of repetition.

# We could also improve our application in other ways, adding tests along the way.
# For example, it’s silly that Questions can be published on the site that have no Choices. So, our views could check for this, and exclude such Questions.
# Our tests would create a Question without Choices and then test that it’s not published, as well as create a similar Question with Choices, and test that it is published.

# Perhaps logged-in admin users should be allowed to see unpublished Questions, but not ordinary visitors.
# Again: whatever needs to be added to the software to accomplish this should be accompanied by a test,
# whether you write the test first and then make the code pass the test, or work out the logic in your code first and then write a test to prove it.

# At a certain point you are bound to look at your tests and wonder whether your code is suffering from test bloat, which brings us to:
