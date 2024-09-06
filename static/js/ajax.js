$(document).ready(function() {
    $('.toggle-url-list').click(function(e) {
        e.preventDefault();
        $(this).next('.url-list').slideToggle();
    });
});