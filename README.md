# UniTest

UniTest is a web-based portal designed for faculty members to create, conduct, evaluate, and assess online surprise tests for their batches. It provides an intuitive interface for managing tests, batches, courses, and students, making the process of test management seamless and efficient.

## Features

-   **User Authentication**: Secure login and registration for faculty members.

-   **Dashboard**: Overview of active tests, total students, tests conducted, and average scores.

-   **Test Management**:
    -   Create and manage multiple-choice question tests.
    -   Add questions and options with correct answers.
    -   View test details, including duration, total marks, and questions.

-   **Batch Management**:
    -   Add, update, and delete batches.
    -   View batch details such as name, session, semester, and section.

-   **Course Management**:
    -   Add, update, and delete courses.
    -   Manage course details like course name and code.

-   **Student Management**: View a list of students associated with the portal.

## Technologies Used

-   **Backend**: Django (Python)

-   **Frontend**: HTML, CSS, JavaScript

-   **Database**: SQLite

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/lavenderpeaches/UniTest
    cd UniTest
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Apply migrations:

    ```bash
    python manage.py migrate
    ```

4. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Usage

1. **Login/Register**: Faculty members can log in or register to access the portal.

2. **Dashboard**: View an overview of tests and statistics.

3. **Create Tests**: Navigate to "Create Test" to set up a new test.

4. **Manage Batches and Courses**: Add, update, or delete batches and courses.

5. **View Tests**: Access the list of all tests and their details.

## Folder Structure

-   `base/`: Contains the core app for managing models, views, forms, and URLs.

-   `templates/`: HTML templates for the frontend.

-   `static/`: Static files such as CSS and JavaScript.

-   `migrations/`: Database migration files.

-   `db.sqlite3`: SQLite database file.

-   `manage.py`: Django's command-line utility.

## Contributing

Contributions are welcome! Please follow these steps to contribute to the project:

1. **Fork the Repository**:

    - Navigate to the [UniTest GitHub repository](https://github.com/lavenderpeaches/UniTest).

    - Click the "Fork" button in the top-right corner to create a copy of the repository under your GitHub account.

2. **Clone the Forked Repository**:

    - Open a terminal and run the following command to clone the forked repository to your local machine:
        ```bash
        git clone https://github.com/your-username/UniTest.git
        ```
    - Replace `your-username` with your GitHub username.

3. **Set Up the Development Environment**:

    - Navigate to the project directory:
        ```bash
        cd UniTest
        ```
    - Install the required dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    - Apply database migrations:
        ```bash
        python manage.py migrate
        ```

4. **Create a New Branch**:

    - Create a new branch for your feature or bug fix:
        ```bash
        git checkout -b feature-name
        ```
    - Replace `feature-name` with a descriptive name for your branch.

5. **Make Changes**:

    - Implement your changes or additions in the appropriate files.

    - Ensure your code follows the project's coding standards and conventions.

6. **Test Your Changes**:

    - Run the development server to test your changes:
        ```bash
        python manage.py runserver
        ```
    - Verify that your changes work as expected and do not break existing functionality.

7. **Commit Your Changes**:

    - Stage your changes:
        ```bash
        git add .
        ```
    - Commit your changes with a descriptive message:
        ```bash
        git commit -m "Add feature-name"
        ```

8. **Push to Your Branch**:

    - Push your branch to your forked repository:
        ```bash
        git push origin feature-name
        ```

9. **Open a Pull Request**: Go to the original repository on GitHub and submit a pull request. Provide a clear and detailed description of your changes in the pull request.

10. **Address Feedback**:

    - Collaborate with the maintainers to review your pull request.

    - Make any requested changes and push them to your branch.

11. **Celebrate**:

    - Once your pull request is merged, your contribution will be part of the project!

## Contributors

We extend our gratitude to the following individuals for their contributions to the project:

-   **Yuvraj Singh**: https://github.com/Yuvraj-Singh01

-   **Deepali**: https://github.com/lavenderpeaches

If you would like to contribute, please refer to the [Contributing](#contributing) section above.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any inquiries or feedback, please contact yuvsingh18@gmail.com or deepalix7@gmail.com.