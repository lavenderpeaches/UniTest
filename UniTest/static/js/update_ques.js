document.addEventListener('DOMContentLoaded', function() {
    // Add choice button functionality
    const addChoiceButtons = document.querySelectorAll('.add-choice');
    addChoiceButtons.forEach(button => {
        button.addEventListener('click', function() {
            const questionNum = this.getAttribute('data-question');
            const optionsContainer = this.closest('.question-card').querySelector('.options-container');
            const existingOptions = optionsContainer.querySelectorAll('.option-item');
            const newOptionNum = existingOptions.length + 1;

            if (newOptionNum <= 6) { // Maximum 6 choices
                const newOption = document.createElement('div');
                newOption.className = 'option-item';
                newOption.innerHTML = `
                    <span class="option-label">${String.fromCharCode(64 + newOptionNum)}.</span>
                    <input type="text" name="choice_${questionNum}_${newOptionNum}" required />
                    <input type="checkbox" name="is_correct_${questionNum}_${newOptionNum}" /> Correct
                    <button type="button" class="button ghost remove-choice">
                        <span class="icon trash">×</span>
                    </button>
                    <div class="error-message"></div>
                `;
                optionsContainer.appendChild(newOption);

                // Add event listener to the new remove button
                const removeButton = newOption.querySelector('.remove-choice');
                removeButton.addEventListener('click', function() {
                    this.closest('.option-item').remove();
                    updateOptionLabels(optionsContainer);
                });
            }

            if (newOptionNum >= 6) {
                button.disabled = true;
            }
        });
    });

    // Function to update option labels (A, B, C, etc.) after removal
    function updateOptionLabels(container) {
        const options = container.querySelectorAll('.option-item');
        options.forEach((option, index) => {
            const label = option.querySelector('.option-label');
            label.textContent = `${String.fromCharCode(65 + index)}.`;
        });
    }

    // Form validation
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        let isValid = true;

        // Check if each question has at least one correct answer
        const questions = document.querySelectorAll('.question-card');
        questions.forEach((question, qIndex) => {
            const correctAnswers = question.querySelectorAll('input[type="checkbox"]:checked');
            if (correctAnswers.length === 0) {
                const errorMsg = question.querySelector('.options-container .error-message');
                errorMsg.textContent = 'Please select at least one correct answer.';
                isValid = false;
            }
        });

        if (!isValid) {
            event.preventDefault();
        } else {
            // Remove this line to allow form submission
            // event.preventDefault();
            const toast = document.getElementById('toast');
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
                // Redirect would happen here in a real app
                window.location.href = '/tests/'; // Change to your desired redirect URL
            }, 3000);
        }
    });
});