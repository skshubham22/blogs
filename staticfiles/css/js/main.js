// static/js/main.js
$(document).ready(function() {
    // Like functionality
    $('.like-btn').click(function(e) {
        e.preventDefault();
        var postId = $(this).data('post-id');
        var button = $(this);
        
        $.ajax({
            url: '/post/' + postId + '/like/',
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                if (response.liked) {
                    button.find('i').addClass('text-danger');
                } else {
                    button.find('i').removeClass('text-danger');
                }
                button.find('.like-count').text(response.total_likes);
            },
            error: function(xhr, status, error) {
                if (xhr.status === 403) {
                    window.location.href = '/login/?next=' + window.location.pathname;
                }
            }
        });
    });
    
    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});