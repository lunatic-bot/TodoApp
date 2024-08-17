
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




document.addEventListener('DOMContentLoaded', function() {
    // Function to toggle todo completion status
    function toggleComplete(todoId, button) {
        fetch(`/todos/toggle-complete/${todoId}`, {
            method: 'PUT', // Ensure this matches the method expected by your route
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
                // Toggle button class and text based on the new state
                if (button.classList.contains('btn-danger')) {
                    button.classList.remove('btn-danger');
                    button.classList.add('btn-success');
                    button.innerHTML = '☑️';
                } else {
                    button.classList.remove('btn-success');
                    button.classList.add('btn-danger');
                    button.innerHTML = '⬜';
                }
            } else {
                alert('Failed to update todo status');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the todo status.');
        });
    }

    // Attach the toggleComplete function to each button
    document.querySelectorAll('.toggle-complete-btn').forEach(button => {
        button.addEventListener('click', function() {
            toggleComplete(button.dataset.todoId, button);
        });
    });
});


// Function to handle the update operation
function updateTodo(todoId) {
    console.log(`Update button clicked for Todo ID: ${todoId}`); // Debugging line
    const form = document.getElementById(`updateTodoForm${todoId}`);
    const formData = new FormData(form);

    fetch(`/todos/update-todo/${todoId}`, {
        method: 'PUT',
        body: JSON.stringify({
            title: formData.get('title'),
            description: formData.get('description')
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            // alert('Todo updated successfully');
            window.location.reload(); // Reload the page to reflect changes
        } else {
            alert('Failed to update todo');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the todo.');
    });
}



