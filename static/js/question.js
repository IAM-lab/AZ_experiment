/*
 * NAME:			questions.js
 * AUTHOR:			Alan Davies
 * DATE:			05/02/2019
 * INSTITUTION:		Interaction Analysis and Modelling Lab (IAM), University of Manchester
 * DESCRIPTION:		Object to handle questions
 *
 */

 function QuestionManager()
 {
    var questionManager = new Object();

    // member vars
    questionManager.numGraphLiteracyQuestionBlocks = 9;
    questionManager.currentGLQuestionBlock = 1;
    questionManager.startProgress = 11.76;
    questionManager.newProgressVal = 0;

    // display demographic questions
    questionManager.nextGLQuestionBlock = function()
    {
        var progressBar = document.getElementById("gl-prog");
        var questionBlockIdString = "glq-";
        var currentBlock = "";

        this.hideAllGLQuestionBlocks();

        this.currentGLQuestionBlock++;
        currentBlock = questionBlockIdString + String(this.currentGLQuestionBlock);
        currentBlockElement = document.getElementById(currentBlock);
        currentBlockElement.style.display = "block";
        this.newProgressVal += 5.88;
        progressBar.style.width =  this.startProgress + this.newProgressVal + "%";
        progressBar.setAttribute("aria-valuenow", this.startProgress + this.newProgressVal);
    }

    // hide all the GL question blocks
    questionManager.hideAllGLQuestionBlocks = function()
    {
        var questionBlockIdString = "glq-";
        var currentBlock = "";

        for(var i = 0; i < this.numGraphLiteracyQuestionBlocks; i++)
        {
            currentBlock = questionBlockIdString + String(this.currentGLQuestionBlock);
            currentBlockElement = document.getElementById(currentBlock);
            currentBlockElement.style.display = "none";
        }
    }

    return questionManager;
 }
