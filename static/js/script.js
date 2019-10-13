$(document).ready(function() {

    $(".viewBook").click(function() {
        window.location = $(this).find("a").attr("href");
        return false;
    });
});
