document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('testForm');
    const addQuestionBtn = document.getElementById('addQuestionBtn');
    const questionsContainer = document.getElementById('questionsContainer');
    const questionTemplate = document.getElementById('questionTemplate');
    const toast = document.getElementById('toast');

    let questionCount = 0;

    // Add initial question
    addQuestion();

    // Add question button click handler
    addQuestionBtn.addEventListener('click', addQuestion);

    // Form submit handler
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        if (validateForm()) {
            // Collect form data
            const formData = {
                title: document.getElementById('title').value,
                course: document.getElementById('course').value,
                duration: document.getElementById('duration').value,
                totalMarks: document.getElementById('totalMarks').value,
                description: document.getElementById('description').value,
                questions: [],
            };

            // Collect questions data
            const questionCards = document.querySelectorAll('.question-card');
            questionCards.forEach((card) => {
                const questionData = {
                    questionText: card.querySelector('[name="questionText"]').value,
                    marks: card.querySelector('[name="marks"]').value,
                    options: [{ text: card.querySelector('[name="optionA"]').value }, { text: card.querySelector('[name="optionB"]').value }, { text: card.querySelector('[name="optionC"]').value }, { text: card.querySelector('[name="optionD"]').value }],
                    correctOption: card.querySelector('input[name="correctOption"]:checked').value,
                };
                formData.questions.push(questionData);
            });

            // Show success toast
            showToast();

            // Log the form data (in a real app, you would send this to the server)
            console.log('Form Data:', formData);
        }
    });

    // Function to add a new question
    function addQuestion() {
        questionCount++;

        // Clone the template
        const questionNode = document.importNode(questionTemplate.content, true);

        // Update question number
        questionNode.querySelector('.question-number').textContent = questionCount;

        // Update radio button IDs to make them unique
        const radioInputs = questionNode.querySelectorAll('input[type="radio"]');
        radioInputs.forEach((input) => {
            const newId = input.id + questionCount;
            const label = questionNode.querySelector(`label[for="${input.id}"]`);
            input.id = newId;
            label.setAttribute('for', newId);
            input.name = `correctOption${questionCount}`;
        });

        // Add delete button handler
        const deleteBtn = questionNode.querySelector('.delete-question');
        deleteBtn.addEventListener('click', function () {
            if (questionCount > 1) {
                this.closest('.question-card').remove();
                updateQuestionNumbers();
            }
        });

        // Append the new question
        questionsContainer.appendChild(questionNode);
    }

    // Function to update question numbers after deletion
    function updateQuestionNumbers() {
        const questionCards = document.querySelectorAll('.question-card');
        questionCount = questionCards.length;

        questionCards.forEach((card, index) => {
            card.querySelector('.question-number').textContent = index + 1;
        });
    }

    // Function to validate the form
    function validateForm() {
        let isValid = true;

        // Validate test details
        const requiredFields = ['title', 'course', 'duration', 'totalMarks'];
        requiredFields.forEach((field) => {
            const input = document.getElementById(field);
            const errorElement = document.getElementById(`${field}-error`);

            if (!input.value.trim()) {
                errorElement.textContent = 'This field is required';
                isValid = false;
            } else {
                errorElement.textContent = '';
            }
        });

        // Validate questions
        const questionCards = document.querySelectorAll('.question-card');
        questionCards.forEach((card) => {
            // Validate question text
            const questionText = card.querySelector('[name="questionText"]');
            const questionTextError = questionText.nextElementSibling;

            if (!questionText.value.trim()) {
                questionTextError.textContent = 'Question text is required';
                isValid = false;
            } else {
                questionTextError.textContent = '';
            }

            // Validate marks
            const marks = card.querySelector('[name="marks"]');
            const marksError = marks.nextElementSibling;

            if (!marks.value.trim()) {
                marksError.textContent = 'Marks are required';
                isValid = false;
            } else {
                marksError.textContent = '';
            }

            // Validate options
            const options = [card.querySelector('[name="optionA"]'), card.querySelector('[name="optionB"]'), card.querySelector('[name="optionC"]'), card.querySelector('[name="optionD"]')];

            options.forEach((option, index) => {
                const optionError = option.nextElementSibling;

                if (!option.value.trim()) {
                    optionError.textContent = `Option ${String.fromCharCode(65 + index)} is required`;
                    isValid = false;
                } else {
                    optionError.textContent = '';
                }
            });

            // Validate correct option
            const correctOption = card.querySelector('input[name^="correctOption"]:checked');
            const correctOptionError = card.querySelector('.radio-group').nextElementSibling;

            if (!correctOption) {
                correctOptionError.textContent = 'Please select the correct option';
                isValid = false;
            } else {
                correctOptionError.textContent = '';
            }
        });

        return isValid;
    }

    // Function to show toast notification
    function showToast() {
        toast.classList.add('show');

        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
});
