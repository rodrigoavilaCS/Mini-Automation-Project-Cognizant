Feature: Tennis Court Reservation System
  As a tennis player
  I want to reserve tennis courts online
  So that I can ensure court availability for my desired time

  Background:
    Given I am on the quick reservation page and logged in with valid credentials

  Scenario: End-to-end tennis court reservation flow
    When I select a date and desired time slot for desired tennis court
    And I confirm the booking reservation
    #Then I should see a confirmation message with reservation details