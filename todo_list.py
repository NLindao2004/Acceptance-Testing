"""
To-Do List Manager
A command-line application for managing tasks.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any


class Task:
    """Represents a single task in the to-do list."""
    
    def __init__(self, description: str, priority: str = "medium", category: str = "general"):
        self.id = None
        self.description = description
        self.status = "pending"
        self.priority = priority  # low, medium, high
        self.category = category
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed_date = None
    
    def mark_completed(self):
        """Mark the task as completed."""
        self.status = "completed"
        self.completed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'category': self.category,
            'created_date': self.created_date,
            'completed_date': self.completed_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create task from dictionary."""
        task = cls(data['description'], data['priority'], data['category'])
        task.id = data['id']
        task.status = data['status']
        task.created_date = data['created_date']
        task.completed_date = data['completed_date']
        return task


class TodoListManager:
    """Main class for managing the to-do list."""
    
    def __init__(self, data_file: str = "todo_data.json"):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
    
    def add_task(self, description: str, priority: str = "medium", category: str = "general") -> bool:
        """Add a new task to the to-do list."""
        if not description.strip():
            return False
        
        task = Task(description.strip(), priority, category)
        task.id = self.next_id
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return True
    
    def list_tasks(self) -> List[Task]:
        """Return all tasks in the to-do list."""
        return self.tasks.copy()
    
    def list_pending_tasks(self) -> List[Task]:
        """Return only pending tasks."""
        return [task for task in self.tasks if task.status == "pending"]
    
    def list_completed_tasks(self) -> List[Task]:
        """Return only completed tasks."""
        return [task for task in self.tasks if task.status == "completed"]
    
    def mark_task_completed(self, task_description: str) -> bool:
        """Mark a task as completed by its description."""
        for task in self.tasks:
            if task.description.lower() == task_description.lower() and task.status == "pending":
                task.mark_completed()
                self.save_tasks()
                return True
        return False
    
    def mark_task_completed_by_id(self, task_id: int) -> bool:
        """Mark a task as completed by its ID."""
        for task in self.tasks:
            if task.id == task_id and task.status == "pending":
                task.mark_completed()
                self.save_tasks()
                return True
        return False
    
    def remove_task(self, task_description: str) -> bool:
        """Remove a task from the list."""
        for i, task in enumerate(self.tasks):
            if task.description.lower() == task_description.lower():
                self.tasks.pop(i)
                self.save_tasks()
                return True
        return False
    
    def clear_all_tasks(self) -> bool:
        """Clear all tasks from the to-do list."""
        self.tasks.clear()
        self.next_id = 1
        self.save_tasks()
        return True
    
    def get_task_by_description(self, description: str) -> Task:
        """Find a task by its description."""
        for task in self.tasks:
            if task.description.lower() == description.lower():
                return task
        return None
    
    def is_empty(self) -> bool:
        """Check if the to-do list is empty."""
        return len(self.tasks) == 0
    
    def contains_task(self, description: str) -> bool:
        """Check if the list contains a task with the given description."""
        return any(task.description.lower() == description.lower() for task in self.tasks)
    
    def save_tasks(self):
        """Save tasks to JSON file."""
        try:
            data = {
                'next_id': self.next_id,
                'tasks': [task.to_dict() for task in self.tasks]
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def load_tasks(self):
        """Load tasks from JSON file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.next_id = data.get('next_id', 1)
                    self.tasks = [Task.from_dict(task_data) for task_data in data.get('tasks', [])]
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []
            self.next_id = 1


def display_menu():
    """Display the main menu."""
    print("\n=== To-Do List Manager ===")
    print("1. Add task")
    print("2. List all tasks")
    print("3. List pending tasks")
    print("4. List completed tasks")
    print("5. Mark task as completed")
    print("6. Remove task")
    print("7. Clear all tasks")
    print("8. Exit")
    print("=" * 27)


def display_tasks(tasks: List[Task], title: str = "Tasks"):
    """Display a list of tasks."""
    if not tasks:
        print(f"\nNo {title.lower()} found.")
        return
    
    print(f"\n{title}:")
    for task in tasks:
        status_symbol = "✓" if task.status == "completed" else "○"
        priority_symbol = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
        
        print(f"  {status_symbol} [{task.id}] {task.description}")
        print(f"    Priority: {priority_symbol} {task.priority.title()} | Category: {task.category}")
        print(f"    Created: {task.created_date}")
        if task.completed_date:
            print(f"    Completed: {task.completed_date}")
        print()


def main():
    """Main function to run the To-Do List Manager."""
    todo_manager = TodoListManager()
    
    print("Welcome to the To-Do List Manager!")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            # Add task
            description = input("Enter task description: ").strip()
            if not description:
                print("Task description cannot be empty!")
                continue
            
            priority = input("Enter priority (low/medium/high) [default: medium]: ").strip().lower()
            if priority not in ['low', 'medium', 'high']:
                priority = 'medium'
            
            category = input("Enter category [default: general]: ").strip()
            if not category:
                category = 'general'
            
            if todo_manager.add_task(description, priority, category):
                print(f"Task '{description}' added successfully!")
            else:
                print("Failed to add task!")
        
        elif choice == '2':
            # List all tasks
            tasks = todo_manager.list_tasks()
            display_tasks(tasks, "All Tasks")
        
        elif choice == '3':
            # List pending tasks
            tasks = todo_manager.list_pending_tasks()
            display_tasks(tasks, "Pending Tasks")
        
        elif choice == '4':
            # List completed tasks
            tasks = todo_manager.list_completed_tasks()
            display_tasks(tasks, "Completed Tasks")
        
        elif choice == '5':
            # Mark task as completed
            if todo_manager.is_empty():
                print("No tasks available!")
                continue
            
            display_tasks(todo_manager.list_pending_tasks(), "Pending Tasks")
            
            choice_type = input("Mark by (1) ID or (2) description? [1]: ").strip()
            
            if choice_type == '2':
                description = input("Enter task description to mark as completed: ").strip()
                if todo_manager.mark_task_completed(description):
                    print(f"Task '{description}' marked as completed!")
                else:
                    print("Task not found or already completed!")
            else:
                try:
                    task_id = int(input("Enter task ID to mark as completed: "))
                    if todo_manager.mark_task_completed_by_id(task_id):
                        print(f"Task with ID {task_id} marked as completed!")
                    else:
                        print("Task not found or already completed!")
                except ValueError:
                    print("Invalid task ID!")
        
        elif choice == '6':
            # Remove task
            if todo_manager.is_empty():
                print("No tasks available!")
                continue
            
            display_tasks(todo_manager.list_tasks(), "All Tasks")
            description = input("Enter task description to remove: ").strip()
            if todo_manager.remove_task(description):
                print(f"Task '{description}' removed successfully!")
            else:
                print("Task not found!")
        
        elif choice == '7':
            # Clear all tasks
            if todo_manager.is_empty():
                print("To-do list is already empty!")
                continue
            
            confirm = input("Are you sure you want to clear all tasks? (y/N): ").strip().lower()
            if confirm == 'y':
                todo_manager.clear_all_tasks()
                print("All tasks cleared successfully!")
            else:
                print("Operation cancelled.")
        
        elif choice == '8':
            # Exit
            print("Thank you for using To-Do List Manager!")
            break
        
        else:
            print("Invalid choice! Please enter a number between 1-8.")


if __name__ == "__main__":
    main()
