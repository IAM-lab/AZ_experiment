/*
 * NAME:			main.js
 * AUTHOR:			Alan Davies
 * DATE:			05/02/2019
 * INSTITUTION:		Interaction Analysis and Modelling Lab (IAM), University of Manchester
 * DESCRIPTION:		Main JS page
 */

// system objects
var popupController = null;
var questionManager = null;
var dragContent = null;

// initialisation function
function initializeMain()
{
    // create objects
    popupController = PopupController();
    questionManager = QuestionManager();
    dragContent = DragContent();
}
