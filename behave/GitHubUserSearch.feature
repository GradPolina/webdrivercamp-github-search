Feature: Search for users' data on GitHub to track changes in real time

  Background:
    Given Navigate to https://gh-users-search.netlify.app/
    When UI: Search for GradPolina

  Scenario: Navigate to the page

  Scenario: Search for User

  Scenario: Verify total number of Repos against API
    Then GitHub Integration API: verify total number of Repos

  Scenario: Verify number of followers against API
    And API: send GET request to users/<username>/followers?per_page=100
    And API: verify status code is 200
    Then GitHub Integration API: verify fields values




