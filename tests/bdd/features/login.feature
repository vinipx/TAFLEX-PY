Feature: User Login

  @PROJ-123
  Scenario: Successful login to The Internet
    Given I navigate to "https://the-internet.herokuapp.com/login"
    When I enter "tomsmith" as username and "SuperSecretPassword!" as password
    And I click on the login button
    Then I should see "You logged into a secure area!" in the flash message
