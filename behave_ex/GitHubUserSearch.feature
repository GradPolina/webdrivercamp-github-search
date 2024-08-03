Feature: Search for users' data on GitHub to track changes in real time

  Background:
    Given Navigate to https://gh-users-search.netlify.app/
    When UI: Search for GradPolina

  Scenario Outline: Verify total info
    Then GitHub Integration API: verify total number of <options>
    Examples:
    |options   |
    |repos     |
    |followers |
    |following |
    |gists     |


  Scenario Outline: Verify user components
    Then GitHub Integration API: verify user's <data_type>
    Examples:
    |data_type     |
    |Full Name     |
    |Twitter       |
    |Bio           |
    |Company Name  |
    |Location      |
    |Blog          |


  Scenario: Display followers components
    Then Display followers components with max 100 followers
    And Each followers has Name and Link






