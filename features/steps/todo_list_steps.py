"""
Step definitions for To-Do List Manager BDD tests.
"""

import os
import tempfile
from behave import given, when, then, step
from todo_list import TodoListManager, Task


@given('I have a to-do list manager')
def step_impl(context):
    """Initialize a to-do list manager for testing."""
    # Create a temporary file for testing
    context.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    context.temp_file.close()
    context.todo_manager = TodoListManager(context.temp_file.name)
    context.last_output = ""


@given('the to-do list is empty')
def step_impl(context):
    """Ensure the to-do list is empty."""
    context.todo_manager.clear_all_tasks()
    assert context.todo_manager.is_empty(), "To-do list should be empty"


@given('the to-do list contains tasks')
def step_impl(context):
    """Add tasks to the to-do list from the table."""
    context.todo_manager.clear_all_tasks()
    
    # Store the table for later use
    context.expected_tasks = []
    
    for row in context.table:
        task_description = row['Task']
        status = row.get('Status', 'Pending')
        
        # Store expected task info
        context.expected_tasks.append({
            'description': task_description,
            'status': status
        })
        
        # Add the task
        context.todo_manager.add_task(task_description)
        
        # Mark as completed if specified
        if status.lower() == 'completed':
            context.todo_manager.mark_task_completed(task_description)


@when('the user adds a task "{task_description}"')
def step_add_simple_task(context, task_description):
    """Add a task to the to-do list."""
    context.result = context.todo_manager.add_task(task_description)


@when('the user adds a detailed task "{task_description}" with priority "{priority}" and category "{category}"')
def step_add_detailed_task(context, task_description, priority, category):
    """Add a task with priority and category."""
    context.result = context.todo_manager.add_task(task_description, priority, category)


@when('the user attempts to add an empty task')
def step_impl(context):
    """Attempt to add an empty task."""
    context.result = context.todo_manager.add_task("")


@when('the user lists all tasks')
def step_impl(context):
    """List all tasks."""
    context.last_output = context.todo_manager.list_tasks()


@when('the user lists pending tasks')
def step_impl(context):
    """List pending tasks."""
    context.last_output = context.todo_manager.list_pending_tasks()


@when('the user marks task "{task_description}" as completed')
def step_impl(context, task_description):
    """Mark a task as completed."""
    context.result = context.todo_manager.mark_task_completed(task_description)


@when('the user removes task "{task_description}"')
def step_impl(context, task_description):
    """Remove a task from the list."""
    context.result = context.todo_manager.remove_task(task_description)


@when('the user clears the to-do list')
def step_impl(context):
    """Clear all tasks from the to-do list."""
    context.result = context.todo_manager.clear_all_tasks()


@then('the to-do list should contain "{task_description}"')
def step_impl(context, task_description):
    """Verify that the to-do list contains the specified task."""
    assert context.todo_manager.contains_task(task_description), \
        f"Task '{task_description}' not found in to-do list"


@then('the to-do list should not contain "{task_description}"')
def step_impl(context, task_description):
    """Verify that the to-do list does not contain the specified task."""
    assert not context.todo_manager.contains_task(task_description), \
        f"Task '{task_description}' should not be in to-do list"


@then('the to-do list should show task "{task_description}" as completed')
def step_impl(context, task_description):
    """Verify that the task is marked as completed."""
    task = context.todo_manager.get_task_by_description(task_description)
    assert task is not None, f"Task '{task_description}' not found"
    assert task.status == "completed", f"Task '{task_description}' is not completed"


@then('the to-do list should be empty')
def step_impl(context):
    """Verify that the to-do list is empty."""
    assert context.todo_manager.is_empty(), "To-do list should be empty"


@then('the to-do list should remain empty')
def step_impl(context):
    """Verify that the to-do list remains empty."""
    assert context.todo_manager.is_empty(), "To-do list should remain empty"


@then('the task should not be added')
def step_impl(context):
    """Verify that the task was not added."""
    assert not context.result, "Task should not have been added"


@then('the task "{task_description}" should have priority "{priority}"')
def step_impl(context, task_description, priority):
    """Verify that the task has the specified priority."""
    task = context.todo_manager.get_task_by_description(task_description)
    assert task is not None, f"Task '{task_description}' not found"
    assert task.priority == priority, f"Task priority should be '{priority}', but was '{task.priority}'"


@then('the task "{task_description}" should have category "{category}"')
def step_impl(context, task_description, category):
    """Verify that the task has the specified category."""
    task = context.todo_manager.get_task_by_description(task_description)
    assert task is not None, f"Task '{task_description}' not found"
    assert task.category == category, f"Task category should be '{category}', but was '{task.category}'"


@then('the output should contain all tasks')
def step_impl(context):
    """Verify that the output contains all tasks."""
    tasks = context.last_output
    assert len(tasks) > 0, "Output should contain tasks"
    
    # Check that all expected tasks are present
    if hasattr(context, 'expected_tasks'):
        for expected_task in context.expected_tasks:
            task_description = expected_task['description']
            found = any(task.description == task_description for task in tasks)
            assert found, f"Task '{task_description}' not found in output"


@then('the output should contain "{task_description}"')
def step_impl(context, task_description):
    """Verify that the output contains the specified task."""
    tasks = context.last_output
    found = any(task.description == task_description for task in tasks)
    assert found, f"Task '{task_description}' not found in output"


@then('the output should not contain "{task_description}"')
def step_impl(context, task_description):
    """Verify that the output does not contain the specified task."""
    tasks = context.last_output
    found = any(task.description == task_description for task in tasks)
    assert not found, f"Task '{task_description}' should not be in output"


@step('the to-do list should contain "{task_description}"')
def step_impl(context, task_description):
    """Step that can be used with And/But."""
    assert context.todo_manager.contains_task(task_description), \
        f"Task '{task_description}' not found in to-do list"


def after_scenario(context, scenario):
    """Clean up after each scenario."""
    if hasattr(context, 'temp_file'):
        try:
            os.unlink(context.temp_file.name)
        except:
            pass
