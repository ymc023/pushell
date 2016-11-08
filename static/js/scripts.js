jQuery(document).ready(function() {
    $('.page-container form').submit(function(){
        var username = $(this).find('.username').val();
        var password = $(this).find('.password').val();
        var token = $(this).find('.token').val();
        var re = /^\d{6,}$/;
        if(username == '') {
            $(this).find('.error').fadeOut('fast', function(){
                $(this).css('top', '64px');
            });
            $(this).find('.error').fadeIn('fast', function(){
                $(this).parent().find('.username').focus();
            });
            return false;
        }
        if(password == '') {
            $(this).find('.error').fadeOut('fast', function(){
                $(this).css('top', '64px');
            });
            $(this).find('.error').fadeIn('fast', function(){
                $(this).parent().find('.password').focus();
            });
            return false;
        }
        if(token=='') {
            $(this).find('.error').fadeOut('fast', function(){
                $(this).css('top', '143px');
            });
            $(this).find('.error').fadeIn('fast', function(){
                $(this).parent().find('.token').focus();
            });
            return false;
        }
        if(!re.test(token)) {
            $(this).find('.error').fadeOut('fast', function(){
                $(this).css('top', '143px');
            });
            $(this).find('.error').fadeIn('fast', function(){
                $(this).parent().find('.token').focus();
            });
            return false;
        }
    });

    $('.page-container form .username, .page-container form .password').keyup(function(){
        $(this).parent().find('.error').fadeOut('fast');
    });

});
