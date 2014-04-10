views['login'] = ->
    $.ajaxSetup({ cache: true });
    $.getScript('//connect.facebook.net/en_US/all.js', ->
        window.fbAsyncInit = ->
            FB.init
                appId: '502137286574807'
                status: true
    )

    $('#login-fb').click ->
        $('#login-fb').button("loading")
        FB.getLoginStatus(facebookStatusCallback)

    facebookStatusCallback = (response) ->
        console.log response
        if response.status == 'connected'
            accessToken = response.authResponse.accessToken
            FB.api('/me?field=name', (response) ->
                $('#login-facebook-id').val(response.id)
                $('#login-facebook-token').val(accessToken)
                $('#login-form').submit()
            )
        else
            FB.login(facebookStatusCallback)
