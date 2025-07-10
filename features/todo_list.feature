Feature: To-Do List Manager
  As a user
  I want to manage my tasks
  So that I can keep track of what needs to be done

  Background:
    Given I have a to-do list manager

  # Suggested Scenarios from the workshop
  Scenario: Add a task to the to-do list
    Given the to-do list is empty
    When the user adds a task "Buy groceries"
    Then the to-do list should contain "Buy groceries"

  Scenario: List all tasks in the to-do list
    Given the to-do list contains tasks:
      | Task          |
      | Buy groceries |
      | Pay bills     |
    When the user lists all tasks
    Then the output should contain all tasks

  Scenario: Mark a task as completed
    Given the to-do list contains tasks:
      | Task          | Status  |
      | Buy groceries | Pending |
    When the user marks task "Buy groceries" as completed
    Then the to-do list should show task "Buy groceries" as completed

  Scenario: Clear the entire to-do list
    Given the to-do list contains tasks:
      | Task          |
      | Buy groceries |
      | Pay bills     |
    When the user clears the to-do list
    Then the to-do list should be empty

  # Additional Scenarios (2 more as required)
  Scenario: Add a task with priority and category
    Given the to-do list is empty
    When the user adds a detailed task "Complete project" with priority "high" and category "work"
    Then the to-do list should contain "Complete project"
    And the task "Complete project" should have priority "high"
    And the task "Complete project" should have category "work"

  Scenario: Attempt to add an empty task
    Given the to-do list is empty
    When the user attempts to add an empty task
    Then the task should not be added
    And the to-do list should remain empty

  # Additional feature scenarios for extended functionality
  Scenario: Remove a specific task
    Given the to-do list contains tasks:
      | Task          |
      | Buy groceries |
      | Pay bills     |
    When the user removes task "Buy groceries"
    Then the to-do list should not contain "Buy groceries"
    But the to-do list should contain "Pay bills"

  Scenario: List only pending tasks
    Given the to-do list contains tasks:
      | Task          | Status    |
      | Buy groceries | Pending   |
      | Pay bills     | Completed |
      | Walk the dog  | Pending   |
    When the user lists pending tasks
    Then the output should contain "Buy groceries"
    And the output should contain "Walk the dog"
    But the output should not contain "Pay bills"
