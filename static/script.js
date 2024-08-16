
document.getElementById('todoForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    // Gather the form data
    const formData = new FormData(this);
    const data = {
        title: formData.get('title'),
        description: formData.get('description')
    };

    try {
        // Send a POST request to the server
        const response = await fetch('/todos/add-todo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            // Handle successful response
            // alert('Todo added successfully!');
            window.location.reload();
            this.reset(); // Reset the form
        } else {
            // Handle errors
            alert('Failed to add todo.');
        }
    } catch (error) {
        // Handle network errors
        console.error('Error:', error);
        alert('An error occurred while adding the todo.');
    }
});


// update toggle and delete button
document.addEventListener('DOMContentLoaded', function() {
    // Handle toggle complete
    // document.querySelectorAll('.toggle-complete-btn').forEach(button => {
    //     button.addEventListener('click', async function() {
    //         const todoItem = this.closest('.todo-item');
    //         const todoId = todoItem.getAttribute('data-id');
    //         const completed = todoItem.querySelector('.completed-status').innerText === 'Yes';
            
    //         try {
    //             const response = await fetch(`/todos/toggle-complete/${todoId}`, {
    //                 method: 'PATCH',
    //                 headers: {
    //                     'Content-Type': 'application/json'
    //                 },
    //                 body: JSON.stringify({ completed: !completed })
    //             });

    //             if (response.ok) {
    //                 // Toggle the button color and completed status text
    //                 todoItem.querySelector('.completed-status').innerText = completed ? 'No' : 'Yes';
    //                 this.classList.toggle('btn-green');
    //                 this.classList.toggle('btn-red');
    //             } else {
    //                 alert('Failed to toggle todo completion.');
    //             }
    //         } catch (error) {
    //             console.error('Error:', error);
    //             alert('An error occurred while toggling todo completion.');
    //         }
    //     });
    // });

    // Handle delete
    // document.querySelectorAll('.delete-btn').forEach(button => {
    //     button.addEventListener('click', async function() {
    //         const todoItem = this.closest('.todo-item');
    //         const todoId = todoItem.getAttribute('data-id');

    //         try {
    //             const response = await fetch(`/todos/delete_todo/${todoId}`, {
    //                 method: 'DELETE'
    //             });

    //             if (response.ok) {
    //                 todoItem.remove();
    //             } else {
    //                 alert('Failed to delete todo.');
    //             }
    //         } catch (error) {
    //             console.error('Error:', error);
    //             alert('An error occurred while deleting the todo.');
    //         }
    //     });
    // });

    // Handle update
    document.querySelectorAll('.update-btn').forEach(button => {
        button.addEventListener('click', function() {
            const todoItem = this.closest('.todo-item');
            const todoId = todoItem.getAttribute('data-id');
            const title = todoItem.querySelector('strong').innerText;
            const description = todoItem.querySelector('strong').nextSibling.textContent.trim();

            // Populate the update form with the current todo details
            document.getElementById('update-id').value = todoId;
            document.getElementById('update-title').value = title;
            document.getElementById('update-description').value = description;

            // Show the update form
            document.getElementById('update-form-container').style.display = 'block';
        });
    });

    // Handle update form submission
    document.getElementById('updateForm').addEventListener('submit', async function(event) {
        event.preventDefault();

        const todoId = document.getElementById('update-id').value;
        const data = {
            title: document.getElementById('update-title').value,
            description: document.getElementById('update-description').value
        };

        try {
            const response = await fetch(`/todos/update_todo/${todoId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                // Update the UI with the new details
                const todoItem = document.querySelector(`.todo-item[data-id="${todoId}"]`);
                todoItem.querySelector('strong').innerText = data.title;
                todoItem.querySelector('strong').nextSibling.textContent = `: ${data.description}`;
                document.getElementById('update-form-container').style.display = 'none';
                alert('Todo updated successfully!');
            } else {
                alert('Failed to update todo.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while updating the todo.');
        }
    });
});


function deleteTodo(todoId) {
    fetch(`/todos/delete-todo/${todoId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            // alert('Todo deleted successfully');
            window.location.reload(); // Reload the page to reflect changes
        } else {
            alert('Failed to delete todo');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the todo.');
    });
}


function toggleComplete(todoId) {
    fetch(`/todos/toggle-complete/${todoId}`, {
        method: 'PUT', // Ensure this matches the method expected by your route
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            alert('Todo status updated successfully');
            window.location.reload(); // Reload the page to reflect changes
        } else {
            alert('Failed to update todo status');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the todo status.');
    });
}


