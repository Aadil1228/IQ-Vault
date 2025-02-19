let questions=window.questions
console.log(questions)
let score=0
let currentQuestionIndex = 0;
var correct=false
let count=0
const progressBarFill=document.getElementById('progress-bar-fill')

//Defining selected option for each question as empty
function selectedEmpty() {
    for (let i = 0; i < questions.length; i++) {
        questions[i].selected = '';
        questions[i].score=0;
    }
}


// Load the current question
function loadQuestion(index) {
    console.log("in load question")
    if (index < 0 || index>=questions.length){
        console.error("Invalid index: ", index);
        return;
    }
    console.log("Index :"+ index)
    document.getElementById('question-no').textContent=index+1  //Defining question no. for showing
    const question = questions[index];  //Extracting a single question out of the array
    console.log(question, question.id)
    progressBarFill.style.width=((index+1)/questions.length)*100 + '%'
    document.getElementById('question').innerHTML = question.question;
    console.log(question.selected)
    accessKeyColor(String(currentQuestionIndex+1), "#D1D72D") // Highlight the current question number
    options=[question.option1, question.option2,question.option3,question.option4]
    // Render options
    const answersContainer = document.querySelector('#options-container');
    answersContainer.innerHTML = ''; // Clear existing options
    options.forEach((option, i) => {
        const li = document.createElement('li');
        li.textContent = `${String.fromCharCode(65 + i)}) ${option}`;
        console.log("inside options render")
        li.classList.add("options")
        li.dataset.answer = option; // Correct option text
        li.classList.toggle('selected-option', question.selected.trim() === li.dataset.answer.trim()); // Restore selection
        li.addEventListener('click', () => {
            // Save the selected answer
            question.selected = li.dataset.answer;
            answersContainer.querySelectorAll('.selected-option').forEach(element => {
                element.classList.remove('selected-option')
            })
            // Highlight the selected option
            li.classList.add('selected-option');
            console.log(question.selected)
            if (question.selected===question.correct){
                question.score=question.marks
            }
            else{
                question.score=0
            }
        });
        answersContainer.appendChild(li);
    });
    console.log("outside load question")
}


function submitQuiz(){
    score=0
    questions.forEach(question=>{
        score+=question.score
    })
    console.log("total score : ", score)
    
    // console.log(questions.length*10)
    // localStorage.setItem('total', JSON.stringify(questions.length*10))
    //Counting Correct Answers
    let correctCount = 0;
    questions.forEach(question => {
        if (question.score === question.marks) {
            correctCount++;
            console.log(question.score, "inside correct count")
        }
    })
    //Counting Wrong Answers
    let wrongCount = 0;
    questions.forEach(question => {
        if (question.score !== question.marks) {
            wrongCount++;
        }
    })
    let quiz=window.quiz_details
    console.log("inside submit quiz")
    document.getElementById('scoreInput').value = score;
    document.getElementById('correctCountInput').value = correctCount;
    document.getElementById('wrongCountInput').value = wrongCount;
    document.getElementById('quiz_id').value = quiz.id;

    // Submit the form
    document.getElementById('resultForm').submit();
}

// Next Question
document.getElementById('next-btn').addEventListener('click', () => {
    console.log(questions[currentQuestionIndex].score)
    if (questions[currentQuestionIndex].selected)
        accessKeyColor(String(currentQuestionIndex+1), "#3CCC7A")
    else
        accessKeyColor(String(currentQuestionIndex+1), "white")
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        loadQuestion(currentQuestionIndex);
        if (currentQuestionIndex==questions.length-1)
            document.querySelector('#next-btn #NextOrSubmit').textContent="Submit"
    } else {
        submitQuiz()
    }
});

// Previous Question
document.getElementById('prev-btn').addEventListener('click', () => {
    if (questions[currentQuestionIndex].selected)
        accessKeyColor(String(currentQuestionIndex+1), "#3CCC7A")
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        loadQuestion(currentQuestionIndex);
    }
    if(currentQuestionIndex<questions.length-1)
        document.querySelector('#next-btn #NextOrSubmit').textContent="Next"
});

// SCAN BELOW THIS FOR OTHER CHANGES



// Initialize the first question
// loadQuestion(currentQuestionIndex);

const totalQuestions=document.getElementById("total-questions")
const accessKeyContainer=document.getElementById('question-access-keys-container')
const accessKeyContainerRight=document.getElementById('question-access-arrow-right')
const accessKeyContainerLeft=document.getElementById('question-access-arrow-left')
function load(){
    console.log("hi2")
    totalQuestions.innerHTML=questions.length
    for(let i=1;i<=questions.length;i++){
        console.log("creating access key")
        const accessKey=document.createElement('div')
        accessKey.textContent=i
        accessKey.id=i
        accessKey.classList.add('question-access-keys')
        if (i==1)
            accessKey.style.backgroundColor='#D1D72D'
        accessKey.addEventListener('click', ()=>accessKeysLoad(i-1))
        accessKeyContainer.appendChild(accessKey)
    }
    if (questions.length<5){
        accessKeyContainerRight.style.zIndex=-10
        accessKeyContainerLeft.style.zIndex=-10
    }
    progressBarFill.style.width=(1/questions.length)*100+'%'
}

document.addEventListener('DOMContentLoaded', ()=>{
    console.log("hi")
    selectedEmpty()
    loadQuestion(currentQuestionIndex)
    load()
})

function accessKeysLoad(index){
    console.log(index+ "access key clicked")
    if (questions[currentQuestionIndex].selected)
        accessKeyColor(String(currentQuestionIndex+1), "#3CCC7A")
    else
        accessKeyColor(String(currentQuestionIndex+1), "white")
    if (currentQuestionIndex <= questions.length - 1) {
        currentQuestionIndex=index;
        if (currentQuestionIndex==questions.length -1)
            document.querySelector('#next-btn #NextOrSubmit').textContent="Submit"
        else if(currentQuestionIndex<questions.length-1)
            document.querySelector('#next-btn #NextOrSubmit').textContent="Next"
        else{
            submitQuiz()
        }
        loadQuestion(currentQuestionIndex);
    } else {
        submitQuiz()
    }
}

function accessKeyColor(id, color){
    accessKeys=document.querySelectorAll('.question-access-keys')
    console.log("access key: "+ accessKeys)
    accessKeys.forEach(key => {
        console.log(key)
        if (key.id === id) {
            key.style.backgroundColor=color
        }
    })
}