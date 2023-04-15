// Due date alert
    // get all todo item due dates
    const todoItemDates = document.getElementsByClassName('todo-item');
    console.log(todoItemDates)

    // set the number of days before the due date to show the pop-up window
    const daysBeforeDue = 2;

    // loop through all todo item due dates
    for (let i = 0; i < todoItemDates.length; i++) {
        const dueDate = new Date(todoItemDates[i].innerText);
        console.log(dueDate)
        const currentDate = new Date();

        // calculate the difference between the due date and the current date in milliseconds
        const timeDiff = dueDate.getTime() - currentDate.getTime();
        console.log(timeDiff)

        const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
        console.log(daysDiff)

        // the pop-up window
        if (daysDiff <= daysBeforeDue) {
            const todoItemName = todoItemDates[i].previousElementSibling.innerText;
            console.log(todoItemName)
            const message = "Todo item : " + todoItemName + " is due in " + daysDiff + " day(s).";
            alert(message);
            todoItemDates[i].previousElementSibling.style.color="red"

        }
    }
