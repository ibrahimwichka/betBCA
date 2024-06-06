document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {});
});

$(document).ready(function() {
    $('.animated-text').hide().fadeIn(2000);
});