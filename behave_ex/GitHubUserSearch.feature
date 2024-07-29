Feature: Search for users' data on GitHub to track changes in real time

  Background:
    Given Navigate to https://gh-users-search.netlify.app/
    When UI: Search for GradPolina

  Scenario: Verify total number of Repos, Followers, Following, and Gists against API
    Then GitHub Integration API: verify total number of Repos
    And GitHub Integration API: verify total number of Followers
    And GitHub Integration API: verify total number of Following
    And GitHub Integration API: verify total number of Gists

  Scenario: Verify user components
    Then GitHub Integration API: verify user's Full Name, Twitter, Bio, Company Name, Location, and Blog


  Scenario: Display followers components
    Then API: send GET request to users/GradPolina/followers?per_page=100
    And Display followers components with max 100 followers
    #And Each followers has Name and Link






