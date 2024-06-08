document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {});
});

$(document).ready(function() {
    $('.animated-text').hide().fadeIn(2000);
});

document.addEventListener('DOMContentLoaded', function() {
    var modals = document.querySelectorAll('.modal');
    M.Modal.init(modals);

    document.querySelectorAll('.submit-bet').forEach(function(element) {
        element.addEventListener('click', function(event) {
            event.preventDefault();
            var betId = this.getAttribute('data-bet-id');
            var betTopic = this.getAttribute('data-bet-topic');
            var choice1 = this.getAttribute('data-choice1');
            var choice2 = this.getAttribute('data-choice2');
            document.getElementById('bet-id').innerText = betId;
            document.getElementById('bet-topic').innerText = betTopic;
            document.getElementById('choice1-label').innerText = choice1;
            document.getElementById('choice2-label').innerText = choice2;
            document.getElementById('choice1-hidden').value = choice1;
            document.getElementById('choice2-hidden').value = choice2;
            document.getElementById('bet-id-hidden').value = betId;
            document.getElementById('bet-topic-hidden').value = betTopic;
            var modalInstance = M.Modal.getInstance(document.getElementById('bet-modal'));
            modalInstance.open();
        });
    });

    var betAmountInput = document.getElementById('bet-amount');
    var betAmountValue = document.getElementById('bet-amount-value');
    betAmountInput.addEventListener('input', function() {
        betAmountValue.innerText = this.value;
    });
});