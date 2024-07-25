from behave import *

use_step_matcher("re")


@given("Navigate to https://gh-users-search\.netlify\.app/")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given Navigate to https://gh-users-search.netlify.app/')