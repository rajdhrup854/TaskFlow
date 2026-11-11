
from task_manager import work, completed_tasks, save_tasks



if __name__ == "__main__":

    print("=====TaskFlow=====")

    while True:

        print("Let's start today's work!\n"
              "1. Add a task\n"
              "2. View all tasks\n"
              "3. Delete a task\n"
              "4. Mark a task as completed\n"
              "5. View completed tasks\n"
              "6. Search for a task\n"
              "7. View task statistics\n"
              "8. Exit\n")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input! Please enter a valid number.")
            continue

        #===ADDING TASKS===#

        if choice == 1:
            task = input("Enter the task you want to add: ").strip()

            if task in work:
                print("Task already exists.")
            elif task in completed_tasks:
                print("Task already completed.")
            elif task == "":
                print("Task cannot be empty.")
            else:
                work.append(task)
                save_tasks()
                print("Task added successfully!")

        #===VIEWING TASKS===#

        elif choice == 2:
            if len(work) == 0:
                print("No tasks available.")
            else:
                print("\nYour Pending Tasks:\n")

                for number, task in enumerate(work, start=1):
                    print(number, task)

        #===DELETING TASKS===#

        elif choice == 3:
            if len(work) == 0:
                print("No tasks available to delete.")
            else:
                print("\nYour Pending Tasks:\n")

                for number, task in enumerate(work, start=1):
                    print(number, task)

                try:
                    task_number = int(input("Enter the task number to delete: "))

                    if 1 <= task_number <= len(work):
                        work.pop(task_number - 1)
                        save_tasks()
                        print("Task deleted successfully!")
                    else:
                        print("Invalid task number.")

                except ValueError:
                    print("Please enter a valid task number.")

        #===MARKING TASKS AS COMPLETED===#

        elif choice == 4:
            if len(work) == 0:
                print("No pending tasks available.")
            else:
                print("\nYour Pending Tasks:\n")

                for number, task in enumerate(work, start=1):
                    print(number, task)

                try:
                    task_number = int(input("Enter the task number to complete: "))

                    if 1 <= task_number <= len(work):
                        task = work.pop(task_number - 1)
                        completed_tasks.append(task)
                        save_tasks()
                        print("Congratulations! You have completed a task.")
                    else:
                        print("Invalid task number.")

                except ValueError:
                    print("Please enter a valid task number.")

        #===VIEWING COMPLETED TASKS===#

        elif choice == 5:
            if len(completed_tasks) == 0:
                print("No completed task yet!")
            else:
                print("\nYour Completed Tasks:\n")

                for number, task in enumerate(completed_tasks, start=1):
                    print(number, task)

                print("\nRemaining tasks:", len(work))

        #===SEARCHING FOR TASKS===#

        elif choice == 6:
            search_task = input("Enter the task you want to search for: ").strip()

            if search_task in work:
                print("Task found!")
                print("status: Not completed yet!")
            elif search_task in completed_tasks:
                print("Task found!")
                print("status: Completed!")
            else:
                print("Task not found.")

        #===VIEWING TASK STATISTICS===#

        elif choice == 7:
            total_tasks = len(work) + len(completed_tasks)

            print("\n===== Task Statistics =====")
            print("Total tasks:", total_tasks)
            print("Completed tasks:", len(completed_tasks))
            print("Pending tasks:", len(work))

            if total_tasks > 0:
                completed_percentage = (len(completed_tasks) / total_tasks) * 100
                print("Completed percentage: {:.2f}%".format(completed_percentage))
            else:
                print("Completed percentage: 0.00%")

        #===EXITING APPLICATION===#

        elif choice == 8:
            print("Exiting application. Goodbye!")
            break

        #===INVALID CHOICE===#

        else:
            print("Invalid choice. Please try again.")
