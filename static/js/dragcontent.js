/*
 * NAME:			dragcontent.js
 * AUTHOR:			Alan Davies
 * DATE:			18/04/2019
 * INSTITUTION:		Interaction Analysis and Modelling Lab (IAM), University of Manchester
 * DESCRIPTION:		Object to handle dragging content
 *
 */

function DragContent()
{
    var dragContent = new Object();

    // member vars
    dragContent.pos1 = 0;
    dragContent.pos2 = 0;
    dragContent.pos3 = 0;
    dragContent.pos4 = 0;
    dragContent.elmnt = null;

    // drag element around
    dragContent.dragElement = function(elmnt)
    {
        this.elmnt = elmnt;
        this.elmnt.onmousedown = this.dragMouseDown;
    }

    // call functions on mouse up/move
    dragContent.dragMouseDown = function(e)
    {
        e = e || window.event;
        e.preventDefault();

        this.pos3 = e.clientX;
        this.pos4 = e.clientY;
        document.onmouseup = dragContent.closeDragElement;
        document.onmousemove = dragContent.elementDrag;
    }

    // reposition element
    dragContent.elementDrag = function(e)
    {
        e = e || window.event;
        e.preventDefault();

        this.pos1 = this.pos3 - e.clientX;
        this.pos2 = this.pos4 - e.clientY;
        this.pos3 = e.clientX;
        this.pos4 = e.clientY;

        dragContent.elmnt.style.top = (dragContent.elmnt.offsetTop - this.pos2) + "px";
        dragContent.elmnt.style.left = (dragContent.elmnt.offsetLeft - this.pos1) + "px";
    }

    // tidy up
    dragContent.closeDragElement = function()
    {
        document.onmouseup = null;
        document.onmousemove = null;
    }

    return dragContent;
}