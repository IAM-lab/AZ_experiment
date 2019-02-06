/*
 * NAME:			popup.js
 * AUTHOR:			Alan Davies
 * DATE:			05/02/2019
 * INSTITUTION:		Interaction Analysis and Modelling Lab (IAM), University of Manchester
 * DESCRIPTION:		Object to handle popups
 *
 */

function PopupController()
{
    var popupController = new Object();

    // member vars
    popupController.consentAgreed = false;
    popupController.pageMask = document.getElementById("page-mask");
    popupController.PISPopup = document.getElementById("PIS-popup");
    popupController.popupText = document.getElementById("pis-popup-text");

    // resize/position popup
    popupController.resizeAndPositionPopup = function()
    {
        this.PISPopup.style.left = (window.innerWidth / 2) - (this.PISPopup.offsetWidth / 2) + "px";
        this.PISPopup.style.height = (window.innerHeight) - (this.PISPopup.offsetTop * 4) + "px";
        this.popupText.style.height = ((60 * this.PISPopup.offsetHeight) / 100) + "px";

        // enable consent button when scrolled to the bottom
        jQuery(function($) {
            $('#pis-popup-text').on('scroll', function() {
                if($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
                    $('#consent-check').prop('disabled', false);
                    popupController.consentAgreed = true;
                }
            })
        });
    }

    // show popup
    popupController.showPopup = function()
    {
        this.pageMask.style.display = "block";
        this.PISPopup.style.display = "block";
        this.resizeAndPositionPopup();
    }

    // hide popup
    popupController.hidePopup = function()
    {
        this.pageMask.style.display = "none";
        this.PISPopup.style.display = "none";
    }

    // on consent given
    popupController.consented = function()
    {
        if(this.consentAgreed) {
            $('#pis-popup-ok').prop('disabled', false);
        }
    }

    // enable start study
    popupController.enableStudyStart = function()
    {
        this.hidePopup();
        $('#begin-study').prop('disabled', false);
        $('#begin-study').addClass('btn btn-dark pulse-button');
    }

    return popupController;
}