$(document).ready(function() {


$(".newsletter-email").click(function (){
$(this).val("");
});

$(".arrow-next").mouseenter(function() {
$(this).css("background", "url('images/a03.png') -186px -35px no-repeat");
})
.mouseleave(function(){
$(this).css("background", "url('images/a03.png') 55px -35px no-repeat");
});

$(".arrow-next").mousedown(function() {
$(this).css("background", "url('images/a03.png') -66px -35px no-repeat");
})
.mouseup(function(){
$(this).css("background", "url('images/a03.png') 55px -35px no-repeat");
});

$(".arrow-previous").mouseenter(function() {
$(this).css("background", "url('images/a03.png') -125px -35px no-repeat");
})
.mouseleave(function() {
$(this).css("background", "url('images/a03.png') 55px -35px no-repeat");
});

$(".arrow-previous").mousedown(function(){
$(this).css("background", "url('images/a03.png') -5px -35px no-repeat");
})
.mouseup(function(){
$(this).css("background", "url('images/a03.png') 55px -35px no-repeat");
});

function validateEmail(sEmail) {
    var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
    if (filter.test(sEmail)) {
        return true;
    }
    else {
        return false;
    }
};

});